from datetime import date, timedelta

class Task:
    def __init__(
        self,
        title,
        duration_minutes,
        priority="medium",
        scheduled_time=None,
        frequency="once",
        due_date=None,
    ):
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.scheduled_time = scheduled_time
        self.frequency = frequency
        self.due_date = due_date if due_date is not None else date.today()
        self.completed = False

    def mark_complete(self):
        if self.frequency == "daily":
            self.due_date += timedelta(days=1)
        elif self.frequency == "weekly":
            self.due_date += timedelta(days=7)
        else:
            self.completed = True


class Pet:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)


class Owner:
    def __init__(self, name, preferences=None):
        self.name = name
        self.preferences = preferences if preferences is not None else {}
        self.pets = []

    def add_pet(self, pet):
        self.pets.append(pet)

    def get_all_tasks(self):
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks

class Scheduler:
    def __init__(self, owner):
        self.owner = owner

    def sort_by_priority_and_time(self, tasks):
        priority_order = {"high": 0, "medium": 1, "low": 2}

        return sorted(
            tasks,
            key=lambda task: (
                priority_order[task.priority],
                task.scheduled_time or "23:59",
            ),
        )

    def filter_tasks(self, tasks, priority=None, completed=None):
        result = []

        for task in tasks:
            if priority is not None and task.priority != priority:
                continue

            if completed is not None and task.completed != completed:
                continue

            result.append(task)

        return result

    def build_daily_plan(self, available_minutes):
        pending_tasks = self.filter_tasks(
            self.owner.get_all_tasks(),
            completed=False,
        )
        pending_tasks = [
            task for task in pending_tasks
            if task.due_date <= date.today()
        ]
        sorted_tasks = self.sort_by_priority_and_time(pending_tasks)

        plan = []
        remaining_minutes = available_minutes

        for task in sorted_tasks:
            if task.duration_minutes > remaining_minutes:
                continue

            if self.detect_conflicts(plan + [task]):
                continue

            plan.append(task)
            remaining_minutes -= task.duration_minutes

        return plan

    def detect_conflicts(self, tasks):
        timed_tasks = [
            task for task in tasks
            if task.scheduled_time is not None
        ]
        timed_tasks.sort(key=lambda task: task.scheduled_time)

        conflicts = []

        for i, first in enumerate(timed_tasks):
            hours, minutes = map(int, first.scheduled_time.split(":"))
            first_start = hours * 60 + minutes
            first_end = first_start + first.duration_minutes

            for second in timed_tasks[i + 1:]:
                hours, minutes = map(int, second.scheduled_time.split(":"))
                second_start = hours * 60 + minutes

                if second_start >= first_end:
                    break

                conflicts.append((first, second))

        return conflicts