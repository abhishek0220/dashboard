from django.contrib import admin
from .models import Member, Pin
from django.contrib.auth.admin import UserAdmin

class MemberAdmin(UserAdmin):
    list_display = ('username', 'email', 'name', 'gender','is_staff')

class PinAdmin(admin.ModelAdmin):
    list_display = ['author', 'pin', 'pub_date']
    def pin(self, obj):
        if(len(obj.content) > 50):
            return obj.content[:50] + '...'
        else:
            return obj.content

admin.site.register(Member, MemberAdmin)

admin.site.register(Pin, PinAdmin)