from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Associate(models.Model):
	
	STATUS = (
        ('AVL','Available'),
        ('BLK','Blocked'),
        ('OFF','Offline')
    )
        
	user = models.OneToOneField(User)
	employee_id = models.IntegerField(primary_key=True)
	user_status  = models.CharField('User Status',max_length=15,choices=STATUS)
	designation  = models.CharField(max_length=50,)
	mobile       = models.IntegerField(max_length=10,null=True,blank=True)
	is_supervisor = models.BooleanField(default=False)
	supervisor   = models.ForeignKey('self',blank=True,null=True,related_name='reporting_authority')
	
	def supervisor_name(self):
		return	self.supervisor.user.first_name if not self.is_supervisor else None
		
	def __unicode__(self):
		return self.user.first_name
		
	class Meta:
		db_table = 'associate'
	
	
class Task(models.Model):

    STATUS = (
            ('create','CREATED'),
            ('assign','ASSIGNED'),
            ('pending','PENDING'),
            ('ack','ACKNOWLEDGED'),
            ('extend','EXTENDED'),
            ('complete','COMPLETED'),
    )

    task_id = models.AutoField(primary_key=True)
    summary = models.CharField(max_length=250,unique=True)
    description = models.TextField()
    assigned_to = models.ForeignKey(Associate,related_name='task_assigned_to')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Associate,related_name='task_created_by')  # Check abstaract is possible
    ack_at       = models.DateTimeField(null=True,blank=True)
    completed_at = models.DateField(null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    task_status =  models.CharField(max_length=30,choices=STATUS,default='CREATED')

    def __unicode__(self):
        return self.summary


    class Meta:
        db_table = 'tasks'


class RevisionHistory(models.Model):
    revision_id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task)
    reason = models.TextField(max_length=200)
    extended_hrs = models.TimeField()
    current_status = models.CharField(max_length=30)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User)

    def __unicode__(self):
        return self.reason


    class Meta:
        db_table = 'revision_history'