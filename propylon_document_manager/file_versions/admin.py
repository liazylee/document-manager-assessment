from django.contrib import admin

from file_versions import models


# Register your models here.
@admin.register(models.FileVersion)
class FileVersionAdmin(admin.ModelAdmin):
    list_display = ("file_name", "version_number",  "file_user")
    list_filter = ("file_user",)
    search_fields = ("file_name",)
    ordering = ("version_number",)
    readonly_fields = ("version_number",)


