from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from . import models


class GoogleUserAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'google_userid',
        )
    raw_id_fields = ("user",)


admin.site.register(models.GoogleUser, GoogleUserAdmin)
