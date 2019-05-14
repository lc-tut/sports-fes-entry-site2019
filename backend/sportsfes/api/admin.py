from django.contrib import admin
from api.models import Team, Member

class MemberInline(admin.TabularInline):
    model = Member


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'leader', 'created_by', 'is_registered', )
    list_filter = ('event', 'is_registered')
    inlines = [
        MemberInline,
    ]


admin.site.register(Team, TeamAdmin)