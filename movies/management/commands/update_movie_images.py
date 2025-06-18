from django.core.management.base import BaseCommand
from movies.models import Movie
import os

class Command(BaseCommand):
    help = 'Update movie images by matching movie names with image files'

    def handle(self, *args, **options):
        self.stdout.write('Updating movie images...')
        
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
        
        # Get all movies
        movies = Movie.objects.all()
        self.stdout.write(f'Found {movies.count()} movies in database')
        
        # Create a mapping of movie names to image files
        movie_image_mapping = {
            'Tourist Family': '238502-tourist.jpg',
            'Thug Life': 'Thug_life_NoFRb8D.webp',
            'Retro': 'retro_movie_S0ZNTXL.jpg',
            'Maaman': 'maaman.webp',
            'Ace': 'Ace_QstJFiX.webp',
        }
        
        updated_count = 0
        
        for movie in movies:
            if movie.name in movie_image_mapping:
                image_filename = movie_image_mapping[movie.name]
                image_path = f'movies/{image_filename}'
                
                # Check if the image file exists
                if os.path.exists(os.path.join(media_dir, image_filename)):
                    # Update the movie's image field
                    movie.image = image_path
                    movie.save()
                    self.stdout.write(f'Updated {movie.name} with image: {image_filename}')
                    updated_count += 1
                else:
                    self.stdout.write(self.style.WARNING(f'Image file not found for {movie.name}: {image_filename}'))
            else:
                self.stdout.write(self.style.WARNING(f'No image mapping found for movie: {movie.name}'))
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} movies with images!')
        )
        
        # Show current movie images
        self.stdout.write('\nCurrent movie images:')
        for movie in Movie.objects.all():
            self.stdout.write(f'- {movie.name}: {movie.image}') 