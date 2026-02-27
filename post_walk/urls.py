from django.urls import path
from . import views

urlpatterns = [
    path('', views.walk_list, name='walk_list'),  # /walks/ → show all walks
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),  # Delete a comment
    path('walks/create/', views.walk_create, name='walk_create'),
    path('comment/<int:comment_id>/edit/', views.comment_edit, name='comment_edit'),
    path('favourite-walks/', views.favourite_walks, name='favourite_walks'),
    path('<slug:slug>/favourite/', views.toggle_favourite, name='toggle_favourite'),
    path('<slug:slug>/', views.walk_detail, name='walk_detail'),  # /walks/slug/ → show walk by slug
]
