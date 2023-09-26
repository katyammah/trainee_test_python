from .models import Lesson, Product, User, ProductAccess, LessonView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import LessonSerializer, LessonsViewSerializer, StatisticSerializer

from django.db.models import Sum


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
    """API с выведением списка уроков по конкретному продукту (по id),
     к которому пользователь имеет доступ,
     с выведением информации о статусе и времени просмотра,
     а также датой последнего просмотра ролика"""

    user = request.user
    product = Product.objects.get(id=product_id)
    accessible_products = ProductAccess.objects.filter(user=user, access=ProductAccess.ACCESS).values_list('product_id',
                                                                                                           flat=True)

    if product.id in accessible_products:
        lesson_views_in_product = LessonView.objects.filter(user=user, lesson__product=product).prefetch_related(
            'lesson')

        lesson_view_info = {}

        for lesson_view in lesson_views_in_product:
            lesson_view_info[lesson_view.lesson.id] = {
                'lesson_title': lesson_view.lesson.title,
                'viewed_in_seconds': f'{lesson_view.view_time_in_seconds} / {lesson_view.lesson.duration_in_seconds}',
                'status': lesson_view.status,
                'date_of_last_view': lesson_view.date_of_last_view.strftime("%d-%m-%Y")
            }

        not_opened_lessons = Lesson.objects.filter(product=product).exclude(id__in=lesson_view_info)

        for lesson in not_opened_lessons:
            lesson_view_info[lesson.title] = {
                'lesson_title': lesson.title,
                'viewed_in_seconds': f'0 / {lesson.duration_in_seconds} ',
                'status': LessonView.IS_NOT_WATCHED,
                'date_of_last_view': '-'
            }

        serializer = LessonsViewSerializer(lesson_view_info.values(), many=True)
        return Response(serializer.data)

    else:
        return Response({'message': f'У вас нет доступа к продукту {product}'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def get_statistic(request):
    """API для отображения статистики по продуктам.
    Отображает список всех продуктов на платформе, к каждому продукту приложить информацию:
        1) Количество просмотренных уроков от всех учеников.
        2) Сколько в сумме все ученики потратили времени на просмотр роликов.
        3) Количество учеников занимающихся на продукте.
        4) Процент приобретения продукта (рассчитывается исходя из количества полученных доступов к продукту деленное на общее количество пользователей на платформе).
    """
    all_products = Product.objects.all()

    statistic_info = {}

    def get_statistic(product: Product):
        viewed_lessons = LessonView.objects.filter(lesson__product=product, status=LessonView.IS_WATCHED).count()

        total_viewing_time = \
            LessonView.objects.filter(lesson__product=product).values('view_time_in_seconds').aggregate(
                total=Sum('view_time_in_seconds'))['total']

        student_amount = ProductAccess.objects.filter(product=product, access=ProductAccess.ACCESS).values(
            'user').distinct().count()

        all_users = User.objects.all().count()
        percent = student_amount / all_users * 100
        return viewed_lessons, total_viewing_time, student_amount, percent

    for product in all_products:
        v_l, t_v_t, s_a, p_p = get_statistic(product)

        statistic_info[product] = {
            'name': product.name,
            'viewed_lesson': v_l,
            'total_viewing_time': t_v_t,
            'student_amount': s_a,
            'purchase_percent': p_p
        }

    serializer = StatisticSerializer(statistic_info.values(), many=True)
    return Response(serializer.data)
