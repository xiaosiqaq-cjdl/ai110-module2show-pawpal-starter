import unittest
from datetime import date, timedelta
from pawpal_system import Task,Pet, Owner, Scheduler


class TestScheduler(unittest.TestCase):
    def test_daily_task_moves_to_next_day(self):
        task = Task(
            "Feed",
            10,
            frequency="daily",
            due_date=date.today(),
        )

        task.mark_complete()

        self.assertEqual(
            task.due_date,
            date.today() + timedelta(days=1),
        )
        self.assertFalse(task.completed)

        
    def test_back_to_back_tasks_do_not_conflict(self):
        scheduler = Scheduler(Owner("Lucia"))
        tasks = [
            Task("Walk", 20, "high", "09:00"),
            Task("Feed", 10, "medium", "09:20"),
        ]

        self.assertEqual(scheduler.detect_conflicts(tasks), [])

    def test_plan_skips_lower_priority_conflict(self):
        owner = Owner("Lucia")
        pet = Pet("Mochi", "cat")

        low = Task("Brush", 15, "low", "09:00")
        high = Task("Medicine", 5, "high", "09:05")

        pet.add_task(low)
        pet.add_task(high)
        owner.add_pet(pet)

        scheduler = Scheduler(owner)
        plan = scheduler.build_daily_plan(60)

        self.assertEqual(plan, [high])


    def test_plan_skips_long_task_and_selects_short_task(self):
        owner = Owner("Lucia")
        pet = Pet("Mochi", "cat")

        long_task = Task("Long walk", 30, "high")
        short_task = Task("Feed", 10, "medium")

        pet.add_task(long_task)
        pet.add_task(short_task)
        owner.add_pet(pet)

        scheduler = Scheduler(owner)
        plan = scheduler.build_daily_plan(10)

        self.assertEqual(plan, [short_task])

    def test_plan_excludes_completed_tasks(self):
        owner = Owner("Lucia")
        pet = Pet("Mochi", "cat")

        completed_task = Task("Feed", 10, "high")
        completed_task.mark_complete()
        pending_task = Task("Brush", 15, "low")

        pet.add_task(completed_task)
        pet.add_task(pending_task)
        owner.add_pet(pet)

        scheduler = Scheduler(owner)
        plan = scheduler.build_daily_plan(60)

        self.assertEqual(plan, [pending_task])

    def test_empty_owner_returns_empty_plan(self):
        scheduler = Scheduler(Owner("Lucia"))

        self.assertEqual(scheduler.build_daily_plan(60), [])

    def test_zero_budget_returns_empty_plan(self):
        owner = Owner("Lucia")
        pet = Pet("Mochi", "cat")
        pet.add_task(Task("Feed", 10, "high"))
        owner.add_pet(pet)

        scheduler = Scheduler(owner)

        self.assertEqual(scheduler.build_daily_plan(0), [])

if __name__ == "__main__":
    unittest.main()