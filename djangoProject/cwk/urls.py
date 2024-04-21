from django.contrib import admin
from django.urls import path, include

from .views import login_view, logout_view, stories, delete_story

urlpatterns = [
    #path('index/', view.index, name='index'),
    path('api/login', login_view, name='login'),
    path('api/logout', logout_view, name='logout'),
    path('api/stories', stories, name='postStory'),
    path('api/stories/<int:key>', delete_story, name='deleteStory')
    # path('api/stories', get_story, name='getStory'),
    # path('register/', views.register, name='register'),
    # path('logout/', views.logout, name='logout'),
]
