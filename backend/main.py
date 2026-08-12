from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from incident_agent import (
    investigate_incident,
    retain_resolution,
)


app = FastAPI(
    title="IncidentMind",
    description="AI Incident Response Agent with Hindsight Memory",
    version="1.0.0",
)


# Allow the React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IncidentRequest(BaseModel):
    incident_id: str
    service: str
    severity: str
    symptoms: str
    logs: str = ""


class ResolutionRequest(BaseModel):
    incident: str
    root_cause: str
    attempted_actions: list[str]
    successful_action: str
    outcome: str
    engineer_feedback: str


@app.get("/")
def root():
    return {
        "name": "IncidentMind",
        "status": "running",
        "description": "AI Incident Response Agent with Hindsight Memory",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/api/incidents/analyze")
def analyze_incident(request: IncidentRequest):

    incident = f"""
Incident ID: {request.incident_id}

Service: {request.service}

Severity: {request.severity}

Symptoms:
{request.symptoms}

Logs:
{request.logs}
"""

    result = investigate_incident(incident)

    return {
        "incident_id": request.incident_id,
        "analysis": result["analysis"],
        "memories": result["memories"],
        "memory_count": len(result["memories"]),
    }


@app.post("/api/incidents/resolve")
def resolve_incident(request: ResolutionRequest):

    retain_resolution(
        incident=request.incident,
        root_cause=request.root_cause,
        attempted_actions=request.attempted_actions,
        successful_action=request.successful_action,
        outcome=request.outcome,
        engineer_feedback=request.engineer_feedback,
    )

    return {
        "status": "success",
        "message": "Incident resolution stored in Hindsight memory.",
    }