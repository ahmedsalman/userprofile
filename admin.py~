from django.contrib import admin

from userprofile.models import Felloz, ProfessionalExperience, UserProfile, Action


class UserProfileAdmin(admin.ModelAdmin):
    pass

class ProfessionalExperienceAdmin(admin.ModelAdmin):
    ordering = ('user', 'title')


class FellozAdmin(admin.ModelAdmin):
    pass

class ActionAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ProfessionalExperience, ProfessionalExperienceAdmin)
admin.site.register(Felloz, FellozAdmin)
admin.site.register(Action, ActionAdmin)
