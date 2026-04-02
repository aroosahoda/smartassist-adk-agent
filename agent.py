import os
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent
from smart_assist.tools import (
    create_task, list_tasks, complete_task, delete_task,
    save_note, list_notes, get_note, delete_note
)

load_dotenv()
model_name = os.getenv("MODEL", "gemini-2.5-flash")

# ── Sub-agent 1: Task Manager ────────────────────────────────────────────────
task_agent = Agent(
    name="task_agent",
    model=model_name,
    description="Manages the user's tasks. Can create, list, complete, and delete tasks stored in a database.",
    instruction="""
    You are a task management assistant. You help users manage their to-do list.
    Use the available tools to:
    - Create tasks with optional due dates and priority (low/medium/high)
    - List tasks by status (pending, completed, all)
    - Mark tasks as completed using their ID
    - Delete tasks using their ID
    Always confirm actions taken and show the user what was done.
    """,
    tools=[create_task, list_tasks, complete_task, delete_task],
)

# ── Sub-agent 2: Notes Manager ───────────────────────────────────────────────
notes_agent = Agent(
    name="notes_agent",
    model=model_name,
    description="Manages the user's notes. Can save, list, retrieve, and delete notes stored in a database.",
    instruction="""
    You are a notes management assistant. You help users capture and retrieve information.
    Use the available tools to:
    - Save new notes with a title and content
    - List all saved notes
    - Retrieve full content of a specific note by ID
    - Delete notes by ID
    Always confirm actions and summarize what was saved or retrieved.
    """,
    tools=[save_note, list_notes, get_note, delete_note],
)

# ── Root orchestrator agent ───────────────────────────────────────────────────
root_agent = Agent(
    name="smartassist_orchestrator",
    model=model_name,
    description="The primary SmartAssist orchestrator. Routes user requests to the task or notes agent.",
    instruction="""
    You are SmartAssist, a personal productivity AI assistant.
    You help users manage their tasks, notes, and schedules.

    You coordinate two specialist agents:
    1. task_agent — for anything related to tasks, to-dos, or action items
    2. notes_agent — for saving, finding, or retrieving notes and information

    When the user asks about:
    - Tasks, to-dos, action items, reminders → transfer to task_agent
    - Notes, information, saving content, looking something up → transfer to notes_agent
    - Multiple things at once → handle them in sequence, transferring to each agent

    Always greet the user warmly and confirm what you have done after each action.
    If unsure which agent to use, ask the user to clarify.
    """,
    sub_agents=[task_agent, notes_agent],
)
