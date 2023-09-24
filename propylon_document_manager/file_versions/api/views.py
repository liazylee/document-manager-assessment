from urllib.parse import quote_plus

from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiResponse
from file_versions.api.serializers import FileVersionSerializer
from file_versions.models import FileVersion
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from utils.permission import OwnFilePermission

from propylon_document_manager.file_versions.api.serializers import CreateFileVersionSerializer, \
    ListFileVersionSerializer


class FileVersionViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet):
    authentication_classes = []
    permission_classes = [OwnFilePermission]
    serializer_class = FileVersionSerializer
    queryset = FileVersion.objects.all()

    def get_queryset(self) -> FileVersion:
        if self.action == "list":
            return FileVersion.objects.filter(file_user=self.request.user, is_deleted=False, parent_file=None)
        return FileVersion.objects.filter(file_user=self.request.user, is_deleted=False)

    def get_serializer_context(self) -> serializer_class:
        if self.action == "create":
            return CreateFileVersionSerializer
        if self.action == "list":
            return ListFileVersionSerializer

    @extend_schema(
        description='Paths for download file.\nExample: api/file_versions/download_by_version/test.pdf\nExample with version: api/file_versions/download_by_version/test.pdf?revision=2',
        responses={
            200: OpenApiResponse(
                description='File download',
            ),
            401: OpenApiResponse(
                description='Authentication credentials were not provided.',
            ),
            404: OpenApiResponse(description="not find."),
        }
    )
    @action(detail=False, methods=["GET"])
    def download_by_version(self, request, *args, **kwargs):
        file_name = quote_plus(request.path.split("/")[-1])
        version = request.GET.get("version", '1')
        file_version = get_object_or_404(FileVersion, file_name=file_name,
                                         version_number=version, is_deleted=False)
        file_name = quote_plus(file_version.file_name)
        file_path = file_version.url_file.path
        with open(file_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="application/octet-stream")
            response["Content-Disposition"] = f"attachment; filename={file_name}"
            return response
