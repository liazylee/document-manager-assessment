from file_versions.api.serializers import FileVersionSerializer
from file_versions.models import FileVersion
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from utils.permission import OwnFilePermission

from propylon_document_manager.file_versions.api.serializers import CreateFileVersionSerializer, \
    ListFileVersionSerializer


class FileVersionViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet):
    authentication_classes = []
    permission_classes = [IsAuthenticated, OwnFilePermission]
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.file_size = instance.url_file.size
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
