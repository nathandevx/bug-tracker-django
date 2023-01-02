from django.db import models
from django.conf import settings


class TimestampCreatorMixin(models.Model):
	creator = models.ForeignKey(verbose_name="Creator", to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_creator')
	updater = models.ForeignKey(verbose_name="Updater", to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_updater')
	created_at = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name="Date updated", auto_now=True)

	class Meta:
		abstract = True
		verbose_name = "TimestampCreatorMixin"
		verbose_name_plural = "TimestampCreatorMixin"

