from urllib.parse import (quote_plus,
                          unquote_plus)

from file_versions.models import FileVersion
from rest_framework import serializers


class FileVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileVersion
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["file_name"] = unquote_plus(representation["file_name"])
        return representation


class ListFileVersionSerializer(serializers.ModelSerializer):
    child_file = serializers.SerializerMethodField()

    class Meta:
        model = FileVersion
        fields = "__all__"
        extra_fields = ["child_file", ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["file_name"] = unquote_plus(representation["file_name"])
        return representation

    def get_fields_names(self, declared_fields, info):
        expanded_fields = super().get_fields_names(declared_fields, info)
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
    class Meta:
        model = FileVersion
        fields = "__all__"

    def create(self, validated_data):
        if validated_data["file_user"] != self.context["request"].user:
            raise serializers.ValidationError("You can't upload file for other users")
        validated_data["file_name"] = validated_data["url_file"].name
        validated_data["file_name"] = quote_plus(validated_data["file_name"])
        if (version_numer := FileVersion.objects.filter(file_name=
                                                        validated_data["file_name"])):
            validated_data["version_number"] = version_numer.first().version_number + 1
            validated_data["parent_file"] = version_numer.last()
        return super().create(validated_data)
