from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

from propylon_document_manager.file_versions.api.views import download_by_version

# from propylon_document_manager import file_versions  # noqa: F401

# API URLS
urlpatterns = [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("api-auth/", include("rest_framework.urls")),
    path("auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    re_path(r'api/file_versions/download_by_version/(?P<file_name>.+)(?:\?revision=\d+)?$',
            download_by_version, name='download_by_version')

]

if settings.DEBUG:
    urlpatterns = [path(settings.ADMIN_URL, admin.site.urls)] + urlpatterns
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
