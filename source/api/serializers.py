from rest_framework import serializers
from webapp.models import Project, Task


class TaskSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'summary', 'description', 'status', 'type',
                  'project', 'created_at', 'updated_at', 'created_by', 'assigned_to')


class ProjectSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    project_tasks = TaskSerializer(many=True, read_only=True, source='projects_task')

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'created_at', 'updated_at', 'project_status', 'project_tasks')


