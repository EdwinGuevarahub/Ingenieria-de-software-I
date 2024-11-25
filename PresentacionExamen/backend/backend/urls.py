"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from api import views
from rest_framework import routers

class CustomDefaultRouter(DefaultRouter):
    def get_api_root_view(self):
        from rest_framework.response import Response
        from rest_framework.views import APIView

        class APIRootView(APIView):
            def get(self, request, *args, **kwargs):
                return Response({
                    'auth': request.build_absolute_uri('api/auth/'),
                    'exam-questionaire': request.build_absolute_uri('api/exam-questionaire/'),
                    'exam-scheduled': request.build_absolute_uri('api/exam-scheduled/'),
                    'exam': request.build_absolute_uri('api/exam/'),
                    'notes': request.build_absolute_uri('api/notes/'),
                    'question': request.build_absolute_uri('api/question/'),
                    'salon': request.build_absolute_uri('api/salon/'),
                })

        return APIRootView.as_view()

router = routers.DefaultRouter()
router.register(r'api', views.ApiViewSet, basename='api')
router.register(r'api/auth', views.AuthViewSet, basename='auth')
router.register(r'api/exam-questionaire', views.ExamQuestionaireViewSet, basename='exam_q&a')
router.register(r'api/exam-scheduled', views.ExamScheduledViewSet, basename='exam_scheduled_info')
router.register(r'api/exam', views.ExamViewSet, basename='exam_info')
router.register(r'api/notes', views.NotesViewSet, basename='notes_info')
router.register(r'api/question', views.QuestionViewSet, basename='question_info')
router.register(r'api/salon', views.SalonViewSet, basename='salon_info')
router.register(r'api/subject', views.SubjectViewSet, basename='subject_info')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
