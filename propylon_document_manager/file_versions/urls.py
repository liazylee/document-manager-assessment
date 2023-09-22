
from rest_framework.routers import DefaultRouter

from propylon_document_manager.file_versions.api.views import FileVersionViewSet

router=DefaultRouter()
router.register(r'file_versions', FileVersionViewSet, basename='file_versions')
urlpatterns = [

]
urlpatterns += router.urls


