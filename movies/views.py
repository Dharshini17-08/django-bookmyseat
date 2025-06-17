from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect ,get_object_or_404
from .models import Movie,Theater,Seat,Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages

def movie_list(request):
    search_query=request.GET.get('search')
    if search_query:
        movies=Movie.objects.filter(name__icontains=search_query)
    else:
        movies=Movie.objects.all()
    return render(request,'movies/movie_list.html',{'movies':movies})

def theater_list(request,movie_id):
    movie = get_object_or_404(Movie,id=movie_id)
    theater=Theater.objects.filter(movie=movie)
    return render(request,'movies/theater_list.html',{'movie':movie,'theaters':theater})

@login_required(login_url='/login/')
def book_seats(request,theater_id):
    theaters=get_object_or_404(Theater,id=theater_id)
    seats=Seat.objects.filter(theater=theaters)
    
    if request.method=='POST':
        selected_Seats= request.POST.getlist('seats')
        error_seats=[]
        successful_bookings = []
        
        if not selected_Seats:
            messages.error(request, "Please select at least one seat.")
            return render(request,"movies/seat_selection.html",{'theaters':theaters,"seats":seats})
        
        for seat_id in selected_Seats:
            seat=get_object_or_404(Seat,id=seat_id,theater=theaters)
            if seat.is_booked:
                error_seats.append(seat.seat_number)
                continue
            try:
                booking = Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theaters.movie,
                    theater=theaters
                )
                seat.is_booked=True
                seat.save()
                successful_bookings.append(booking)
            except IntegrityError:
                error_seats.append(seat.seat_number)
        
        if error_seats:
            error_message=f"The following seats are already booked: {', '.join(error_seats)}"
            messages.error(request, error_message)
            return render(request,'movies/seat_selection.html',{'theaters':theaters,"seats":seats})
        
        if successful_bookings:
            messages.success(request, f"Successfully booked {len(successful_bookings)} seat(s)!")
            return redirect('booking_confirmation', booking_id=successful_bookings[0].id)
    
    return render(request,'movies/seat_selection.html',{'theaters':theaters,"seats":seats})

@login_required(login_url='/login/')
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'movies/booking_confirmation.html', {'booking': booking})

@login_required(login_url='/login/')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        # Free up the seat
        seat = booking.seat
        seat.is_booked = False
        seat.save()
        
        # Delete the booking
        booking.delete()
        
        messages.success(request, "Booking cancelled successfully!")
        return redirect('profile')
    
    return render(request, 'movies/cancel_booking.html', {'booking': booking})



