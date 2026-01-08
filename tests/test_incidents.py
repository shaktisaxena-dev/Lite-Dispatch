def test_create_incident(client):
    response = client.post(
        "/incidents/", json={"title": "Test Incident", "priority": "High"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Incident"
    assert "id" in data


def test_read_incident(client):
    # 1. Create
    create_res = client.post(
        "/incidents/", json={"title": "To be read", "priority": "Low"}
    )
    incident_id = create_res.json()["id"]
    # 2. Read
    response = client.get(f"/incidents/{incident_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "To be read"


def test_incident_state_flow(client):
    # 1. Create
    res = client.post("/incidents/", json={"title": "Flow Test"})
    incident_id = res.json()["id"]
    # 2. Try closing immediately (Should Fail)
    res = client.put(f"/incidents/{incident_id}", json={"status": "Closed"})
    assert (
        res.status_code == 400
    )  # Or 500 if we didn't handle exception well? Update main.py if needed!
    # Wait, in module 3 we raised ValueError, and main.py caught it!

    # 3. Investigate
    res = client.put(f"/incidents/{incident_id}", json={"status": "Investigating"})
    assert res.status_code == 200
    assert res.json()["status"] == "Investigating"
