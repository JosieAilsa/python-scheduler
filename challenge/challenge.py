import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from timeit import repeat
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
        #Abstract the below out into method into separate abstract helper class for getting the current time - this is not dry 
        formatted_time = FormattedDate(datetime.utcnow())
        last_hour_start = formatted_time.get_last_hour_start
        task_hour_start = FormattedDate(self.start_from).get_now_hour_start

        #If task to be done is in the current hour return none - as too late
        if task_hour_start > last_hour_start or last_hour_start == self.repeat_until: 
            return None

        #If the latest done doesn't exist or its less than current time, return current hour todo
        if self.latest_done == None or self.latest_done < last_hour_start: 
            self._next_to_do  = last_hour_start
            return self._next_to_do
  
        #If backdated, return previous hour to earliest done so far
        if self.earliest_done != None:
            next_todo = self.earliest_done + timedelta(hours=1)
            self._next_to_do = next_todo
            return self._next_to_do 
        #Otherwise, task is currently up to date
        return None

    

    def schedule(self, when: datetime) -> None:
        """Schedule this task at the 'when' time, update local time markers."""
        #If its not the current time, update the earliest done 
        formatted_time = FormattedDate(datetime.utcnow())
        last_hour_start = formatted_time.get_last_hour_start
      
        #Set to latest done if when matches most recent time 
        if when == last_hour_start:
            self.latest_done = when
            #If there is no earliest done set that to be earliest done 
            if self.earliest_done == None: 
                self.earliest_done = when
            return
        #Else it's backfilled
        self.earliest_done = when
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
                tasks_todo.append(task)
        return tasks_todo

    def schedule_tasks(self) -> None:
        """Schedule the tasks.

        Tasks should be prioritised so that tasks with a recent "to do" date
        are done before any that need backfilling.
        """
        tasks = self.get_sorted_tasks_to_do()
        formatted_time = FormattedDate( datetime.utcnow())
        last_hour_start = formatted_time.get_last_hour_start
        for task in tasks: 
            task.schedule(last_hour_start)
    
    #Getting sorted tasks 
    def get_sorted_tasks_to_do(self) -> List[HourlyTask]: 
        last_hour_start = FormattedDate(datetime.utcnow()).get_last_hour_start
        all_tasks_to_do = self.get_tasks_to_do()
        primary_tasks_to_do = []
        backdated_tasks_to_do = []
        for task in all_tasks_to_do: 
            if task.latest_done == None: 
                primary_tasks_to_do.append(task)
                continue
            if task.latest_done >= last_hour_start: 
                backdated_tasks_to_do.append(task)
                continue
            primary_tasks_to_do.append(task)

        backdated_tasks_to_do.sort()
        sorted_tasks = primary_tasks_to_do + backdated_tasks_to_do
        return sorted_tasks

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


@dataclass 
class FormattedDate: 
    """To create relevant date time in appropriate format """
    
    def __init__(self, given_date):
        self.given_date = given_date

    @property
    def get_now_hour_start(self) -> datetime: 
        self._get_now_hour_start = self.given_date.replace(minute=0, second=0, microsecond=0)
        return self._get_now_hour_start


    @property
    def get_last_hour_start (self) -> datetime: 
        self._get_last_hour_start = self.get_now_hour_start  - timedelta(hours=1)
        return self._get_last_hour_start



sch = Scheduler()

#dates
date1 = datetime(2022, 7, 31)
date2 = datetime(2022,8,1)
date3 = datetime(2022,8,2)

#hours
last_hour_start = FormattedDate(datetime.utcnow()).get_now_hour_start
now_hour_start = FormattedDate(datetime.utcnow()).get_last_hour_start
backdated_time_1 = FormattedDate(datetime.utcnow()).get_last_hour_start - timedelta(hours = 1)
backdated_time_2 = FormattedDate(datetime.utcnow()).get_last_hour_start - timedelta(hours = 2)

task_too_late = HourlyTask(start_from=datetime.utcnow())

#Should be first
task_with_todo = HourlyTask(start_from=date2)

#Should be second
unfinished_task_backdate =HourlyTask(start_from=date3, latest_done=backdated_time_1,earliest_done=backdated_time_2)

#Should be last
finished_task_with_backdate = HourlyTask(start_from=date1, latest_done=last_hour_start, earliest_done=backdated_time_1)

sch.register_tasks([task_with_todo,task_with_todo,finished_task_with_backdate])
sorted_todos = sch.get_sorted_tasks_to_do()

