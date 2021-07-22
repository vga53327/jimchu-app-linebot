from datetime import datetime
import time

from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.background import BackgroundScheduler


def tick():
    print('Tick! The time is: %s' % datetime.now())


# def listener(event):
#     if not event.exception:
#         job = scheduler.get_job(event.job_id)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    # scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.add_job(tick, 'interval', seconds=5)
    scheduler.start()

    try:
        print("hello")
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
