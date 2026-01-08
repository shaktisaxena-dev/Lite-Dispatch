from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas, service, security  # Import security
from database import get_db, SessionLocal  # Import SessionLocal
from fastapi import BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Request
from logging_config import configure_logging, logger


app = FastAPI(title="Lite-Dispatch", version="0.1.0")


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Lite-Dispatch is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.on_event("startup")
def create_test_user():
    configure_logging()
    db = SessionLocal()
    # Check if user exists
    if (
        not db.query(models.User)
        .filter(models.User.email == "admin@example.com")
        .first()
    ):
        user = models.User(
            email="admin@example.com",
            hashed_password=security.get_password_hash("secret"),
        )
        db.add(user)
        db.commit()
    db.close()


# Middleware to log requests (Observe "Duration")
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("request_started", path=request.url.path, method=request.method)

    response = await call_next(request)

    logger.info("request_finished", status=response.status_code)
    return response


# 2. Login Route
@app.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    # In real app: decode token and get user from DB
    return token


@app.post(
    "/incidents/", response_model=schemas.Incident, status_code=status.HTTP_201_CREATED
)
def create_incident(
    incident: schemas.IncidentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return service.create_incident(
        db=db, incident=incident, background_tasks=background_tasks
    )


@app.get("/incidents/{incident_id}", response_model=schemas.Incident)
def read_incident(incident_id: int, db: Session = Depends(get_db)):
    db_incident = service.get_incident(db, incident_id=incident_id)
    if db_incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return db_incident


@app.get("/incidents/", response_model=List[schemas.Incident])
def read_incidents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_incidents(db, skip=skip, limit=limit)


@app.put("/incidents/{incident_id}", response_model=schemas.Incident)
def update_incident(
    incident_id: int,
    incident_update: schemas.IncidentUpdate,
    db: Session = Depends(get_db),
):
    try:
        db_incident = service.update_incident(db, incident_id, incident_update)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if db_incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return db_incident
