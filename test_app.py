import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_signup_success():
    """Test successful signup"""
    response = client.post("/activities/Chess%20Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    assert "Signed up newstudent@mergington.edu for Chess Club" in response.json()["message"]

def test_duplicate_signup():
    """Test that duplicate signup is prevented"""
    # First signup
    client.post("/activities/Chess%20Club/signup?email=dupe@mergington.edu")
    # Second signup should fail
    response = client.post("/activities/Chess%20Club/signup?email=dupe@mergington.edu")
    assert response.status_code == 400
    assert "Student already signed up for this activity" in response.json()["detail"]

def test_activity_full():
    """Test that signup fails when activity is full"""
    # Chess Club has max_participants: 12, currently 2 participants
    # Add 10 more to fill it up
    for i in range(10):
        client.post(f"/activities/Chess%20Club/signup?email=student{i}@mergington.edu")

    # Now it should be full (12 participants)
    response = client.post("/activities/Chess%20Club/signup?email=overflow@mergington.edu")
    assert response.status_code == 400
    assert "Activity is full" in response.json()["detail"]

def test_activity_not_found():
    """Test signup for non-existent activity"""
    response = client.post("/activities/NonExistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_new_activity_signup():
    """Test signup for newly added activities"""
    # Test Basketball Team (sports)
    response = client.post("/activities/Basketball%20Team/signup?email=newplayer@mergington.edu")
    assert response.status_code == 200
    assert "Signed up newplayer@mergington.edu for Basketball Team" in response.json()["message"]

    # Test Art Club (artistic)
    response = client.post("/activities/Art%20Club/signup?email=artist@mergington.edu")
    assert response.status_code == 200
    assert "Signed up artist@mergington.edu for Art Club" in response.json()["message"]

    # Test Debate Club (intellectual)
    response = client.post("/activities/Debate%20Club/signup?email=debater@mergington.edu")
    assert response.status_code == 200
    assert "Signed up debater@mergington.edu for Debate Club" in response.json()["message"]