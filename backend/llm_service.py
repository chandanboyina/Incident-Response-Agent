import os
import json

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are IncidentMind, an AI production incident response assistant.

Analyze the current incident using relevant operational memories.

Use previous experiences intelligently:
- successful fixes
- failed fixes
- previous root causes
- observations
- engineer feedback

Do not blindly copy a previous solution.
Compare the previous incident with the current evidence.

Return ONLY valid JSON matching the requested schema.
"""


INCIDENT_SCHEMA = {
    "type": "object",
    "properties": {
        "root_cause": {
            "type": "string"
        },
        "evidence": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "previous_experience": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "failed_approaches": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "recommended_actions": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "uncertainty": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "confidence": {
            "type": "string",
            "enum": [
                "Low",
                "Medium",
                "High"
            ]
        }
    },
    "required": [
        "root_cause",
        "evidence",
        "previous_experience",
        "failed_approaches",
        "recommended_actions",
        "uncertainty",
        "confidence"
    ],
    "additionalProperties": False
}


def analyze_incident(incident, memories):

    memory_text = "\n\n".join(
        [
            f"[{memory.type}] {memory.text}"
            for memory in memories
        ]
    )

    user_prompt = f"""
CURRENT INCIDENT:

{incident}


RELEVANT HINDSIGHT MEMORIES:

{memory_text}


Analyze the current incident.

Return:
- most likely root cause
- evidence
- relevant previous experiences
- failed approaches from previous incidents
- recommended actions
- uncertainty
- confidence

Only use previous memories when they are relevant to the current incident.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],

        temperature=0.2,

        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "incident_analysis",
                "strict": True,
                "schema": INCIDENT_SCHEMA,
            },
        },
    )

    content = response.choices[0].message.content

    return json.loads(content)