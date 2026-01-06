

import uuid
import logging
from jobs.models import ContentStore,JobsStatus,  PrintJobs, SessionKeyValueLog
from common.functions import get_jobstatus, get_jobtype
from common import settings 
from jobs.tasks import runGenerator
log = logging.getLogger(__name__)



def createRegisterJob(fileObjects):
    log.info("Creating  downloadFiles job")
    kitchenId = fileObjects["VendorAlias"]
    fileName = fileObjects["FileName"]
    
    jobtype = get_jobtype("downloadFile") 
    gsession = str(uuid.uuid4())
    global_session,created = ContentStore.objects.get_or_create(global_session=gsession,account_name=kitchenId)
                                                            
    job = JobsStatus(jobstatus=get_jobstatus(settings.JOB_STATUS.Future.value),jobtype=jobtype,job_step=settings.INIT,global_session=global_session,fullfilename=fileName)       
         
    SessionKeyValueLog.objects.get_or_create(global_session=job.global_session,jobtype=job.jobtype, key=settings.SESSION.edit_object.value, defaults={ 'value':json.dumps(editobject) })     
    
    job.save()
    log.info("Created  downloadFiles job")
    return job

def process(t):  
    try :
        log.info(f">>>>>>>>>>>>  Starting - fileWatcher_ {t} >>>>>>>>>>>>>>>>>>>>>>>>>" )
        pending_jobs = PrintJobs.objects.filter(print_status="pending")
        
        if not pending_jobs.exists():
            log.info("No pending jobs found. Skipping processing.")
            return
        for job in pending_jobs:
            job.print_status = "processing"
            job.save()
            runGenerator.delay(job.id, t)
        log.info(f"********************* watch_external_sources finished *********************")
   
    except Exception as e :
        log.exception(f"exception in process inputWatcher_ # e : {e}")
        raise e
   

def process_job(job_id,t):
    log.error("If you see a lot of this messages probably you need implement inputWatcher process_job function.[job_id=%i]" % (job_id))
        
        