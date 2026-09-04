from django.urls import path
from . import views
app_name = 'mango'

urlpatterns = [
    path('', views.mango_users_list, name='mangousers_list'),
    path('create/', views.mango_users_create, name='mangousers_create'),
    path('<int:pk>/', views.mango_users_detail, name='mangousers_detail'),
    path('<int:pk>/edit/', views.mango_users_update, name='mangousers_update'),
    path('<int:pk>/delete/', views.mango_users_delete, name='mangousers_delete'),
]
