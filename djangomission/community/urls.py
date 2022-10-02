from django.urls import path, include

from .views import QuestionView, QuestionDetailView

urlpatterns = [
    path('/<int:klass_id>/question', QuestionView.as_view()),
    path('/<int:klass_id>/question/<int:question_id>', QuestionDetailView.as_view()),
]