from django.contrib import admin

from .models import MangoUsersModel


@admin.register(MangoUsersModel)
class MangoUsersModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title', 'age')
    search_fields = ('name', 'title')
