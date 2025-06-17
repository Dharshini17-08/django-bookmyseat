# BookMySeat - Movie Ticket Booking System

A modern Django-based web application for booking movie tickets online. BookMySeat provides a complete movie ticket booking experience with user authentication, seat selection, and booking management.

## 🎬 Features

### Core Features
- **User Authentication**: Register, login, logout, and password reset functionality
- **Movie Catalog**: Browse and search through available movies
- **Theater Management**: View theaters and showtimes for each movie
- **Seat Selection**: Interactive seat selection with real-time availability
- **Booking System**: Book multiple seats with confirmation
- **Booking Management**: View and cancel existing bookings
- **Responsive Design**: Mobile-friendly interface

### Advanced Features
- **Seat Availability Indicator**: Real-time seat availability status
- **Interactive Seat Map**: Visual seat selection with hover effects
- **Booking Confirmation**: Detailed booking confirmation page
- **Profile Management**: Update user profile information
- **Admin Panel**: Complete admin interface for managing movies, theaters, and bookings

## 🛠️ Technology Stack

- **Backend**: Django 5.2.1
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 4
- **Icons**: Font Awesome
- **Deployment**: Vercel (Frontend) + Render (Backend)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd django-bookmyseat
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Create Sample Data (Optional)
```bash
python manage.py create_sample_data
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 📁 Project Structure

```
django-bookmyseat/
├── bookmyseat/          # Main Django project settings
├── movies/              # Movie booking app
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── urls.py          # URL routing
│   ├── admin.py         # Admin interface
│   └── management/      # Custom management commands
├── users/               # User authentication app
│   ├── models.py        # User models
│   ├── views.py         # Authentication views
│   ├── forms.py         # User forms
│   └── urls.py          # User URLs
├── templates/           # HTML templates
│   ├── home.html        # Homepage
│   ├── movies/          # Movie-related templates
│   └── users/           # User-related templates
├── static/              # Static files (CSS, JS, images)
├── media/               # User-uploaded files
├── requirements.txt     # Python dependencies
├── vercel.json          # Vercel deployment config
└── build_files.sh       # Build script
```

## 🎯 Usage Guide

### For Users

1. **Registration/Login**
   - Visit the homepage and click "Register" or "Login"
   - Create an account or sign in with existing credentials

2. **Browse Movies**
   - View featured movies on the homepage
   - Use the search function to find specific movies
   - Click on any movie to view available theaters

3. **Book Tickets**
   - Select a theater and showtime
   - Choose your preferred seats from the interactive seat map
   - Confirm your booking
   - Receive booking confirmation

4. **Manage Bookings**
   - View all your bookings in your profile
   - Cancel bookings if needed
   - Update your profile information

### For Administrators

1. **Access Admin Panel**
   - Go to `/admin/` and login with superuser credentials

2. **Manage Content**
   - Add/edit movies with images, ratings, and descriptions
   - Create theaters and assign showtimes
   - Monitor bookings and user activity

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=your-database-url
```

### Database Configuration
The application supports both SQLite (development) and PostgreSQL (production):

```python
# Development (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Production (PostgreSQL)
DATABASES = {
    'default': dj_database_url.parse('your-postgresql-url')
}
```

## 🚀 Deployment

### Vercel Deployment
1. Connect your GitHub repository to Vercel
2. Configure build settings:
   - Build Command: `./build_files.sh`
   - Output Directory: `staticfiles`
3. Set environment variables in Vercel dashboard
4. Deploy!

### Render Deployment
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn bookmyseat.wsgi:application`
5. Configure environment variables
6. Deploy!

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📝 API Endpoints

- `GET /` - Homepage
- `GET /movies/` - Movie list
- `GET /movies/theater/<movie_id>/` - Theater list for a movie
- `GET /movies/book/<theater_id>/` - Seat selection
- `POST /movies/book/<theater_id>/` - Book seats
- `GET /profile/` - User profile
- `GET /login/` - Login page
- `GET /register/` - Registration page

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap for the UI framework
- Font Awesome for icons
- Vercel and Render for hosting

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team

---

**BookMySeat** - Making movie ticket booking simple and enjoyable! 🎬✨ 
