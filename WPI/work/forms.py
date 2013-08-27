
from django.forms import ModelForm
from work.models import Task


class TaskForm(ModelForm):
	
	class Meta:
		model = Task
		fields = ['summary','description','assigned_to','task_status','created_by']
		