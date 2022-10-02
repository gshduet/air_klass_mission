from django.urls import path

from .views import SetMasterView, KlassCreateView

urlpatterns = [
    path('/setmaster', SetMasterView.as_view()),
    path('/klass', KlassCreateView.as_view())
]