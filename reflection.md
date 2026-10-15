# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- I planned four main classes for PawPal+: Owner, Pet, Task, and Scheduler.

- The Owner class stores the owner's name, preferences, and pets. It can add pets and provide access to all tasks belonging to those pets. The Pet class stores basic information such as the pet's name and species, as well as a list of care tasks. It can add and manage tasks.

- The Task class represents one pet-care activity. It stores information such as the task title, duration, priority, scheduled time, frequency, and completion status. The Scheduler class is responsible for organizing the tasks and building a daily plan. It retrieves tasks through the Owner class, sorts and filters them, checks for conflicts, and creates a schedule based on the available time and task priorities.

- In this design, one Owner can have multiple Pets, and each Pet can have multiple Tasks. The Scheduler works with the Owner's collection of pets and tasks, but it does not directly own those objects.

**b. Design changes**

- I added a due_date attribute when implementing recurring tasks. At first, a task only had a frequency, but that was not enough to tell whether it should appear in today's plan. Adding a due date allowed the scheduler to exclude future tasks.

- I also changed the scheduler from only displaying conflict warnings to skipping tasks that overlap with an already selected task. This made the generated plan more useful.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- My scheduler considers completion status, due date, priority, scheduled time, and available minutes. It first excludes completed tasks and tasks that are not due yet. It then considers tasks by priority, from high to low, and by scheduled time within each priority level.

- I put priority first because important care tasks should be considered before less urgent ones. Each selected task must also fit within the remaining time budget and must not overlap with another selected fixed-time task. Owner preferences are stored in the Owner class, but they are not currently used in scheduling.
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- My scheduler uses a greedy approach: it considers higher-priority tasks first and adds each task if it fits the remaining time and does not conflict with a selected task. It does not compare every possible combination, so it may leave some time unused even when another combination could fit more tasks.

- I think this is reasonable for a basic pet-care planner because important tasks should come first, and the logic is easy to understand and verify. The tradeoff is that it does not always produce the most efficient use of the available time.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- I used ChatGPT to help with class design, scheduling logic, Streamlit integration, debugging, and automated tests. The most helpful approach was asking for one small change at a time, including where to put the code and how to check the result.

- When something did not work, I shared my current code or a screenshot of the error. This was more useful than asking general questions because we could focus on the actual problem. I mostly continued in one conversation rather than using separate chats for each phase. This kept the context together, but the conversation became long and sometimes made it harder to track the latest changes.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- One example was the recurring-task completion behavior. At first, clicking Mark complete seemed to do nothing because Completed stayed False. After checking the due date, I realized that each click was moving the task forward another day. We added a check in the UI to prevent completing a task that was already scheduled for a future date.

- I verified this by adding a new daily task, completing it once, and checking that its due date moved to tomorrow. Clicking again then displayed the next due date instead of moving it forward again.

- I also questioned whether the AI was suggesting more features than the assignment needed. I asked to stop adding features and return to the original requirements. This reminded me that I needed to make decisions about scope instead of accepting every suggestion.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I wrote seven automated tests covering:

- Daily tasks move their due date forward by one day after completion.
- Back-to-back tasks are not treated as conflicts.
- A higher-priority task is selected over a conflicting lower-priority task.
- A task that exceeds the time budget is skipped so a shorter task can still be selected.
- Completed tasks are excluded from the plan.
- An owner with no tasks receives an empty plan.
- A zero-minute budget produces an empty plan.

These tests were important because a schedule can look correct in the UI while still handling edge cases incorrectly. For example, a task ending at 09:20 should not conflict with a task starting at 09:20.

All seven tests passed using `python -m unittest test_scheduler -v`. I also manually checked task creation, schedule generation, conflict warnings, completion status, and recurring-task dates in the Streamlit app.
**b. Confidence**

- How confident are you that your scheduler works correctly?
- I would rate my confidence as 3 out of 5. The behaviors covered by the tests work, but the tests do not cover every possible situation.

 - If I had more time, I would add direct tests for sorting, adding tasks to a pet, weekly recurrence, multiple pets, and future or overdue tasks. I would also check conflicts between tasks on different dates, since the current conflict detection compares clock times without considering dates.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am most satisfied that the backend classes now work with the Streamlit interface. Seeing tasks appear in a table and then become part of a generated plan helped me understand how Owner, Pet, Task, and Scheduler work together.

Building and checking one small part at a time also worked well. When something broke, it was easier to identify the cause than if I had copied a large amount of code at once.

**b. What you would improve**

I would improve recurring tasks by keeping the completed occurrence and creating a new task for the next date, rather than only changing the existing task's due date. This would preserve completion history and follow the assignment's recurrence instructions more closely.

I would also improve the UI explanations. For example, future tasks can appear under Tasks not selected, but the current explanation only mentions time limits and conflicts. A clear message after completing a recurring task would also make the date change easier to notice.

Before adding more features, I would finish checking the required UML files, multi-pet demonstration, and remaining test coverage.

**c. Key takeaway**

I learned that working with AI still requires me to understand the design, check the results, and control the scope. AI helped me turn ideas into code, but some suggestions needed debugging or clearer explanations.

A working page and passing tests are useful evidence, but they do not automatically mean every requirement has been met. I still need to compare the final implementation with the assignment and decide what needs to be corrected.
