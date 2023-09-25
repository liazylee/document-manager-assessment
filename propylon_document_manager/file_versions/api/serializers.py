from urllib.parse import (unquote)

from rest_framework import serializers

from propylon_document_manager.file_versions.models import FileVersion


class FileVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileVersion
        exclude = ['is_deleted', 'parent_file', ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["file_name"] = unquote(representation["file_name"])
        return representation


class ListFileVersionSerializer(serializers.ModelSerializer):
    child_file = serializers.SerializerMethodField()

    class Meta:
        model = FileVersion
        extra_fields = ["child_file", ]
        exclude = ['is_deleted', 'parent_file', ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["file_name"] = unquote(representation["file_name"])
        return representation

    def get_fields_names(self, declared_fields, info):
        expanded_fields = super().get_fields_names(declared_fields, info)  # type: ignore
        if getattr(self.Meta, "extra_fields", None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

    def get_child_file(self, obj):
        queryset = FileVersion.objects.filter(parent_file=obj.parent_file)
        if queryset:
            return FileVersionSerializer(queryset, many=True).data

    #


class CreateFileVersionSerializer(serializers.ModelSerializer):
    file_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = FileVersion
        exclude = ['is_deleted', 'parent_file', ]

    def create(self, validated_data):
        url_file = validated_data["url_file"]
        if not validated_data.get("file_name"):
            validated_data["file_name"] = url_file.name
        validated_data['file_type'], validated_data['file_size'], \
            validated_data['file_hash'] = url_file.content_type, url_file.size, \
            abs(hash(validated_data['file_name'])) % (10 ** 8)
        version_numer = FileVersion.objects.filter(file_name=validated_data["file_name"],
                                                   file_user=validated_data["file_user"])
        if version_numer:
            validated_data["version_number"] = version_numer.first().version_number + 1
            validated_data["parent_file"] = version_numer.last()
        return super().create(validated_data)
