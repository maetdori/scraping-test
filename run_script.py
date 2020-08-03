# -*- coding:utf-8 -*-
import logging
import subprocess
from time import gmtime, strftime
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def main():
   command = "python3 main.py"
   subprocess.call(command.split())

if __name__ == "__main__":
   logging.basicConfig(level=logging.INFO)
   sched = BlockingScheduler()
   sched.add_job(main, 'cron', hour="13", minute="38")
   sched.start()