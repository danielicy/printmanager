from django.db import models
import uuid
from django.contrib.auth.models import User
from common.models import BaseModel
from celery.worker.strategy import default
from django.db.models.fields import TextField
from printmanager import  settings


#===============================================================================
# jobstatus_id    jobstatus_name
# 1    Future
# 2    Waiting
# 3    Processing
# 4    Completed
# 5    Failed
#===============================================================================
class JobStatusNames(models.Model):
    jobstatus_id   = models.AutoField(primary_key=True , help_text="Job status ID.") 
    jobstatus_name = models.CharField(max_length=200, null=False, help_text="Job status name.")
      
    def __unicode__(self):
        return u'%d-%s' % (self.jobstatus_id,self.jobstatus_name)
    
#===============================================================================
# "jobtype_id"    "jobtype_name"
#'1', 'distributor', '7'
#'2', 'trimWatcher', '1'
#'3', 'downloadFile', '3'
#'4', 'trim', '3'

#===============================================================================
class JobType(models.Model):
    jobtype_id = models.AutoField(primary_key=True , help_text="Job type ID.")
    jobtype_name = models.CharField(max_length=200, null=False, help_text="Job type name.")
    jobtype_max_retries = models.SmallIntegerField(default=7,null=False)
      
    def __unicode__(self):
        return u'%d-%s' % (self.jobtype_id,self.jobtype_name)
     
class ContentStore(BaseModel):
    global_session = models.CharField(primary_key=True, max_length=36)    
    bvp_content_create = models.TextField()
    bvp_content_update = models.TextField()
    account_name = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' % (self.global_session)

    class Meta:
        managed = False
        db_table = 'jobs_contentstore'
    
class JobsStatus(BaseModel):
    jobid = models.AutoField(primary_key=True , help_text="Job ID.")
    jobstatus = models.ForeignKey(JobStatusNames,on_delete=models.DO_NOTHING)
    jobtype = models.ForeignKey(JobType,on_delete=models.DO_NOTHING)
    job_priority = models.IntegerField(null=False,default=50, help_text="Job priority.")
    job_failure_count = models.IntegerField(null=False,default=0, help_text="Job failure count.")
    job_step = models.IntegerField(null=False,default=0,help_text="Job steps.")
    global_session = models.ForeignKey(ContentStore,on_delete=models.DO_NOTHING)
    fullfilename = models.CharField(max_length=1000, null=True)
    task_id = models.CharField(max_length=50, null=True)

    class Meta:
        ordering = ('global_session','job_priority',)
    def __unicode__(self):
        return u'%s-%d-%s-%s' % (self.global_session,self.jobid,self.jobstatus,self.jobtype)
    def reset_job_url(self):
        if self.jobstatus.jobstatus_name == 'Failed' or settings.DEBUG:
            return '<a href="/%s/%d" target="_blank">run now</a>' % (self.jobtype.jobtype_name.lower(),self.jobid)
        else:
            return '';
    reset_job_url.allow_tags = True
    


class SessionKeyValueLog(BaseModel):
    global_session = models.ForeignKey(ContentStore,on_delete=models.DO_NOTHING)
    jobtype = models.ForeignKey(JobType,on_delete=models.DO_NOTHING)
    key = models.CharField(max_length=100, null=False)
    value = models.CharField(max_length=10000, null=True)
    
    def __unicode__(self):
        return u'%s - %s:%s' % (self.global_session,self.key,self.value)
    
    class Meta:
        unique_together=("global_session","key")

class PrintJobs(BaseModel):
    id = models.AutoField(primary_key=True, db_column='id')
    card_id = models.IntegerField(null=False, db_column='cardid')
    print_status = models.CharField(max_length=100, null=True, db_column='printstatus')
    created_date = models.DateTimeField(auto_now_add=True, db_column='created_date')
    print_reason = models.IntegerField(null=True, db_column='print_reason')
    user_id = models.IntegerField(null=False, db_column='userid')

    class Meta:
        db_table = 'print_jobs'



