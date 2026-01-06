#from jobs.models import JobsStatus


import logging

from jobs.models import JobStatusNames, JobType, JobsStatus

log = logging.getLogger(__name__)

def get_jobtype(name):
    return JobType.objects.get(jobtype_name=name)

def get_jobstatus(name):
    return JobStatusNames.objects.get(jobstatus_name=name)

def save_job_task(job_id, task_id):
    job = JobsStatus.objects.get(jobid=job_id)
    log.info("save_job_task [" + str(job_id) + "] [" +task_id + "]")
    job.task_id = task_id
    job.save()