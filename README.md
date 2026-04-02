# SmartAssist — Multi-Agent AI Productivity System

A multi-agent AI system built with **Google ADK** and **Gemini 2.5 Flash**, deployed on **Google Cloud Run**. Helps users manage tasks and notes through natural language conversation.

## Live Demo
**Cloud Run URL:** https://smart-assist-946542576224.europe-west1.run.app

## What it does
SmartAssist uses an orchestrator agent that routes user requests to specialist sub-agents:
- **task_agent** — create, list, complete, and delete tasks stored in SQLite
- **notes_agent** — save, retrieve, list, and delete notes stored in SQLite

## Architecture
- **Google ADK** — multi-agent orchestration and session management
- **Gemini 2.5 Flash** — inference via Vertex AI
- **Google Cloud Run** — serverless deployment (europe-west1)
- **SQLite** — persistent structured storage for tasks and notes
- **Google Cloud Build + Artifact Registry** — container build pipeline

## Project Structure
```
smart_assist/
├── agent.py          # ADK agent definitions (orchestrator + sub-agents)
├── tools.py          # SQLite tool functions for tasks and notes
├── requirements.txt  # Python dependencies
└── __init__.py       # Package entry point
```

## Try it
Open the live URL and type any of these:
```
Create a task: Review project report, due Friday, high priority
Show me all pending tasks
Mark task 1 as completed
Save a note titled "Ideas" with content "Use ADK for multi-agent workflows"
Show all my notes
```

## Deployment
Built using Google ADK CLI:
```bash
uvx --from google-adk==1.14.0 adk deploy cloud_run \
  --project=PROJECT_ID \
  --region=europe-west1 \
  --service_name=smart-assist \
  --with_ui
```

## Hackathon
Gen AI Academy — APAC Edition | Google Cloud x H2S
