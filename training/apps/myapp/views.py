
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from .models import User, Trip
import bcrypt

def index(request):

    return render(request, 'myapp/index.html')

def register(request):

    print(request.POST)
    errors = User.objects.register_validator(request.POST)

    if len(errors):
        for key, error in errors.items():
            messages.add_message(request, messages.ERROR, error, extra_tags='register')
        return redirect('/')

    else:
        password = request.POST['password']
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(name=request.POST['name'], username=request.POST['username'], password = password)
        request.session['user_id'] = user.id
        return redirect('/dash')

def login(request):
    print(request.POST)
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for key, error in errors.items():
            messages.add_message(request, messages.ERROR, error, extra_tags='login')
        return redirect('/')

    else:
        user = User.objects.get(username=request.POST['usernamelogin'])
        request.session['user_id'] = user.id
        return redirect('/dash')

def dash(request):

    if 'user_id' not in request.session:
        return redirect('/')
    else:
        other_trips = []
        all_trips = Trip.objects.all()
        mytrips = User.objects.get(id=request.session['user_id']).joined_travels.all()
        for trip in all_trips:
            if trip not in mytrips:
                other_trips.append(trip)

        context = {
            "trips": other_trips,
            "user" : User.objects.get(id= request.session['user_id']),
            "mytrips": mytrips,
        }
        return render(request, "myapp/dash.html", context)

def create(request):
    errors = Trip.objects.trip_validator(request.POST)
    if errors:
        for key, error in errors.items():
            messages.add_message(request, messages.ERROR, error)
        print(errors)
        return redirect('/new')
    else:
        print(request.POST)
        trip = Trip.objects.create(destination=request.POST["destination"], plan=request.POST["plan"],travel_start_date=request.POST['travel_start_date'],travel_end_date=request.POST['travel_end_date'], creater_id = request.session['user_id'])
        trip.joined_users.add(User.objects.get(id=request.session['user_id']))
        return redirect('/dash')

def new(request):
    return render(request, 'myapp/new.html')

def show(request, tripid):
    trip = Trip.objects.get(id=tripid)
    all_users = User.objects.all()
    creater = trip.creater
    users = []
    for user in all_users:
        if user != creater:
            users.append(user)
    context = {
    'trip': trip,
    'users': users,
    }
    return render(request, 'myapp/show.html', context)

def join(request, tripid):
    trip = Trip.objects.get(id=tripid)
    trip.joined_users.add(User.objects.get(id= request.session['user_id']))
    
    trip = Trip.objects.get(id=tripid)
    all_users = User.objects.all()
    creater = trip.creater
    users = []
    for user in all_users:
        if user != creater:
            users.append(user)
    context = {
    'trip': trip,
    'users': users,
    }
    return render(request, 'myapp/show.html', context)

def cancel(request, tripid):
    trip = Trip.objects.get(id=tripid)
    trip.joined_users.remove(User.objects.get(id=request.session['user_id']))
    return redirect('/dash')

def delete(request, tripid):
    Trip.objects.get(id=tripid).delete()
    return redirect ('/dash')


def logout(request):
    request.session.clear()
    return redirect('/')
