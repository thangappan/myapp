
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.models import User
from work.models import Associate,Task,RevisionHistory


class AssociateInline(admin.StackedInline):

	model = Associate
	can_delete = False
	verbose_name_plural = 'associate'

class UserAdmin(UserAdmin):
	inlines = (AssociateInline,)
	
	

admin.site.unregister(User)
admin.site.register(User,UserAdmin)
