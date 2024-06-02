from django.urls import path
from .views import IndexView, QtsView

urlpatterns = [
    path('',IndexView.as_view(), name = 'index'),
    path('\qts',QtsView.as_view(), name = 'qts')
]