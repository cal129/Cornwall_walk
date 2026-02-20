from django.urls import path
from . import views

urlpatterns = [
    path('', views.walk_list, name='walk_list'),  # /walks/ → show all walks
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),  # Delete a comment
    path('<slug:slug>/', views.walk_detail, name='walk_detail'),  # /walks/slug/ → show walk by slug
]
