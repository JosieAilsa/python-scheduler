from datetime import datetime, timedelta
from unittest import TestCase
TestCase.maxDiff = None

from freezegun import freeze_time

from challenge.challenge import HourlyTask, Scheduler, Controller


class TestHourlyTask(TestCase):
    """Test the HourlyTask class."""

    def test_can_make_a_task(self):
        """Check we can make a task at all."""
        task = HourlyTask(start_from=datetime(2022, 8, 1))
        self.assertEqual(task.start_from, datetime(2022, 8, 1))


class TestScheduler(TestCase):
    """Test the Scheduler class."""

    def test_can_register_a_task(self):
        """Check a Scheduler can register an HourlyTask."""
        sch = Scheduler()
        task1 = HourlyTask(start_from=datetime.utcnow())
        sch.register_task(task1)
        self.assertEqual(sch.task_store, [task1])

    def test_can_find_any_tasks_to_do(self):
        """Check a Scheduler can correctly select tasks that need doing."""
        sch = Scheduler()
        with freeze_time(datetime(2022, 8, 1, 8, 15)):
            yesterday = datetime(2022, 7, 31)
            task_too_late = HourlyTask(start_from=datetime.utcnow())
            task_with_todo = HourlyTask(start_from=yesterday)
            task_done = HourlyTask(
                start_from=yesterday,
                latest_done=datetime(2022, 8, 1, 7)
            )
            sch.register_tasks([task_too_late, task_with_todo, task_done])
            todos = sch.get_tasks_to_do()
            self.assertEqual(todos, [task_with_todo])

    def test_can_find_todos_with_most_recent_first(self):
        """Check found tasks are in order of most recent -> most historic."""
        #Arrange 
        
        #Act 

        #Assert 


class TestController(TestCase):
    """Test the scheduler controller."""

    def test_can_run_scheduler_once(self):
        """Check can run a scheduler once."""
        sch = Scheduler()
        ctrl = Controller(
            scheduler=sch,
            throttle_wait=timedelta(seconds=1),
            run_forever=False,
            run_iterations=1
        )
        with freeze_time(datetime(2022, 8, 1, 8, 15)):
            yesterday = datetime(2022, 7, 31)
            task_with_todo = HourlyTask(start_from=yesterday)
            sch.register_task(task_with_todo)
            ctrl.run()
            self.assertEqual(
                task_with_todo.earliest_done,
                datetime(2022, 8, 1, 7)
            )

