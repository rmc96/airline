from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

from .models import Flight, Passenger

# Create your views here.

def index(request):
    return render(request, "flights/index.html",{
        "flights": Flight.objects.all()
    })

# def flight(request, flight_id):
#     flight = Flight.objects.get(pk=flight_id)
#     print(flight)
#     return render(request,"flights/flight.html",{
#         "flight":flight, 
#         "passengers": flight.passengers.all(),
#         "non_passengers":Passenger.objects.exclude(flights = flight).all()
#     })

def flight(request, flight_id):
    try:
        # Attempt to retrieve the flight with the given ID
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        # If the flight doesn't exist, return a 404 Not Found response
        return HttpResponseNotFound("Flight not found")

    # Render the flight details template with the retrieved flight object
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })

def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flight",args=(flight.id,)))



