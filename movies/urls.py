from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('theater/<int:movie_id>/', views.theater_list, name='theater_list'),
    path('book/<int:theater_id>/', views.book_seats, name='book_seats'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]