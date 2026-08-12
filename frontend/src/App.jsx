import { useState } from "react";
import {
  Activity,
  Brain,
  CheckCircle2,
  AlertTriangle,
  Search,
  ShieldCheck,
  Clock,
  XCircle,
} from "lucide-react";

import "./App.css";


const API_URL = "http://127.0.0.1:8000";


function App() {

  const [service, setService] = useState("Payment API");
  const [severity, setSeverity] = useState("P1");

  const [symptoms, setSymptoms] = useState(
    "Payment API returning HTTP 503 errors. Database requests are timing out. Database connection utilization near 100%."
  );

  const [logs, setLogs] = useState(
    "ERROR: timeout waiting for database connection\nERROR: request failed with HTTP 503\nERROR: connection pool exhausted"
  );

  const [analysis, setAnalysis] = useState(null);
  
  const [memories, setMemories] = useState([]);

  const [loading, setLoading] = useState(false);

  const [resolved, setResolved] = useState(false);


  async function analyzeIncident() {

    setLoading(true);
    setAnalysis(null);
    setResolved(false);

    try {

      const response = await fetch(
        `${API_URL}/api/incidents/analyze`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            incident_id: "INC-002",
            service,
            severity,
            symptoms,
            logs,
          }),
        }
      );

      const data = await response.json();

      setAnalysis(data.analysis);
      setMemories(data.memories || []);

    } catch (error) {

      console.error(error);

      alert(
        "Unable to connect to IncidentMind backend."
      );

    } finally {

      setLoading(false);

    }
  }


  async function resolveIncident() {

    if (!analysis) return;

    try {

      const response = await fetch(
        `${API_URL}/api/incidents/resolve`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({

            incident:
              `Service: ${service}\nSymptoms: ${symptoms}\nLogs: ${logs}`,

            root_cause:
              analysis.root_cause,

            attempted_actions:
              analysis.failed_approaches,

            successful_action:
              analysis.recommended_actions[0],

            outcome:
              "Incident resolved successfully.",

            engineer_feedback:
              "Previous Hindsight experience provided a useful remediation path.",
          }),
        }
      );

      if (response.ok) {

        setResolved(true);

      }

    } catch (error) {

      console.error(error);

      alert(
        "Unable to store resolution."
      );

    }
  }


  return (

    <div className="app">

      {/* HEADER */}

      <header className="header">

        <div className="brand">

          <div className="brand-icon">
            <Brain size={25} />
          </div>

          <div>
            <h1>IncidentMind</h1>

            <span>
              AI Incident Response • Persistent Memory
            </span>
          </div>

        </div>


        <div className="system-status">

          <span className="status-dot"></span>

          Hindsight Connected

        </div>

      </header>


      {/* MAIN */}

      <main className="container">


        {/* HERO */}

        <section className="hero">

          <div>

            <div className="eyebrow">
              <Activity size={16} />
              MEMORY-POWERED INCIDENT RESPONSE
            </div>

            <h2>
              Resolve incidents using
              <span> operational memory.</span>
            </h2>

            <p>
              IncidentMind recalls previous incidents,
              successful fixes, failed approaches and
              engineer feedback to improve future responses.
            </p>

          </div>

        </section>


        {/* INCIDENT INPUT */}

        <section className="panel">

          <div className="panel-header">

            <div>

              <h3>Current Incident</h3>

              <p>
                Provide the symptoms and logs from the
                production incident.
              </p>

            </div>

            <div className="incident-id">
              INC-002
            </div>

          </div>


          <div className="form-grid">

            <div className="field">

              <label>Service</label>

              <input
                value={service}
                onChange={(e) =>
                  setService(e.target.value)
                }
              />

            </div>


            <div className="field">

              <label>Severity</label>

              <select
                value={severity}
                onChange={(e) =>
                  setSeverity(e.target.value)
                }
              >

                <option>P1</option>
                <option>P2</option>
                <option>P3</option>
                <option>P4</option>

              </select>

            </div>

          </div>


          <div className="field">

            <label>Symptoms</label>

            <textarea
              value={symptoms}
              onChange={(e) =>
                setSymptoms(e.target.value)
              }
            />

          </div>


          <div className="field">

            <label>Recent Logs</label>

            <textarea
              className="logs"
              value={logs}
              onChange={(e) =>
                setLogs(e.target.value)
              }
            />

          </div>


          <button
            className="primary-button"
            onClick={analyzeIncident}
            disabled={loading}
          >

            <Search size={18} />

            {loading
              ? "Analyzing..."
              : "Analyze Incident"}

          </button>

        </section>


        {/* MEMORY */}

        {analysis && (

          <section className="memory-panel">

            <div className="memory-header">

              <div className="memory-title">

                <Brain size={22} />

                <div>

                  <h3>Hindsight Memory</h3>

                  <p>
                    Previous operational experience
                    retrieved for this incident
                  </p>

                </div>

              </div>


              <div className="memory-count">

                <Search size={15} />

                {memories.length} memories recalled

              </div>

            </div>


            <div className="memory-grid">


              <div className="memory-card success">

                <div className="memory-card-icon">
                  <CheckCircle2 size={18} />
                </div>

                <div>

                  <span>
                    SUCCESSFUL EXPERIENCE
                  </span>

                  <strong>
                    INC-001
                  </strong>

                  <p>
                    Increasing the database
                    connection pool from
                    50 → 100 resolved the
                    incident.
                  </p>

                </div>

              </div>


              <div className="memory-card failed">

                <div className="memory-card-icon">
                  <XCircle size={18} />
                </div>

                <div>

                  <span>
                    FAILED EXPERIENCE
                  </span>

                  <strong>
                    INC-001
                  </strong>

                  <p>
                    Restarting the Payment API
                    did not resolve the issue.
                  </p>

                </div>

              </div>


              <div className="memory-card observation">

                <div className="memory-card-icon">
                  <Brain size={18} />
                </div>

                <div>

                  <span>
                    OBSERVATION
                  </span>

                  <strong>
                    Operational Protocol
                  </strong>

                  <p>
                    Check connection pool
                    exhaustion before restarting
                    the service.
                  </p>

                </div>

              </div>

            </div>

          </section>

        )}


        {/* ANALYSIS */}

        {analysis && (

          <section className="analysis-panel">


            <div className="analysis-header">

              <div>

                <div className="eyebrow">
                  <ShieldCheck size={15} />
                  INCIDENTMIND ANALYSIS
                </div>

                <h3>
                  Recommended response
                </h3>

              </div>


              <div className="confidence">

                <span>
                  CONFIDENCE
                </span>

                <strong>
                  {analysis.confidence}
                </strong>

              </div>

            </div>


            {/* ROOT CAUSE */}

            <div className="root-cause">

              <span>ROOT CAUSE</span>

              <h4>
                {analysis.root_cause}
              </h4>

            </div>


            <div className="analysis-grid">


              {/* EVIDENCE */}

              <div className="analysis-card">

                <div className="card-title">

                  <AlertTriangle size={18} />

                  Evidence

                </div>

                <ul>

                  {analysis.evidence.map(
                    (item, index) => (

                      <li key={index}>
                        {item}
                      </li>

                    )
                  )}

                </ul>

              </div>


              {/* PREVIOUS EXPERIENCE */}

              <div className="analysis-card">

                <div className="card-title">

                  <Brain size={18} />

                  Previous Experience

                </div>

                <ul>

                  {analysis.previous_experience.map(
                    (item, index) => (

                      <li key={index}>
                        {item}
                      </li>

                    )
                  )}

                </ul>

              </div>


              {/* FAILED */}

              <div className="analysis-card">

                <div className="card-title failed-title">

                  <XCircle size={18} />

                  Failed Approaches

                </div>

                <ul>

                  {analysis.failed_approaches.map(
                    (item, index) => (

                      <li key={index}>
                        {item}
                      </li>

                    )
                  )}

                </ul>

              </div>


              {/* RECOMMENDATIONS */}

              <div className="analysis-card recommendation">

                <div className="card-title">

                  <CheckCircle2 size={18} />

                  Recommended Actions

                </div>

                <ol>

                  {analysis.recommended_actions.map(
                    (item, index) => (

                      <li key={index}>
                        {item}
                      </li>

                    )
                  )}

                </ol>

              </div>

            </div>


            {/* UNCERTAINTY */}

            <div className="uncertainty">

              <div className="card-title">

                <Clock size={17} />

                What remains uncertain?

              </div>

              <ul>

                {analysis.uncertainty.map(
                  (item, index) => (

                    <li key={index}>
                      {item}
                    </li>

                  )
                )}

              </ul>

            </div>


            {/* RESOLVE */}

            {!resolved ? (

              <button
                className="resolve-button"
                onClick={resolveIncident}
              >

                <CheckCircle2 size={18} />

                Mark Incident Resolved & Learn

              </button>

            ) : (

              <div className="resolved">

                <CheckCircle2 size={20} />

                Resolution stored in Hindsight.
                IncidentMind has learned from this outcome.

              </div>

            )}

          </section>

        )}

      </main>


      <footer>

        IncidentMind • Powered by Hindsight Memory

      </footer>

    </div>

  );

}


export default App;