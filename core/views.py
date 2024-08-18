from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Movie
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def index(request):
    movies = Movie.objects.all()
    context = {
        'movie': movies,
    }
    return render(request, 'index.html',context)

def add_to_list(request):
    pass

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
    return render(request,'movie',context)

def genre(request):
    pass

def my_list(request):
    pass

def search(request):
    pass