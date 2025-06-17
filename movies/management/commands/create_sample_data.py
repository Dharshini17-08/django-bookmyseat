from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from movies.models import Movie, Theater, Seat
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Create sample data for the BookMySeat application'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample movies
        movies_data = [
            {
                'name': 'Avengers: Endgame',
                'rating': 8.4,
                'cast': 'Robert Downey Jr., Chris Evans, Mark Ruffalo',
                'description': 'After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos actions and restore balance to the universe.'
            },
            {
                'name': 'Spider-Man: No Way Home',
                'rating': 8.2,
                'cast': 'Tom Holland, Zendaya, Benedict Cumberbatch',
                'description': 'With Spider-Mans identity now revealed, Peter asks Doctor Strange for help. When a spell goes wrong, dangerous foes from other worlds start to appear, forcing Peter to discover what it truly means to be Spider-Man.'
            },
            {
                'name': 'The Batman',
                'rating': 7.8,
                'cast': 'Robert Pattinson, Zoë Kravitz, Paul Dano',
                'description': 'In his second year of fighting crime, Batman uncovers corruption in Gotham City that connects to his own family while facing a serial killer known as the Riddler.'
            },
            {
                'name': 'Dune',
                'rating': 8.0,
                'cast': 'Timothée Chalamet, Rebecca Ferguson, Oscar Isaac',
                'description': 'Feature adaptation of Frank Herberts science fiction novel about the son of a noble family entrusted with the protection of the most valuable asset and most vital element in the galaxy.'
            },
            {
                'name': 'No Time to Die',
                'rating': 7.3,
                'cast': 'Daniel Craig, Ana de Armas, Rami Malek',
                'description': 'James Bond has left active service. His peace is short-lived when Felix Leiter, an old friend from the CIA, turns up asking for help, leading Bond onto the trail of a mysterious villain armed with dangerous new technology.'
            }
        ]
        
        movies = []
        for movie_data in movies_data:
            movie, created = Movie.objects.get_or_create(
                name=movie_data['name'],
                defaults=movie_data
            )
            movies.append(movie)
            if created:
                self.stdout.write(f'Created movie: {movie.name}')
        
        # Create sample theaters
        theater_names = ['PVR Cinemas', 'INOX', 'Cinepolis', 'Regal Cinemas', 'AMC Theaters']
        theaters = []
        
        for movie in movies:
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
            self.style.SUCCESS('Successfully created sample data!')
        )
        self.stdout.write(f'Created {len(movies)} movies')
        self.stdout.write(f'Created {len(theaters)} theaters')
        self.stdout.write(f'Created {len(seat_rows) * len(seat_numbers) * len(theaters)} seats') 