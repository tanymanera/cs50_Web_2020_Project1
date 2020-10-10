from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('newpage/', views.new_page, name='new_page'),
    path('wiki/<str:title>', views.show, name='show'),
    path('wiki/<str:title>/edit', views.edit, name='edit'),
    path('random/', views.random, name='random')
]