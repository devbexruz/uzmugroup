
from rest_framework import serializers
from ..pages.models import (
    User,
    Course,
    Lesson,
    Task,
    TaskSolution,
    ChatMessage
)

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'auth_token',
            'is_teacher'
        )



