from rest_framework import serializers

from .models import Lesson, Product, ProductAccess, User, LessonView


class LessonSerializer(serializers.ModelSerializer):
    status = serializers.CharField(max_length=40)
    view_time_in_seconds = serializers.IntegerField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'external_link', 'duration_in_seconds', 'status', 'view_time_in_seconds']


class LessonsViewSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(max_length=100)
    date_of_last_view = serializers.DateTimeField()
    viewed_in_seconds = serializers.CharField(max_length=50)

    class Meta:
        model = LessonView
        fields = ['lesson_title', 'status', 'viewed_in_seconds', 'date_of_last_view']