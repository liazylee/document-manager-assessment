from urllib.parse import unquote

import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from propylon_document_manager.file_versions.api.serializers import ListFileVersionSerializer
from propylon_document_manager.file_versions.models import FileVersion

User = get_user_model()


class TestFileVersionViewSet:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.unauthenticated_client = APIClient()
        self.api_client = APIClient()
        self.user = User.objects.create_user(
            email="test_123@gmail.com", password="test_password")
        self.token = Token.objects.create(user=self.user)
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @pytest.mark.django_db
    def test_get_file_version_list(self):
        response = self.api_client.get("/api/file_versions/")
        print(response.data, 'list')
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_upload_file(self):
        with open("../../../docs/Full Stack Engineer Test.pdf", "rb") as file:
            response = self.api_client.post("/api/file_versions/",
                                            data={"url_file": file, })
            assert response.status_code == 201
        file_version = FileVersion.objects.filter(file_name='Full Stack Engineer Test.pdf').count()
        assert file_version == 1

    # test upload file with same name
    @pytest.mark.django_db
    def test_upload_file_with_same_name(self):
        with open("../../../docs/Full Stack Engineer Test.pdf", "rb") as file:
            response = self.api_client.post("/api/file_versions/",
                                            data={"url_file": file, })
            assert response.status_code == 201
        with open("../../../docs/Full Stack Engineer Test.pdf", "rb") as file:
            response = self.api_client.post("/api/file_versions/",
                                            data={"url_file": file, })
            assert response.status_code == 201
        file_version = FileVersion.objects.filter(file_name='Full Stack Engineer Test.pdf').count()
        assert file_version == 2

    @pytest.mark.django_db
    def test_download_file(self):
        with open("../../../docs/Full Stack Engineer Test.pdf", "rb") as file:
            response = self.api_client.post("/api/file_versions/", data={"url_file": file,
                                                                         })
            assert response.status_code == 201
        file_version = FileVersion.objects.filter(file_name='Full Stack Engineer Test.pdf')
        assert file_version
        file_name = \
            unquote('"/api/file_versions/download_by_version/Full%20Stack%20Engineer%20Test.pdf'.split("/")[-1]).split(
                "?")[
                0]
        assert file_name == 'Full Stack Engineer Test.pdf'
        file_version = FileVersion.objects.filter(file_name=file_name, file_user=self.user)
        assert file_version
        response = self.api_client.get("/api/file_versions/download_by_version/Full%20Stack%20Engineer%20Test.pdf")

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_download_file_with_version(self):
        with open("../../../docs/Full Stack Engineer Test.pdf", "rb") as file:
            response = self.api_client.post("/api/file_versions/",
                                            data={"url_file": file, 'file_name': 'Full Stack Engineer Test.pdf'})
            assert response.status_code == 201
        with open("../../../docs/Full Stack Engineer Test.pdf", "rb") as file:
            response = self.api_client.post("/api/file_versions/",
                                            data={"url_file": file, 'file_name': 'Full Stack Engineer Test.pdf'})
            assert response.status_code == 201
        response = self.api_client.get(
            "/api/file_versions/download_by_version/Full%20Stack%20Engineer%20Test.pdf?revision=2")
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_download_file_with_version_not_found(self):
        with open("../../../docs/Full Stack Engineer Test.pdf", "rb") as file:
            response = self.api_client.post("/api/file_versions/", data={"url_file": file})
            assert response.status_code == 201
        response = self.api_client.get(
            "/api/file_versions/download_by_version/Full%20Stack%20Engineer%20Test.pdf?revision=6")
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_unauthorized_user(self):
        response = self.unauthenticated_client.get("/api/file_versions/")
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_unauthorized_user_upload_file(self):
        with open("../../../docs/Full Stack Engineer Test.pdf", "rb") as file:
            response = self.unauthenticated_client.post("/api/file_versions/", data={"url_file": file})
            assert response.status_code == 401

    @pytest.mark.django_db
    def test_unauthorized_user_download_file(self):
        with open("../../../docs/Full Stack Engineer Test.pdf", "rb") as file:
            response = self.api_client.post("/api/file_versions/", data={"url_file": file})
            assert response.status_code == 201
        response = self.unauthenticated_client.get(
            "/api/file_versions/download_by_version/Full%20Stack%20Engineer%20Test.pdf")
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_unauthorized_user_download_file_with_version(self):
        with open("../../../docs/Full Stack Engineer Test.pdf", "rb") as file:
            response = self.api_client.post("/api/file_versions/", data={"url_file": file})
            assert response.status_code == 201
        response = self.unauthenticated_client.get(
            "/api/file_versions/download_by_version/Full%20Stack%20Engineer%20Test.pdf?revision=2")
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_file_version_with_data(self):
        with open("../../../docs/Full Stack Engineer Test.pdf", "rb") as file:
            response = self.api_client.post("/api/file_versions/", data={"url_file": file})
            assert response.status_code == 201
        with open("../../../docs/Full Stack Engineer Test.pdf", "rb") as file:
            response = self.api_client.post("/api/file_versions/", data={"url_file": file})
            assert response.status_code == 201
        response = self.api_client.get("/api/file_versions/")
        queryset = FileVersion.objects.filter(file_user=self.user, is_deleted=False, parent_file=None)
        serializer_data = ListFileVersionSerializer(queryset, many=True).data

        assert response.status_code == 200
