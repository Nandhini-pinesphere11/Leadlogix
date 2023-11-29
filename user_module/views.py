
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = None  # Initialize the user variable

        # Try to authenticate the user with the provided credentials
        if User.objects.filter(username=username).exists():
            user = auth.authenticate(username=username, password=password)
        else:
            user = User.objects.filter(email=username).first()
            if user:
                user = auth.authenticate(username=user.username, password=password)

        if user is not None:
            auth.login(request, user)
           
            return redirect('index1')  # Replace 'home' with the URL name of your desired landing page after login
        else:
            messages.error(request, "Invalid username or password.")  # Set the error message
            return redirect('login')  # Replace 'login' with the URL name of your login page

    else:
        messages.get_messages(request)  # Clear any messages from previous requests
        return render(request, "Login/index.html")

 

def logout(request):
    auth.logout(request)
    return redirect('login')  # Replace 'login' with the URL name of your login page