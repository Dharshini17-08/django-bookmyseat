from django.core.management.base import BaseCommand
from movies.models import Movie, Theater, Seat
from datetime import datetime, timedelta
import os
import random

class Command(BaseCommand):
    help = 'Create movies using actual image files from media/movies directory'

    def handle(self, *args, **options):
        self.stdout.write('Creating movies with actual image files...')
        
        # Get the media/movies directory path
        media_dir = os.path.join('media', 'movies')
        
        # Check if the directory exists
        if not os.path.exists(media_dir):
            self.stdout.write(self.style.ERROR(f'Directory {media_dir} does not exist!'))
            return
        
        # Get all image files from the directory
        image_files = [f for f in os.listdir(media_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))]
        
        if not image_files:
            self.stdout.write(self.style.ERROR(f'No image files found in {media_dir}!'))
            return
        
        self.stdout.write(f'Found {len(image_files)} image files: {image_files}')
        
        # Sample movie data to use with the images
        movies_data = [
            {
                'name': 'Tourist Family',
                'rating': 8.5,
                'cast': 'Amitabh Bachchan, Jaya Bachchan, Abhishek Bachchan',
                'description': 'A heartwarming family drama about a tourist family exploring new destinations and discovering the true meaning of togetherness.'
            },
            {
                'name': 'Thug Life',
                'rating': 7.8,
                'cast': 'Aamir Khan, Katrina Kaif, Amitabh Bachchan',
                'description': 'An action-packed thriller about a reformed criminal who must protect his family from his dark past.'
            },
            {
                'name': 'Retro Movie',
                'rating': 8.2,
                'cast': 'Shah Rukh Khan, Deepika Padukone, Priyanka Chopra',
                'description': 'A nostalgic journey through the golden era of cinema, celebrating the magic of classic films.'
            },
            {
                'name': 'Maa Man Main',
                'rating': 8.7,
                'cast': 'Alia Bhatt, Ranbir Kapoor, Neetu Kapoor',
                'description': 'A touching story about the unbreakable bond between a mother and her child, exploring themes of love and sacrifice.'
            },
            {
                'name': 'Ace',
                'rating': 8.0,
                'cast': 'Hrithik Roshan, Deepika Padukone, Amitabh Bachchan',
                'description': 'A high-stakes thriller about a master strategist who must outsmart his enemies in a deadly game of cat and mouse.'
            }
        ]
        
        created_movies = []
        
        # Create movies with the actual image files
        for i, image_file in enumerate(image_files):
            if i < len(movies_data):
                movie_data = movies_data[i]
                
                # Create the movie with the actual image file
                movie, created = Movie.objects.get_or_create(
                    name=movie_data['name'],
                    defaults={
                        'image': f'movies/{image_file}',
                        'rating': movie_data['rating'],
                        'cast': movie_data['cast'],
                        'description': movie_data['description']
                    }
                )
                
                if created:
                    self.stdout.write(f'Created movie: {movie.name} with image: {image_file}')
                else:
                    self.stdout.write(f'Movie already exists: {movie.name}')
                
                created_movies.append(movie)
        
        # Create theaters for each movie
        theater_names = ['PVR Cinemas', 'INOX', 'Cinepolis', 'Regal Cinemas', 'AMC Theaters']
        theaters = []
        
        for movie in created_movies:
            for i in range(2):  # 2 theaters per movie
                theater_name = f"{random.choice(theater_names)} - {movie.name[:20]}"
                show_time = datetime.now() + timedelta(days=random.randint(1, 30), hours=random.randint(10, 22))
                
                theater, created = Theater.objects.get_or_create(
                    name=theater_name,
                    movie=movie,
                    defaults={'time': show_time}
                )
                theaters.append(theater)
                if created:
                    self.stdout.write(f'Created theater: {theater.name}')
        
        # Create seats for each theater
        seat_rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        seat_numbers = list(range(1, 11))  # 1-10
        
        for theater in theaters:
            for row in seat_rows:
                for num in seat_numbers:
                    seat_number = f"{row}{num}"
                    seat, created = Seat.objects.get_or_create(
                        theater=theater,
                        seat_number=seat_number,
                        defaults={'is_booked': random.choice([True, False])}  # Randomly book some seats
                    )
                    if created:
                        self.stdout.write(f'Created seat: {seat_number} for {theater.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created movies with actual image files!')
        )
        self.stdout.write(f'Created {len(created_movies)} movies')
        self.stdout.write(f'Created {len(theaters)} theaters')
        self.stdout.write(f'Created {len(seat_rows) * len(seat_numbers) * len(theaters)} seats') 