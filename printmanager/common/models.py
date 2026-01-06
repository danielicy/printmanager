from django.db import models
import celery

# Create your models here.
class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, editable=False, help_text="Create time")
    lastupdatetime = models.DateTimeField(auto_now=True, editable=False, help_text="Time of the last change.")    
    active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True

class BaseTask(celery.Task):

    abstract = True
    def __call__(self, *args, **kwargs):        
        from common.functions import save_job_task
        save_job_task(args[0], self.request.id)
        return self.run(*args, **kwargs)


