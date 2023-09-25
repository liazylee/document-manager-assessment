from django.db.models import QuerySet
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from propylon_document_manager.file_versions.api.serializers import FileVersionSerializer, CreateFileVersionSerializer, \
    ListFileVersionSerializer
from propylon_document_manager.file_versions.models import FileVersion
from propylon_document_manager.file_versions.permission import OwnFilePermission


class FileVersionViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, OwnFilePermission]
    serializer_class = FileVersionSerializer
    queryset = FileVersion.objects.all()

    def get_queryset(self) -> QuerySet[FileVersion]:
        if self.action == "list":
            return FileVersion.objects.filter(file_user=self.request.user,  # type: ignore
                                              is_deleted=False, parent_file=None)

        return FileVersion.objects.filter(file_user=self.request.user,  # type: ignore
                                          is_deleted=False)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateFileVersionSerializer
        if self.action == "list":
            return ListFileVersionSerializer
        return FileVersionSerializer

    # @extend_schema(
    #     description='Paths for download file.\nExample: api/file_versions/download_by_version/test.pdf\nExample with version: api/file_versions/download_by_version/test.pdf?revision=2',
    #     responses={
    #         200: OpenApiResponse(
    #             description='File download',
    #         ),
    #         401: OpenApiResponse(
    #             description='Authentication credentials were not provided.',
    #         ),
    #         404: OpenApiResponse(description="not find."),
    #     }
    # )
    # @action(detail=False, methods=["GET"])
    # def download_by_version(self, request, *args, **kwargs):
    #     file_name = unquote(request.path.split("/")[-1]).split("?")[0]
    #     print(file_name, 'file_name')
    #     version = request.GET.get("revision", '1')
    #
    #     file_version = get_object_or_404(FileVersion, file_name=file_name,
    #                                      version_number=version, is_deleted=False)
    #     file_name = unquote(file_version.file_name)  # type: ignore
    #     file_path = file_version.url_file.path
    #     with open(file_path, "rb") as f:
    #         response = HttpResponse(f.read(), content_type="application/octet-stream")
    #         response["Content-Disposition"] = f"attachment; filename={file_name}"
    #         return response


@api_view(["GET"])
@permission_classes([IsAuthenticated, OwnFilePermission])
@authentication_classes([TokenAuthentication, ])
def download_by_version(request, file_name):
    version = request.GET.get("revision", '1')
    file_version = get_object_or_404(FileVersion, file_name=file_name,
                                     version_number=version, is_deleted=False, file_user=request.user)
    with open(file_version.url_file.path, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/octet-stream")
        response["Content-Disposition"] = f"attachment; filename={file_name}"
        return response
