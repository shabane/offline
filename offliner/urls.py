from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<int:page_id>/delete', views.delete),
]
