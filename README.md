# Job Application Agent — LangGraph Multi-Step AI Agent

A multi-step AI agent that analyzes job applications using LangGraph conditional routing. Paste a job description and resume and the agent extracts requirements, profiles the candidate, scores the fit, and takes a different path based on the result.

Built with LangGraph, LangChain, Anthropic Claude, and Pydantic.

---

## What It Does

The agent runs through a graph of 5 nodes and makes a real decision based on what it finds:

- Fit score 60 or above — takes the tailoring path
- Fit score below 60 — takes the upskilling path

This conditional routing is what makes it a LangGraph agent rather than a simple chain.

---

## Architecture

```
START
  ↓
Node 1: Extract job requirements
  ↓
Node 2: Extract resume profile
  ↓
Node 3: Analyze fit — calculates score 0 to 100
  ↓
fit score >= 60?
  ↓ Yes                    ↓ No
Node 4a: Tailoring        Node 4b: Upskilling
Resume edits              Skill gaps
Cover letter              Learning plan
Interview prep            Timeline
  ↓                        ↓
Node 5: Compile report
  ↓
END
```

---

## Sample Output

```
FIT SCORE: 82/100 — STRONG FIT

STRENGTHS:
  - Strong healthcare domain expertise with 4+ years in healthcare AI
  - Excellent match on core stack: Python, SQL, FastAPI, RAG, LangChain
  - Proven production deployment with SARIMAX models across 4 hospitals

SKILL GAPS:
  - No explicit MLOps tools mentioned (MLflow, model monitoring)
  - AWS and GCP not mentioned — strong in Azure only
  - HIPAA compliance not explicitly stated

RESUME TAILORING SUGGESTIONS:
  - Add: "Designed RAG pipelines for clinical document retrieval..."
  - Add: "Processed HL7 and FHIR-formatted EHR data at scale..."

COVER LETTER OPENING:
  As a Senior Healthcare AI Engineer at LA County DHS with 4+ years
  of specialized experience building production ML systems...

LIKELY INTERVIEW QUESTIONS:
  - Walk me through your most complex RAG pipeline implementation...
  - How have you ensured HIPAA compliance in your ML pipelines?
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| Agent framework | LangGraph |
| LLM integration | LangChain + LangChain-Anthropic |
| LLM | Anthropic Claude (claude-haiku-4-5) |
| Structured outputs | Pydantic |
| Language | Python 3.13 |

---

## Key Concepts Demonstrated

**LangGraph State** — a shared TypedDict that travels through every node. Starts with job description and resume. Each node adds its piece. By the end every field is populated.

**Nodes** — plain Python functions. Each one does one job, reads from state, and writes back only the fields it changed.

**Conditional Edges** — after the fit analysis node, the graph checks the fit score and routes to a completely different path. This is what makes LangGraph more powerful than a simple chain.

---

## Project Structure

```
job-application-agent/
├── schemas.py        # Pydantic models + AgentState definition
├── nodes.py          # All node functions + routing function
├── graph.py          # Graph construction and compilation
├── test_agent.py     # Sample JD and resume to run the agent
├── requirements.txt
├── .env              # API key (not tracked)
└── .gitignore
```

---

## How to Run It

### 1. Clone the repo
```bash
git clone https://github.com/uvstharun/job-application-agent.git
cd job-application-agent
```

### 2. Set up environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Add your Anthropic API key
```bash
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

### 4. Run the agent
```bash
python test_agent.py
```

### 5. Use your own data
Open `test_agent.py` and replace `JOB_DESCRIPTION` and `RESUME` with your own content. Run again.

---

## Why LangGraph Instead of a Simple Chain

A LangChain chain always runs every step sequentially. It cannot take a different path based on what it discovers.

LangGraph introduces conditional routing — the agent analyzes the fit score and decides which path to take. A weak candidate gets an upskilling plan. A strong candidate gets tailoring advice. The right output for the right situation.

This is the same pattern used in production agentic systems — clinical triage, customer support routing, document processing pipelines — wherever the next step depends on what the previous step found.

---

## Author

**Vishnu Sai** — Data Scientist | Healthcare AI
[LinkedIn](https://www.linkedin.com/in/vishnusai29) · [GitHub](https://github.com/uvstharun)