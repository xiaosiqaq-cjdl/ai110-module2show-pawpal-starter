import streamlit as st
from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption(
    "Pending tasks are considered by priority (high → medium → low), "
    "then by scheduled time. Tasks must fit within the remaining "
    "time budget. Tasks with fixed times cannot overlap; "
    "tasks without a set time remain flexible."
)

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

has_time = st.checkbox("Set a scheduled time")
scheduled_time = None

if has_time:
    scheduled_time = st.time_input("Scheduled time").strftime("%H:%M")

frequency = st.selectbox(
    "Repeat",
    ["once", "daily", "weekly"],
)

if st.button("Add task"):
    if task_title.strip():
        task = Task(
            task_title.strip(),
            int(duration),
            priority,
            scheduled_time=scheduled_time,
            frequency=frequency,
        )
        st.session_state.tasks.append(task)
    else:
        st.error("Please enter a task title.")

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table([
        {
            "Title": task.title,
            "Duration (minutes)": task.duration_minutes,
            "Priority": task.priority,
            "Scheduled time": task.scheduled_time or "Not set",
            "Completed": task.completed,
            "Repeat": task.frequency,
            "Due date": str(task.due_date),
        }
        for task in st.session_state.tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

if st.session_state.tasks:
    task_index = st.selectbox(
        "Choose a task to mark complete",
        options=range(len(st.session_state.tasks)),
        format_func=lambda i: (
            f"{i + 1}. {st.session_state.tasks[i].title}"
        ),
    )

    if st.button("Mark complete"):
        task = st.session_state.tasks[task_index]

        if task.completed:
            st.info("This task is already completed.")
        elif task.due_date > date.today():
            st.info(f"This task is next due on {task.due_date}.")
        else:
            task.mark_complete()
            st.rerun()

st.subheader("Build Schedule")
available_minutes = st.number_input(
    "Available time (minutes)",
    min_value=0,
    max_value=1440,
    value=60,
)

if st.button("Generate schedule"):
    owner = Owner(owner_name)
    pet = Pet(pet_name, species)

    for task in st.session_state.tasks:
        pet.add_task(task)

    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    plan = scheduler.build_daily_plan(int(available_minutes))
    pending_tasks = scheduler.filter_tasks(
        owner.get_all_tasks(),
        completed=False,
    )
    conflicts = scheduler.detect_conflicts(pending_tasks)

    if conflicts:
        with st.expander(
            f"⚠️ Found {len(conflicts)} overlapping task pairs",
            expanded=False,
        ):
            st.caption(
                "These conflicts are among all pending tasks. "
                "The generated plan skips overlapping tasks."
            )
            for first, second in conflicts:
                st.warning(
                    f"{first.title} ({first.scheduled_time}) overlaps with "
                    f"{second.title} ({second.scheduled_time})."
                )
    skipped_tasks = [
        task for task in pending_tasks
        if task not in plan
    ]

    if skipped_tasks:
        with st.expander(f"Tasks not selected ({len(skipped_tasks)})"):
            st.caption(
                "These tasks exceeded the remaining time budget "
                "or overlapped with a selected task."
            )
            for task in skipped_tasks:
                st.write(
                    f"- {task.title} | {task.duration_minutes} minutes | "
                    f"{task.priority} | {task.scheduled_time or 'Not set'}"
                )
    if plan:
        st.write(f"Care plan for {pet.name}:")
        st.caption(
            "Pending tasks are considered by priority (high → medium → low), "
            "then by scheduled time. Each task is included if it fits "
            "within the remaining time budget."
        )
        st.table([
            {
                "Task": task.title,
                "Minutes": task.duration_minutes,
                "Priority": task.priority,
                "Scheduled time": task.scheduled_time or "Not set",
            }
            for task in plan
        ])

        total_minutes = sum(task.duration_minutes for task in plan)
        st.success(
            f"Planned {total_minutes} of {available_minutes} available minutes."
        )
    else:
        st.info("No pending tasks fit within the available time.")
