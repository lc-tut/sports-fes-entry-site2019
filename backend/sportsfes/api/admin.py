from django.contrib import admin
from api.models import Team, Member

class TeamAdmin(admin.ModelAdmin):
    pass

class MemberAdmin(admin.ModelAdmin):
    pass

admin.site.register(Team, TeamAdmin)
admin.site.register(Member, MemberAdmin)