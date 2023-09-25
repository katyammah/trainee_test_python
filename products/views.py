from .models import Lesson, Product, User, ProductAccess, LessonView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LessonSerializer, LessonsViewSerializer
from django.http import HttpResponse


@api_view(['GET'])
def lesson_list(request):
    """API для выведения списка всех уроков по всем продуктам,
     к которым пользователь имеет доступ,
     с выведением информации о статусе и времени просмотра"""
    user = request.user
    accessible_products = ProductAccess.objects.filter(user=user, access=ProductAccess.ACCESS).values_list('product_id',
                                                                                                           flat=True)
    lessons = Lesson.objects.filter(product__in=accessible_products)
    lesson_views = LessonView.objects.filter(user=user)

    lesson_info = {}

    for lesson in lessons:
        lesson_info[lesson.id] = {
            'title': lesson.title,
            'external_link': lesson.external_link,
            'duration_in_seconds': lesson.duration_in_seconds,
            'status': LessonView.IS_NOT_WATCHED,
            'view_time_in_seconds': 0
        }

    for lesson_view in lesson_views:
        lesson_id = lesson_view.lesson_id
        if lesson_id in lesson_info:
            lesson_info[lesson_id]['status'] = lesson_view.status
            lesson_info[lesson_id]['view_time_in_seconds'] = lesson_view.view_time_in_seconds

    serializer = LessonSerializer(lesson_info.values(), many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_lessons_with_info(request, product_id):
    """API с выведением списка уроков по конкретному продукту,
     к которому пользователь имеет доступ,
     с выведением информации о статусе и времени просмотра,
     а также датой последнего просмотра ролика"""

    user = request.user
    product = Product.objects.get(id=product_id)
    accessible_products = ProductAccess.objects.filter(user=user, access=ProductAccess.ACCESS).values_list('product_id',
                                                                                                           flat=True)

    if product.id in accessible_products:
        lesson_views_in_product = LessonView.objects.filter(user=user, lesson__product__id=product.id)
        lesson_view_info = {}
        for lesson_view in lesson_views_in_product:
            lesson_view_info[lesson_view.id] = {
                'lesson_title': lesson_view.lesson.title,
                'viewed_in_seconds': f'{lesson_view.view_time_in_seconds} / {lesson_view.lesson.duration_in_seconds}',
                'status': lesson_view.status,
                'date_of_last_view': lesson_view.date_of_last_view.strftime("%d-%m-%Y")
            }

        serializer = LessonsViewSerializer(lesson_view_info.values(), many=True)
        return Response(serializer.data)

    else:
        return HttpResponse(f'{product} не доступен для пользователя {user}')
