from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarMake
from .restapis import get_dealers_from_cf,get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

def login_request(request):
    context = {}
    url = "https://08663624.us-south.apigw.appdomain.cloud/api/dealership"
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pword']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            context["message"]="Username or password is incorrect."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


def logout_request(request):
    context = {}
    url = "https://08663624.us-south.apigw.appdomain.cloud/api/dealership"
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return render(request, 'djangoapp/index.html', context)

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pword']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context["message"]="Account could not be created try again."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/3da16fba-1f86-4a89-af73-d1d6a3db4c93/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


def get_dealer_details(request, dealer_id):
    context={}
    url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/3da16fba-1f86-4a89-af73-d1d6a3db4c93/dealership-package/get-review"
    apikey="nqgg3f0cV0dmeNiTcGdqNbF2rg1jSE9-2LfK1qXgf05k"
    dealer_details = get_dealer_reviews_from_cf(url,dealer_id)
    context["dealer_id"]=dealer_id
    context["reviews"]=dealer_details
    return render(request, 'djangoapp/dealer_details.html', context)
    
def add_review(request, dealer_id: int):
    if request.method == "GET":
        context = {
            "cars": CarModel.objects.all(),
            "dealer": get_dealers_from_cf(dealer_id)[0],
        }
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == "POST":
        form = request.POST
        review = {
            "name": f"{request.user.first_name} {request.user.last_name}",
            "dealership": dealer_id,
            "review": form["content"],
            "purchase": "true" if form.get("purchase_check") == 'on' else "false",
        }
        if form.get("purchase_check"):
            car = CarModel.objects.get(pk=form["car"])
            review["purchase_date"] = datetime.strptime(form.get("purchase_date"), "%m/%d/%Y").isoformat() 
            review["car_make"] = car.car_make.name
            review["car_model"] = car.name
            review["car_year"] = car.year.strftime("%Y")
          
        print(post_request(POST_DEALERSHIP_REVIEW_URL, review));
    
    return redirect("djangoapp:dealer_details", dealer_id=dealer_id)