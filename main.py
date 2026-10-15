from pawpal_system import Task, Pet, Owner, Scheduler


def main():
    owner = Owner("Lucia")
    pet = Pet("Mochi", "Cat")
    task = Task("Feed Mochi", 10, priority="high")

    pet.add_task(task)
    owner.add_pet(pet)

    pet.add_task(Task("Brush Mochi", 15, "low", "08:00"))
    pet.add_task(Task("Give medicine", 5, "high", "09:00"))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_priority_and_time(owner.get_all_tasks())

    task.mark_complete()

    pending_high = scheduler.filter_tasks(
        owner.get_all_tasks(),
        priority="high",
        completed=False,
    )

    print("Pending high-priority tasks:")
    for item in pending_high:
        print(item.title)

    plan = scheduler.build_daily_plan(10)

    print("Daily plan (10 minutes available):")
    for item in plan:
        print(f"{item.title}: {item.duration_minutes} minutes")

    conflict_tasks = [
        Task("Walk Mochi", 20, "medium", "09:00"),
        Task("Groom Mochi", 15, "low", "09:10"),
        Task("Clean bowl", 5, "low", "09:25"),
    ]

    conflicts = scheduler.detect_conflicts(conflict_tasks)

    print("Time conflicts:")
    for first, second in conflicts:
        print(f"{first.title} overlaps with {second.title}")
        
    print("Sorted tasks:")
    for task in sorted_tasks:
        print(f"{task.priority} | {task.scheduled_time} | {task.title}")

    for item in owner.get_all_tasks():
        print(f"{item.title}: {item.duration_minutes} minutes")
        print(f"Completed: {item.completed}")

        item.mark_complete()
        print(f"Completed after update: {item.completed}")


if __name__ == "__main__":
    main()