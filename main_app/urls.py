from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path('add_habit/<str:name>', views.add_habit, name='add_habit'),
    path('alinkanlik_ekle', views.add_habit, name='add_habit'),
    path('ekle.html', views.ekle_view, name='ekle'),
    path('habit_done/<int:habit_id>/<int:minus_day>', views.habit_done, name='habit_done'),
    path('habit/<int:habit_id>/', views.habit_view, name='habit'),
    path('degistir/<str:name>/<int:habit_id>/', views.Degistir.as_view(), name='degistir'),
    path('sil/<int:habit_id>/', views.sil, name='sil'),
    path('arena.html', views.arena_view, name='arena'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('katil/<int:habit_id>/', views.katil, name='katil'),
    path('ayril/<int:habit_id>/', views.ayril, name='ayril'),
    path('kullanici_sil/<int:user_id>', views.kullanici_sil, name='kullanici_sil'),
]