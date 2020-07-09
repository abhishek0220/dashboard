from django.contrib import admin
from .models import Member
from django.contrib.auth.admin import UserAdmin

class MemberAdmin(UserAdmin):
    list_display = ('username', 'email', 'name', 'gender','is_staff')
    def name(self, obj):
        return obj.first_name + obj.last_name

admin.site.register(Member, MemberAdmin)