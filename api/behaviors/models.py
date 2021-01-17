from django.db import models

class Timestampable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def touch(self, rate_limit_in_seconds=None):
        self.save(update_fields=['updated_at'])

    class Meta:
        abstract = True
