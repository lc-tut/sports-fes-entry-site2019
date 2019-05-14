from django.contrib import admin
from api.models import Team, Member

class MemberInline(admin.TabularInline):
    model = Member

    def get_queryset(self, request):
        qs = super(MemberInline, self).get_queryset(request)
        return qs.filter(is_registered=True)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'leader', 'created_by', 'is_registered', )
    list_filter = ('event', )
    inlines = [
        MemberInline,
    ]


admin.site.register(Team, TeamAdmin)