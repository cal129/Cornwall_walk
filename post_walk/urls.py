from django.urls import path
from . import views

urlpatterns = [
    path('', views.walk_list, name='walk_list'),  # /walks/ → show all walks
    path('<int:pk>/', views.walk_detail, name='walk_detail'),  # /walks/1/ → show walk #1
]
