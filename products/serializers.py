from rest_framework import serializers

from .models import Lesson, Product, LessonView


class LessonSerializer(serializers.ModelSerializer):
    status = serializers.CharField(max_length=40)
    view_time_in_seconds = serializers.IntegerField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'external_link', 'duration_in_seconds', 'status', 'view_time_in_seconds']


class LessonsViewSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(max_length=100)
    viewed_in_seconds = serializers.CharField(max_length=50)

    class Meta:
        model = LessonView
        fields = ['lesson_title', 'status', 'viewed_in_seconds', 'date_of_last_view']


class StatisticSerializer(serializers.ModelSerializer):
    viewed_lesson = serializers.IntegerField()
    total_viewing_time = serializers.IntegerField()
    student_amount = serializers.IntegerField()
    purchase_percent = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = Product
        fields = ['name', 'viewed_lesson', 'total_viewing_time', 'student_amount', 'purchase_percent']



