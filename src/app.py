"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Team training and matches for students who love soccer",
        "schedule": "Monday, Thursday, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["nina@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Practice shooting, defense, and teamwork for basketball players",
        "schedule": "Tuesday, Friday, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["james@mergington.edu"]
    },
    "Art Workshop": {
        "description": "Explore drawing, painting, and mixed-media artwork",
        "schedule": "Wednesday, 3:30 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["maya@mergington.edu"]
    },
    "Theater Club": {
        "description": "Acting, stagecraft, and production for school plays",
        "schedule": "Thursday, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["alex@mergington.edu"]
    },
    "Debate Team": {
        "description": "Learn argumentation, public speaking, and competition strategy",
        "schedule": "Tuesday, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["leah@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments and science project design",
        "schedule": "Monday, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["noah@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already registered for this activity")

    # Validate capacity
    if len(activity["participants"]) >= activity.get("max_participants", float("inf")):
        raise HTTPException(status_code=400, detail="Activity is already full")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
