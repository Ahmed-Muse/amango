from django.db import models


class MangoUsersModel(models.Model):
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    age = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
