from django.urls import path
from . import views           #importa todas as views de actors


urlpatterns = [
    path('reviews/', views.ReviewCreateListView.as_view(), name='review-create-list'),
    path('reviews/<int:pk>/', views.ReviewRetrieveUpdateDestroyView.as_view(), name='review-detail-view'),
]
