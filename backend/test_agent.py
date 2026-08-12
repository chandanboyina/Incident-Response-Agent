from incident_agent import (
    investigate_incident,
    retain_resolution,
)


incident = """
Incident ID: INC-002

Service: Payment API

Severity: P1

Symptoms:
The Payment API is returning HTTP 503 errors.
Database requests are timing out.
Database connection utilization appears to be near 100%.

Recent logs:
ERROR: timeout waiting for database connection
ERROR: request failed with HTTP 503
ERROR: connection pool exhausted
"""


print("=" * 70)
print("INCIDENTMIND - INCIDENT ANALYSIS")
print("=" * 70)

print("\nCURRENT INCIDENT:")
print(incident)

analysis = investigate_incident(incident)

print("\n" + "=" * 70)
print("AI RECOMMENDATION")
print("=" * 70)

print(analysis)


print("\n" + "=" * 70)
print("SIMULATING ENGINEER RESOLUTION")
print("=" * 70)

retain_resolution(
    incident=incident,

    root_cause="Database connection pool exhaustion",

    attempted_actions=[
        "Restart Payment API",
        "Check database connection utilization",
    ],

    successful_action=(
        "Increase database connection pool "
        "from 50 to 100 connections"
    ),

    outcome=(
        "HTTP 503 errors stopped and Payment API "
        "returned to normal operation"
    ),

    engineer_feedback=(
        "The previous Hindsight recommendation was correct. "
        "For similar incidents, check connection pool exhaustion "
        "before restarting the service."
    ),
)

print("\nLearning cycle complete.")