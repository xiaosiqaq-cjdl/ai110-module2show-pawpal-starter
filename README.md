# PawPal+ (Module 2 Project)

PawPal+ is a Python and Streamlit pet-care planner. An owner can add care tasks, set their duration and priority, optionally assign a time, and generate a daily plan within a time budget.

## Features

- Enter an owner's name and a pet's name and species.
- Add tasks with a duration, priority, optional scheduled time, and repeat frequency.
- Generate a plan from pending tasks due today or earlier.
- Detect overlapping fixed-time tasks and skip conflicts when building a plan.
- Mark one-time tasks complete and advance daily or weekly tasks to their next due date.
- Display current tasks, selected tasks, conflict warnings, and tasks not selected.

## Implementation Summary

The backend is in `pawpal_system.py`:

- **Task** stores a title, duration, priority, scheduled time, frequency, due date, and completion status.
- **Pet** stores basic pet information and its tasks.
- **Owner** stores pets and combines their tasks through `get_all_tasks()`.
- **Scheduler** retrieves tasks through the owner, filters and sorts them, detects conflicts, and builds a plan.

The backend supports multiple pets through `Owner.pets`. The current Streamlit interface uses one pet and stores Task objects in `st.session_state.tasks`. It creates the Owner and Pet when a plan is generated.

## Setup and Run

From the project directory, using Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
python -m streamlit run app.py
```

On macOS/Linux, activate the environment with `source .venv/bin/activate`.

## Sample Output

The following excerpt is from running the current `python main.py`:

```text
Pending high-priority tasks:
Give medicine
Daily plan (10 minutes available):
Give medicine: 5 minutes
Time conflicts:
Walk Mochi overlaps with Groom Mochi
Sorted tasks:
high | 09:00 | Give medicine
high | None | Feed Mochi
low | 08:00 | Brush Mochi
```

This demonstrates that priority is considered before time: the low-priority 08:00 task appears after the high-priority tasks. The CLI also prints task completion states.

## Testing PawPal+

Install the dependencies, then run:

```powershell
python -m pytest
```

The tests use Python's `unittest.TestCase`, which pytest can also discover. They can be run directly without pytest:

```powershell
python -m unittest test_scheduler -v
```

The seven tests cover:

1. Daily recurrence advances the due date by one day and keeps the task pending.
2. Back-to-back tasks do not conflict.
3. A higher-priority task is selected over a conflicting lower-priority task.
4. A task that exceeds the budget is skipped, allowing a shorter task to be selected.
5. Completed tasks are excluded.
6. An owner with no tasks receives an empty plan.
7. A zero-minute budget produces an empty plan.

Verified output from the direct unittest run:

```text
----------------------------------------------------------------------
Ran 7 tests in 0.001s

OK
```

This is unittest output, not pytest output. A successful pytest transcript still needs to be captured in the project environment for the assignment's requested evidence.

**Confidence level: 3/5 stars.** The tested behaviors pass, but weekly recurrence, direct sorting, task addition, multiple-pet planning, and date-related edge cases need additional automated checks.

## Smarter Scheduling

| Feature | Method(s) | Behavior |
|---------|-----------|----------|
| Task sorting | `Scheduler.sort_by_priority_and_time()` | High, medium, then low priority; within each priority, sort by HH:MM time. Missing times use 23:59 as the sorting key. |
| Filtering | `Scheduler.filter_tasks()` | Filter by priority and/or completion status. |
| Daily plan | `Scheduler.build_daily_plan()` | Consider pending tasks due today or earlier; select tasks that fit the remaining budget without fixed-time conflicts. |
| Conflict detection | `Scheduler.detect_conflicts()` | Compare start times and durations; touching endpoints do not overlap. |
| Recurring tasks | `Task.mark_complete()` | Advance the existing task's due date by one day or seven days; one-time tasks become completed. |

The planner uses a greedy approach. It considers tasks in priority order and does not search every possible combination. Tasks without a set time consume the time budget but do not receive a specific start time.

## Demo Walkthrough

1. Start the Streamlit app and enter the owner and pet information.
2. Enter a task title, duration, and priority. Optionally check **Set a scheduled time**.
3. Choose **once**, **daily**, or **weekly** under **Repeat**, then click **Add task**.
4. Review the current task table, including the due date and completion state.
5. Add another task with an overlapping time to demonstrate conflict detection.
6. Set **Available time (minutes)** and click **Generate schedule**.
7. Review the selected plan and total minutes. Expand the conflict and unselected-task sections as needed.
8. Select a task and click **Mark complete**. A one-time task becomes completed. A recurring task moves to its next date and remains pending.
9. Clicking complete on a future task shows its next due date instead of advancing it again.

The UI uses Streamlit's `st.table`, `st.expander`, `st.warning`, `st.info`, and `st.success` for its output.

## Current Limitations

- Recurrence updates the existing task instead of creating a new occurrence object. It does not preserve completion history.
- The Streamlit interface does not yet manage multiple pets, edit tasks, or save data between browser sessions.
- Owner preferences are stored but are not used by the scheduling algorithm.
- Conflict detection compares clock times without considering due dates. UI conflict warnings currently include future pending tasks.
- The unselected-task message mentions budget and conflicts, but a future due date can also explain exclusion.
- Fixed-time tasks are checked for overlap; flexible tasks are not placed into actual free time slots.
- The current CLI demo uses one pet. The supplied files do not include the required draft and final UML sources.

