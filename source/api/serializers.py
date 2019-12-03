from rest_framework import serializers
from webapp.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'descripiton', 'created_at', 'updated_at', 'project_status')