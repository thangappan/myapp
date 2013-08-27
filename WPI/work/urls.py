
from django.conf.urls import patterns,url

from work import views

urlpatterns = patterns('',
	
		url(r'^main/$',views.index,name="home"),
		url(r'^logout/$',views.get_out,name="logout"),
		url(r'^$',views.login_user,name="login"),
		url(r'^assign/(?P<user_id>\d+)/$',views.assign_task,name="assign_task"),
		url(r'^show/(?P<user_id>\d+)/$',views.show_task,name="show_task"),

)

