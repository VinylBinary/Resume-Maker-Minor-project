from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponseNotFound
from faunadb import query as q
import pytz
from faunadb.objects import Ref
from faunadb.client import FaunaClient
import hashlib
import datetime
from django.contrib.auth.models import User
from .models import resume_index
from django.contrib.auth import authenticate, login



client = FaunaClient(secret="fnAE5xxjPIACWtFG3s-fqA99TA8L8hSi1NfeOmeQ")
indexes = client.query(q.paginate(q.indexes()))

# Create your views here.
def index(request):
    return render(request,"index.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username").strip().lower()
        password = request.POST.get("password")

        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                print(user.id)
                request.session["user"] = {
                    "username": username,
                    "id":user.id
                }
                return redirect("App:index")
            else:
                messages.add_message(request, messages.INFO,"You have supplied invalid login credentials, please try again!", "danger")
                return redirect("App:login")
                
        except:
            messages.add_message(request, messages.INFO, "Account does not exist, please register first!", "danger")
            raise redirect("App:register")
            
    return render(request,"login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username").strip().lower()
        email = request.POST.get("email").strip().lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
            if user is not None:
                messages.add_message(request, messages.INFO, 'User already exists with that username.')
                return redirect("App:register")
            # messages.add_message(request, messages.INFO, 'User already exists with that username.')
            # return redirect("App:login")
        except:
            user = User.objects.create_user(username, email, password)
            messages.add_message(request, messages.INFO, 'Registration successful.')
            return redirect("App:login")
    return render(request,"register.html")

def create_resume(request):
    # print(request.user)
    user = User.objects.get(id = request.session["user"]["id"])
    print(user)
    if request.method=="POST":
        username=request.session["user"]["username"]
        full_name=request.POST.get("name")
        address=request.POST.get("address")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        about_you=request.POST.get("about")
        education=request.POST.get("education")
        career=request.POST.get("career")
        job_1__start=request.POST.get("job-1__start")
        job_1__end=request.POST.get("job-1__end")
        job_1__details=request.POST.get("job-1__details")
        job_2__start=request.POST.get("job-2__start")
        job_2__end=request.POST.get("job-2__end")
        job_2__details=request.POST.get("job-2__details")
        job_3__start=request.POST.get("job-3__start")
        job_3__end=request.POST.get("job-3__end")
        job_3__details=request.POST.get("job-3__details")
        references=request.POST.get("references")
        try:
            if resume_index.objects.filter(user = user).exists():
                n = resume_index.objects.get(user = user)
                n.data = {
                        "user":username,
                        "full_name": full_name,
                        "address": address,
                        "phone": phone,
                        "email":email,
                        "about_you":about_you,
                        "education":education,
                        "career":career,
                        "job_1__start":job_1__start,
                        "job_1__end":job_1__end,
                        "job_1__details":job_1__details,
                        "job_2__start":job_2__start,
                        "job_2__end":job_2__end,
                        "job_2__details":job_2__details,
                        "job_3__start":job_3__start,
                        "job_3__end":job_3__end,
                        "job_3__details":job_3__details,
                    }
                n.save()
                messages.add_message(request, messages.INFO, 'Resume Info Updated Successfully')
                return redirect("App:create-resume")
            else:
                quiz = resume_index.objects.create(user = user,
                    data =  {
                        "user":username,
                        "full_name": full_name,
                        "address": address,
                        "phone": phone,
                        "email":email,
                        "about_you":about_you,
                        "education":education,
                        "job_1__start":job_1__start,
                        "job_1__end":job_1__end,
                        "job_1__details":job_1__details,
                        "job_2__start":job_2__start,
                        "job_2__end":job_2__end,
                        "job_2__details":job_2__details,
                        "job_3__start":job_3__start,
                        "job_3__end":job_3__end,
                        "job_3__details":job_3__details,
                    }
                )
                messages.add_message(request, messages.INFO, 'Resume created Successfully.')
                return redirect("App:create-resume")
        except Exception as e:
            print("Error: ", e)

            messages.add_message(request, messages.INFO, 'There was an error while saving your resume info. Please try again.')
            return redirect("App:create-resume")
    else:
        try:   
            resume_info = resume_index.objects.get(user = user).data
            context={"resume_info":resume_info}
            print(resume_info)
            return render(request,"create-resume.html",context)
        except:
            return render(request,"create-resume.html")

def resume(request):
    try:
        resume_info = resume_index.objects.get(user = User.objects.get(id = request.session["user"]["id"])).data
        context={"resume_info":resume_info}
        return render(request,"resume.html",context)
    except:
        return render(request,"resume.html")
