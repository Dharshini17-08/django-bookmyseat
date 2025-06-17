from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Movie, Theater, Seat, Booking
from datetime import datetime, timedelta
from django.utils import timezone

# Create your tests here.

class MovieBookingTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create a simple test image
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake-image-content',
            content_type='image/jpeg'
        )
        
        # Create test movie
        self.movie = Movie.objects.create(
            name='Test Movie',
            rating=8.0,
            cast='Test Actor 1, Test Actor 2',
            description='A test movie for testing purposes',
            image=self.test_image
        )
        
        # Create test theater
        self.theater = Theater.objects.create(
            name='Test Theater',
            movie=self.movie,
            time=timezone.now() + timedelta(days=1)
        )
        
        # Create test seats
        self.seat1 = Seat.objects.create(
            theater=self.theater,
            seat_number='A1',
            is_booked=False
        )
        self.seat2 = Seat.objects.create(
            theater=self.theater,
            seat_number='A2',
            is_booked=False
        )
        
        # Create client
        self.client = Client()

    def test_movie_list_view(self):
        """Test that movie list view returns 200 and contains movies"""
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')

    def test_theater_list_view(self):
        """Test that theater list view returns 200 and contains theaters"""
        response = self.client.get(reverse('theater_list', args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Theater')

    def test_seat_booking_requires_login(self):
        """Test that seat booking requires user to be logged in"""
        response = self.client.get(reverse('book_seats', args=[self.theater.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_seat_booking_with_login(self):
        """Test seat booking functionality when user is logged in"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Test GET request to seat selection page
        response = self.client.get(reverse('book_seats', args=[self.theater.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A1')
        self.assertContains(response, 'A2')

    def test_booking_creation(self):
        """Test that booking is created correctly"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Book a seat
        response = self.client.post(reverse('book_seats', args=[self.theater.id]), {
            'seats': [self.seat1.id]
        })
        
        # Check that booking was created
        booking = Booking.objects.filter(user=self.user, seat=self.seat1).first()
        self.assertIsNotNone(booking)
        self.assertEqual(booking.movie, self.movie)
        self.assertEqual(booking.theater, self.theater)
        
        # Check that seat is now booked
        self.seat1.refresh_from_db()
        self.assertTrue(self.seat1.is_booked)

    def test_booking_already_booked_seat(self):
        """Test that booking an already booked seat fails"""
        # Book seat first
        self.seat1.is_booked = True
        self.seat1.save()
        
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Try to book the same seat
        response = self.client.post(reverse('book_seats', args=[self.theater.id]), {
            'seats': [self.seat1.id]
        })
        
        # Should not create a new booking
        booking_count = Booking.objects.filter(user=self.user).count()
        self.assertEqual(booking_count, 0)

    def test_theater_availability_status(self):
        """Test theater availability status method"""
        # Initially all seats are available (2 seats total)
        self.assertEqual(self.theater.get_availability_status(), "Only 2 seats left")
        
        # Book one seat
        self.seat1.is_booked = True
        self.seat1.save()
        
        # Should show only 1 seat left
        self.assertEqual(self.theater.get_availability_status(), "Only 1 seats left")
        
        # Book both seats
        self.seat2.is_booked = True
        self.seat2.save()
        
        # Should show fully booked
        self.assertEqual(self.theater.get_availability_status(), "Fully Booked")

class UserAuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_registration(self):
        """Test user registration functionality"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        
        # Should redirect to profile page
        self.assertEqual(response.status_code, 302)
        
        # Check that user was created
        new_user = User.objects.filter(username='newuser').first()
        self.assertIsNotNone(new_user)

    def test_user_login(self):
        """Test user login functionality"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        # Should redirect to home page
        self.assertEqual(response.status_code, 302)

    def test_profile_view_requires_login(self):
        """Test that profile view requires user to be logged in"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_profile_view_with_login(self):
        """Test profile view when user is logged in"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
