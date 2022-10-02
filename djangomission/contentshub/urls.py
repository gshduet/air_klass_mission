from django.urls import path

from .views import MasterView, KlassView, KlassDetailView

urlpatterns = [
    path('/setmaster', MasterView.as_view()),
    path('/klass', KlassView.as_view()),
    path('/klass/<int:id>', KlassDetailView.as_view())
]