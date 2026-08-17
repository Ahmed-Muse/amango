from django.urls import path

from . import views

app_name = 'mango'

urlpatterns = [
    path('', views.MangoUsersListView.as_view(), name='mangousers_list'),
    path('create/', views.MangoUsersCreateView.as_view(), name='mangousers_create'),
    path('<int:pk>/', views.MangoUsersDetailView.as_view(), name='mangousers_detail'),
    path('<int:pk>/edit/', views.MangoUsersUpdateView.as_view(), name='mangousers_update'),
    path('<int:pk>/delete/', views.MangoUsersDeleteView.as_view(), name='mangousers_delete'),
]
