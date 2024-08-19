from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Movie, MovieList
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import re
from django.shortcuts import get_object_or_404
# Create your views here.
@login_required(login_url='login')
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'index.html',context)

def add_to_list(request):
    if request.method == 'POST':
        movie_url_id = request.POST.get('movie_id')
        
        uuid_pattern =  r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        match = re.search(uuid_pattern, movie_url_id)
        movie_id = match.group() if match else None
        
        movie = get_object_or_404(Movie,uu_id = movie_id)
        movie_list ,created = MovieList.objects.get_or_create(owner_user = request.user, movie = movie) 

        if created:
            response_data = {'status': 'Success', 'message' : 'Movie created successfully!'}
        else:
            response_data = {'status': 'info', 'message' : 'Movie already added!'}

        return JsonResponse(response_data)
    else:
        response_data = {'status': 'error', 'message' : 'Something went wrong!'}
        return JsonResponse(response_data, status = 400)

def userlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username,password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,'Invalid username or password')
            return redirect('/login')
    else:
        return render(request, 'login.html')

def usersignup(request):
    # If recieve POST from website then get the user information
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        repass = request.POST['password2']

        #Check for password, username, email
        if password == repass:
            if User.objects.filter(email =email).exists() or User.objects.filter(username =username).exists():
                messages.info(request, 'Email or Username already exists!')
                return redirect('signup')
            else:
                #Create new user if pass the checking
                user = User.objects.create_user(username = username, email = email, password = password)
                user.save()
                user_login = auth.authenticate(username = username, password = password)
                auth.login(request,user_login)
                return redirect('/')
        else:
            messages.info(request,'Password not match!')
            return redirect('signup')
    else:
        return render(request, 'signup.html')
    
@login_required(login_url='login')
def movie(request,pk):
    movie_uuid = pk
    movie_details = Movie.objects.get(uu_id = movie_uuid)

    context = {
        'movie_details': movie_details
    }
    return render(request,'movie.html',context)

def genre(request):
    pass

@login_required(login_url='login')
def my_list(request):
    movie_list = MovieList.objects.filter(owner_user = request.user)
    user_list = []
    for movie in movie_list:
        user_list.append(movie.movie)
    context = {
        "movies": user_list
    }
    return render(request,'my_list.html', context)

@login_required(login_url='login')
def search(request):
    pass

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')