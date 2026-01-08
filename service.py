from sqlalchemy.orm import Session
import models, schemas
from plugin_manager import manager
from fastapi import BackgroundTasks 

def get_incident(db: Session, incident_id: int):
    return db.query(models.Incident).filter(models.Incident.id == incident_id).first()
def get_incidents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Incident).offset(skip).limit(limit).all()

# Helper function that runs the plugins
def run_plugins(incident_title: str):
    notification_plugins = manager.get_all_by_type("notification")
    for plugin in notification_plugins:
        plugin.send(
            message=f"New Incident Created: {incident_title}",
            targets=["oncall-channel"] 
        )

def create_incident(db: Session, incident: schemas.IncidentCreate, background_tasks: BackgroundTasks):
    db_incident = models.Incident(
        title=incident.title,
        description=incident.description,
        priority=incident.priority,
        status="Open"
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)

    background_tasks.add_task(run_plugins, incident_title=db_incident.title)
    
    return db_incident

def update_incident(db: Session, incident_id: int, incident_update: schemas.IncidentUpdate):
    db_incident = get_incident(db, incident_id)
    if not db_incident:
        return None
    
    # --- STATE MACHINE LOGIC ---
    if incident_update.status:
        current_status = db_incident.status
        new_status = incident_update.status
        
        # Rule: Cannot re-open a closed incident
        if current_status == "Closed" and new_status != "Closed":
            raise ValueError("Cannot re-open a closed incident")
        
        # Rule: Must go to investigating before fixed
        if current_status == "Open" and new_status == "Fixed":
             raise ValueError("Must investigate before fixing")
             
    # --- END LOGIC ---
    # Update fields
    update_data = incident_update.model_dump(exclude_unset=True) # Only update sent fields
    for key, value in update_data.items():
        setattr(db_incident, key, value)
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident