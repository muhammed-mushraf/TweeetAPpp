from django.urls import path
from . import views
from .views import add_comment, tweet_detail


urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('toggle-like/<int:tweet_id>/', views.toggle_like, name='toggle_like'),
    path('register/', views.register, name='register'),
    path('<int:tweet_id>/', views.tweet_detail, name='tweet_detail'),
    path('add-comment/', add_comment, name='add_comment'),

    path('profile/<str:username>/', views.profile, name='profile'),

]
