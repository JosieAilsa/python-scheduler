from datetime import datetime, timedelta
from tkinter.tix import Form
from unittest import TestCase
TestCase.maxDiff = None

from freezegun import freeze_time

from challenge.challenge import FormattedDate, HourlyTask, Scheduler, Controller


class TestHourlyTask(TestCase):
    """Test the HourlyTask class."""

    def test_can_make_a_task(self):
        """Check we can make a task at all."""
        task = HourlyTask(start_from=datetime(2022, 8, 1))
        self.assertEqual(task.start_from, datetime(2022, 8, 1))
    
    def test_can_register_backdated_task_correctly(self):
        """Check a task can correctly schedule itself, updating locals correctly."""       
        with freeze_time(datetime(2022, 8, 1, 8, 15)):
            yesterday = datetime(2022, 7, 31)
            last_hour_start = FormattedDate(datetime.utcnow()).get_last_hour_start
            backdated_time_1 = last_hour_start - timedelta(hours = 2)
            backdated_time_2 = last_hour_start - timedelta(hours = 3)
            task_1 = HourlyTask(start_from=yesterday) 
            task_1_after_sch = HourlyTask(start_from=yesterday, earliest_done=last_hour_start, latest_done=last_hour_start)  
            
            task_2 = HourlyTask(start_from=yesterday, earliest_done=backdated_time_1, latest_done=last_hour_start )
            task_2_after_sch = HourlyTask(start_from=yesterday, earliest_done=backdated_time_2, latest_done=last_hour_start)
        #Act        
            task_1.schedule(last_hour_start)
            task_2.schedule(backdated_time_2)
        #Assert
            self.assertEqual(task_1,task_1_after_sch)
            self.assertEqual(task_2,task_2_after_sch)
        

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
        sch = Scheduler()
        #Arrange: 
        with freeze_time(datetime(2022, 8, 1, 8, 15)):
            yesterday = datetime(2022, 7, 31)
            last_hour_start = FormattedDate(datetime.utcnow()).get_last_hour_start
            now_hour_start = FormattedDate(datetime.utcnow()).get_now_hour_start
            backdated_time_1 = last_hour_start - timedelta(hours = 1)
            backdated_time_2 = last_hour_start - timedelta(hours = 2)

            unfinished_task = HourlyTask(start_from=yesterday)        
            unfinished_task_with_backdate =HourlyTask(start_from=yesterday, latest_done=backdated_time_1,earliest_done=backdated_time_2)
            finished_task_with_backdate = HourlyTask(start_from=yesterday, latest_done=last_hour_start, earliest_done=backdated_time_1)
            finished_task = HourlyTask(start_from=yesterday, earliest_done=yesterday, latest_done=now_hour_start)

    #Act 
            sch.register_tasks([finished_task_with_backdate, unfinished_task, unfinished_task_with_backdate, finished_task])
            sorted_todos = sch.get_sorted_tasks_to_do()
            manually_sorted_tasks = [unfinished_task, unfinished_task_with_backdate,finished_task_with_backdate]
    #Assert 
        self.assertEqual(sorted_todos, manually_sorted_tasks)

    def test_does_not_add_finished_tasks_to_todo_list(self):
        """Complete tasks are not added to todo list."""
        sch = Scheduler()
        with freeze_time(datetime(2022, 8, 1, 8, 15)):
            yesterday = datetime(2022, 7, 31)
            # last_hour_start = FormattedDate(datetime.utcnow()).get_last_hour_start
            now_hour_start = FormattedDate(datetime.utcnow()).get_now_hour_start
            finished_task = HourlyTask(start_from=yesterday, earliest_done=yesterday, latest_done=now_hour_start)
        #Act 
            sch.register_tasks([finished_task])
            sorted_todos = sch.get_sorted_tasks_to_do()
            self.assertNotEqual(sorted_todos,[finished_task])

    def test_does_not_add_invalid_values_to_task_list(self): 
        """Invalid inputs for tasks throws an exception"""
        sch = Scheduler()
        with self.assertRaises(ValueError):
            sch.register_task("Hello")
       




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

