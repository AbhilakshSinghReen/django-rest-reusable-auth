from django.contrib import admin

from core.models.models import CustomUser, UserInvite
from core.admin.CustomUserAdmin import CustomUserAdmin
from core.admin.UserInviteAdmin import UserInviteAdmin


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserInvite, UserInviteAdmin)
