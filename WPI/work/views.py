# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

# our own models and forms
from django.contrib.auth.models import User
from work.forms import TaskForm
from work.models import Associate


def get_out(request):
	logout(request)
	return HttpResponseRedirect('/work/')
	

@login_required(login_url='/work/')
def index(request):
	user = request.user
	userobj = User.objects.get(username=user)
	tasks = ''
	if userobj is not None:
		first_name  = userobj.first_name	
		supervisor_name = userobj.associate.supervisor_name 
		is_super = userobj.associate.is_supervisor
		associates = False
		if is_super:
			associates = userobj.associate.reporting_authority.all()
		else:
			tasks = userobj.associate.task_assigned_to.all()
	
	if not first_name:
		first_name = user
	return render_to_response('work/home.html',{ 'user' : first_name, 'supervisor' : supervisor_name, 'is_super': is_super, 'associates' : associates, 'tasks' : tasks })
	

def login_user(request):
	state = "Please log in below..."
	username = password = ''
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/work/main')
			else:
				state = "Your account is not active, please contact the site admin."
		else:
			state = "Invalid username and password."
	return render_to_response('work/login.html',{'state':state },context_instance=RequestContext(request))
	
@login_required(login_url='/work/')
def assign_task(request,user_id):

	associate = Associate.objects.get(employee_id=user_id)
	if request.method == "POST":
		form = TaskForm(request.POST)
		if form.is_valid():
			task = form.save(commit=False)
			task.task_status = 'assign'
			task.save()
			associate.user_status = 'BLK'
			associate.save()
			return HttpResponseRedirect('/work/main')
	else:
		userobj = User.objects.get(username=request.user)
		form = TaskForm(initial={ 'assigned_to' : associate, 'created_by' : userobj.associate })
	return render_to_response('work/assign_task.html', { 'form' : form, 'user_id' : user_id },context_instance=RequestContext(request))
	
	
@login_required(login_url='/work/')
def show_task(request, user_id):
	
	user = Associate.objects.get(employee_id=user_id)
	tasks = user.task_assigned_to.all()
	return render_to_response('work/show_task.html',{'tasks' : tasks })
