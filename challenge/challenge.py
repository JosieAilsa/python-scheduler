import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Union, List


@dataclass
class HourlyTask:
    """A task to be done every hour, and backfilled if not up to date."""

    #: From when should this task start occurring?
    start_from: datetime

    #: Until when should this task occur?
    repeat_until: Union[datetime, None] = None

    #: What, if any, is the first time that has been done for this task?
    earliest_done: Union[datetime, None] = None

    #: What if any is the last (most recent) time that has been done for this
    #: task?
    latest_done: Union[datetime, None] = None

    @property
    def next_to_do(self) -> Union[datetime, None]:
        """Return the next datetime that needs doing."""
        #If no task for the most recent hour, return that hour 
        if self.latest_done == None: 
            #Abstract the below out into method into separate abstract helper class for getting the current time - this is not dry 
            now = datetime.utcnow()
            now_hour_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            last_hour_start = now_hour_start - timedelta(hours=1)
            self._next_to_do = last_hour_start
            return self._next_to_do 
        #Determine if backfilled task to do   
        if self.earliest_done != self.start_from: 
            next_todo = self.earliest_done - timedelta(hours=1)
            self._next_to_do = next_todo
            return self._next_to_do 
        #Otherwise, task is currently up to date
        return None

    def schedule(self, when: datetime) -> None:
        """Schedule this task at the 'when' time, update local time markers."""
        #If its not the current time, update the earliest done 
        now = datetime.utcnow()
        now_hour_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        last_hour_start = now_hour_start - timedelta(hours=1)
        #Set to latest done if when matches most recent time 
        if when != last_hour_start:
            self.latest_done = when
            return None 
        #Else it's backfilled
        self.earliest_done = last_hour_start
        #If its the current hour update the lastest done 
        raise NotImplementedError("Fill me in!")


class Scheduler:
    """Schedule some work."""

    def __init__(self):
        """Initialise Scheduler."""
        self.task_store = []

    def register_task(self, task: HourlyTask) -> None:
        """Add a task to the local store of tasks known about."""
        self.task_store.append(task)

    def register_tasks(self, task_list: List[HourlyTask]) -> None:
        """Add several tasks to the local store of tasks."""
        [self.register_task(task) for task in task_list]

    def get_tasks_to_do(self) -> List[HourlyTask]:
        """Get the list of tasks that need doing."""
        tasks = self.task_store
        tasks_todo = []
        for task in tasks:
            if task.next_to_do != None:
                tasks_todo.append(task.next_to_do)
        return [tasks_todo]

    def schedule_tasks(self) -> None:
        """Schedule the tasks.

        Tasks should be prioritised so that tasks with a recent "to do" date
        are done before any that need backfilling.
        """
        tasks = self.get_tasks_to_do()
        now = datetime.utcnow()
        now_hour_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        last_hour_start = now_hour_start - timedelta(hours=1)
        [task.schedule(last_hour_start) for task in tasks]


@dataclass
class Controller:
    """Use a Scheduler to repeatedly check and schedule tasks."""

    #: The scheduler that we are controlling
    scheduler: Scheduler

    #: How long to wait between each schedule check
    throttle_wait: timedelta

    #: Daemon mode?
    run_forever: bool = True

    #: Run this many times (if not in Daemon mode)
    run_iterations: int = 0

    def run(self):
        """Run scheduler"""
        while self.run_iterations or self.run_forever:
            before = datetime.utcnow()
            self.scheduler.schedule_tasks()
            self.run_iterations -= 1
            after = datetime.utcnow()
            elapsed = after - before
            wait = self.throttle_wait.total_seconds() - elapsed.total_seconds()
            time.sleep(max([0, wait]))

sch = Scheduler()
task1 = HourlyTask(start_from=datetime.utcnow())
sch.register_task(task1)
sch.get_tasks_to_do()
