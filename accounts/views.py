from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from contacts.models import Contact

def register(requests):
    if requests.method == 'POST':
        # Get form values
        first_name = requests.POST['first_name']
        last_name = requests.POST['last_name']
        username = requests.POST['username']
        email = requests.POST['email']
        password = requests.POST['password']
        password2 = requests.POST['password2']

        # Check if password match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(requests, 'Username Taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(requests, 'That Email is being used.')
                    return redirect('register')
                else:
                    # Looks good
                    user = User.objects.create_user(username=username, password=password,
                                                    email=email, first_name=first_name, last_name=last_name)
                    #Login after register
                    # auth.login(requests, user)
                    # messages.success(requests, 'You are now logged in')
                    # return redirect('index')

                    user.save()
                    messages.success(requests, 'You are now registered and can log in.')
                    return redirect('login')
        else:
            messages.error(requests, 'Passwords do not match')
            return redirect('register')
    else:
        return render(requests, 'accounts/register.html')


def login(requests):
    if requests.method == 'POST':
        username = requests.POST['username']
        password = requests.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(requests, user)
            messages.success(requests, "You are now logged in ")
            return redirect('dashboard')
        else:
            messages.error(requests, 'Invalid Credentials')
            return redirect('login')
    else:
        # Login User
        return render(requests, 'accounts/login.html')


def logout(requests):
    if requests.method == "POST":
        auth.logout(requests)
        messages.success(requests, "You are now logged out.")
        return redirect('index')


def dashboard(requests):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=requests.user.id)

    context = {'contacts': user_contacts}
    return render(requests, 'accounts/dashboard.html', context)
