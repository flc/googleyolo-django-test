from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class GoogleUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        related_name="googleuser",
        )
    google_userid = models.TextField(
        _("google userID"),
        )

    class Meta:
        verbose_name = _("Google user")
        verbose_name_plural = _("Google users")

    def __str__(self):
        return self.google_userid
