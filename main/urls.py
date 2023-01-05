from django.urls import path
from . import views


app_name = "main"

urlpatterns = [
        path('', views.home, name="home"),
        path('details/<int:id>/', views.detail, name="detail"),
        path('addmusics/', views.add_musics, name="add_musics"),
        path('editmusics/<int:id>/', views.edit_musics, name="edit_musics"),
        path('deletemusics/<int:id>/', views.delete_musics, name="delete_musics"),
        path('addreview/<int:id>/', views.add_review, name="add_review"),
        path('editreview/<int:music_id>/<int:review_id>/', views.edit_review, name="edit_review"),
        path('deletereview/<int:music_id>/<int:review_id>/', views.delete_review, name="delete_review")

]
