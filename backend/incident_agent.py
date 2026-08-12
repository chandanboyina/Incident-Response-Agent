import os

from dotenv import load_dotenv
from hindsight_client import Hindsight

from llm_service import analyze_incident


load_dotenv()

hindsight = Hindsight(
    base_url=os.getenv("HINDSIGHT_API_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY"),
)

BANK_ID = os.getenv(
    "HINDSIGHT_BANK_ID",
    "incidentmind"
)


def recall_incidents(incident):

    results = hindsight.recall(
        bank_id=BANK_ID,
        query=f"""
        Find previous production incidents similar to this incident.

        Current incident:
        {incident}

        Focus on:
        - similar symptoms
        - root causes
        - successful resolutions
        - failed remediation attempts
        - engineer feedback
        """,
        budget="low",
        max_tokens=1500,
    )

    return results.results


def investigate_incident(incident):

    print("\n[1] Recalling previous incidents...")

    memories = recall_incidents(incident)

    print(
        f"[2] Found {len(memories)} relevant memories."
    )

    print("\n[3] Asking IncidentMind to analyze...")

    analysis = analyze_incident(
        incident,
        memories,
    )

    return {
        "analysis": analysis,
        "memories": [
            {
                "type": memory.type,
                "text": memory.text,
            }
            for memory in memories
        ],
    }


def retain_resolution(
    incident,
    root_cause,
    attempted_actions,
    successful_action,
    outcome,
    engineer_feedback,
):

    memory = f"""
    Production Incident Resolution

    Incident:
    {incident}

    Root Cause:
    {root_cause}

    Attempted Actions:
    {attempted_actions}

    Successful Action:
    {successful_action}

    Outcome:
    {outcome}

    Engineer Feedback:
    {engineer_feedback}
    """

    hindsight.retain(
        bank_id=BANK_ID,
        content=memory,
        context="production incident resolution and operational learning",
    )

    print("\n[Memory] Resolution stored in Hindsight.")