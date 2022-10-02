from django.urls import path

from .views import MasterView, KlassView, KlassDetailView

urlpatterns = [
    path('/setmaster', MasterView.as_view()),
    path('', KlassView.as_view()),
    path('/<int:klass_id>', KlassDetailView.as_view())
]