from django.db import models


# url_file stores in  each user's folder each file's name and version number
def custom_dirction(instance, filename):
    return f"/{instance.file_user}/{instance.file_name}/{instance.version_number}/"


class FileVersion(models.Model):
    file_name = models.fields.CharField(max_length=512, db_index=True, blank=True, null=True)
    version_number = models.fields.IntegerField(default=1)
    url_file = models.FileField(upload_to=custom_dirction, )
    file_user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    extra_info = models.CharField(max_length=512, blank=True, null=True)
    file_type = models.CharField(max_length=100, blank=True, null=True)
    file_size = models.IntegerField(blank=True, null=True)
    file_hash = models.CharField(max_length=100, blank=True, null=True)
    parent_file = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ['file_name', 'version_number', 'file_user']
        ordering = ['-version_number', ]

    def __str__(self):
        return f"{self.file_name} - {self.version_number} - {self.file_user}"
