from django.urls import path, include
from .views import (
    QuestionView,
    AnswerCreateView,
    AnswerRUDView,
    AnswerListView,
    AnswerLikeView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"questions", QuestionView)
urlpatterns = [

    path('', include(router.urls)),
    path('questions/<slug:slug>/answer/',
         AnswerCreateView.as_view(), name="answer-create"),
    path('questions/<slug:slug>/answers/',
         AnswerListView.as_view(), name="answer-list"),

    path('answers/<uuid:uuid>',
         AnswerRUDView.as_view(), name="answer-detail"),
    path('answers/<uuid:uuid>/like/',
         AnswerLikeView.as_view(), name="answer-like"),
]
