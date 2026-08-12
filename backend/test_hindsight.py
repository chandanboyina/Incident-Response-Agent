import os

from dotenv import load_dotenv
from hindsight_client import Hindsight


load_dotenv()

HINDSIGHT_API_URL = os.getenv("HINDSIGHT_API_URL")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "incidentmind")


def main():

    print("Connecting to Hindsight...")

    client = Hindsight(
        base_url=HINDSIGHT_API_URL,
        api_key=HINDSIGHT_API_KEY,
    )

    print("Connected successfully!")

    print("\n--- RETAINING INCIDENT ---")

    client.retain(
        bank_id=BANK_ID,
        content="""
        Production Incident INC-001.

        Service: Payment API
        Severity: P1

        Symptoms:
        The Payment API returned HTTP 503 errors.
        Database requests were timing out.
        Database connection pool utilization reached 100%.

        Investigation:
        Engineers first restarted the Payment API.
        The restart did not resolve the issue.

        Root Cause:
        PostgreSQL database connection pool exhaustion.

        Resolution:
        The database connection pool was increased from
        50 connections to 100 connections.

        Outcome:
        The Payment API recovered and HTTP 503 errors stopped.

        Engineer feedback:
        For future Payment API incidents involving HTTP 503
        errors and database connection timeouts, check database
        connection pool exhaustion before restarting the service.
        """,
        context="Production incident resolution",
    )

    print("Incident retained successfully!")

    print("\n--- RECALLING PREVIOUS INCIDENT ---")

    results = client.recall(
        bank_id=BANK_ID,
        query="""
        A Payment API is returning HTTP 503 errors.
        Database connections are timing out and the
        connection pool appears exhausted.

        Find previous similar incidents, their root causes,
        failed remediation attempts, successful fixes,
        and outcomes.
        """,
    )

    print("\nMEMORIES FOUND")
    print("=" * 60)

    for memory in results.results:
        print(f"\nType: {memory.type}")
        print(f"Memory: {memory.text}")

    print("\n" + "=" * 60)
    print("HINDSIGHT TEST COMPLETE")


if __name__ == "__main__":
    main()