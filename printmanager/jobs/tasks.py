from __future__ import absolute_import
from celery import shared_task
from datetime import datetime
from common import settings
from common.models import BaseTask

import logging
log = logging.getLogger(__name__)


@shared_task
def runWatcher(job_id=None, base=BaseTask):
    t=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log.info(f"Is Watcher task.[{t}]")
    if job_id is None :
        from watcher.wrapper import process
        process(t)
    else :
        from watcher.wrapper import process_job
        process_job(job_id,t)


@shared_task
def runGenerator(job_id=None, base=BaseTask):
    t=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log.info(f"Is generator task.[{t}]")
    if job_id is None :
        from generator.wrapper import process
        process(t)
    else :
        from generator.wrapper import process_job
        process_job(job_id,t)
