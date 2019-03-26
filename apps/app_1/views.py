from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from datetime import datetime
import bcrypt

def index(request):
    if 'id' not in request.session:
        user = None
    else:
        user = User.objects.get(id=request.session['id'])
    context = {
        'user': user
    }
    return render(request, "app_1/index.html", context)

def registration (request):
    return render(request, "app_1/registration.html")

def login (request):
    return render(request, "app_1/login.html")
    
def register_user(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="registration")
        return redirect("/registration")
    else:
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        hash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        password = hash.decode()
        new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=password)

        request.session['id'] = new_user.id
        return redirect("/events")

def login_user(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="login")
        return redirect("/login")
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['id'] = user.id
        return redirect("/events")

def logout(request):
    if 'id' in request.session:
        del request.session['id']
    return redirect("/")

def events(request):
    if 'id' not in request.session:
        return redirect("/")
    user = User.objects.get(id=request.session['id'])
    my_trips = Trip.objects.filter(attendees=user)
    other_trips = Trip.objects.exclude(attendees=user)
    context = {
        'user': user,
        'my_trips': my_trips,
        'other_trips': other_trips
    }
    return render(request, "app_1/travels.html", context)

def view_trip(request, trip_id):
    if 'id' not in request.session:
        return redirect("/")
    user = User.objects.get(id=request.session['id'])
    trip = Trip.objects.get(id=int(trip_id))
    planner = trip.planner
    attendees = User.objects.filter(attending_trips=trip).exclude(planned_trips__planner=planner)
    context = {
        'user': user,
        'trip': trip,
        'attendees': attendees,
    }
    print(user.id)
    return render(request, "app_1/view_trip.html", context)

def cancel_trip(request, trip_id):
    if 'id' not in request.session:
        return redirect("/")
    user = User.objects.get(id=request.session['id'])
    trip = Trip.objects.get(id=int(trip_id))
    if trip.planner == user:
        pass
    else:
        trip.attendees.remove(user)
    return redirect("/events")

def delete_trip(request, trip_id):
    if 'id' not in request.session:
        return redirect("/")
    user = User.objects.get(id=request.session['id'])
    trip = Trip.objects.get(id=int(trip_id))
    trip.delete()
    return redirect("/events")

def join_trip(request, trip_id):
    if 'id' not in request.session:
        return redirect("/")
    user = User.objects.get(id=request.session['id'])
    trip = Trip.objects.get(id=int(trip_id))
    trip.attendees.add(user)
    return redirect("/events")

def add_event(request):
    if 'id' not in request.session:
        return redirect("/")
    return render(request, "app_1/addtrip.html")

def process_trip(request):
    if 'id' not in request.session:
        return redirect("/")
    user = User.objects.get(id=request.session['id'])
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="trip")
        return redirect("/addtrip")
    destination = request.POST['destination']
    description = request.POST['description']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    new_trip = Trip.objects.create(destination=destination, description=description, start_date=start_date, end_date=end_date, planner=user)
    new_trip.attendees.add(user)
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
        print("valid")
        # m = Trip.objects.get(id=course_id)
        new_trip.image = form.cleaned_data['image']
        new_trip.save()
    else:
        print("invalid")
    # return HttpResponse('image upload success')
    return redirect("/events")

def admin_page(request):
    if 'id' not in request.session:
        return redirect("/")
    user = User.objects.get(id=request.session['id'])
    if user.id != 10:
        return redirect('/')
    trips = Trip.objects.all()
    context = {
        'user': user,
        'trips': trips
    }
    return render(request, 'app_1/admin.html', context)