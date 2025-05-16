from django.contrib.auth import authenticate, update_session_auth_hash, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User

from pets.models import Pet
from users.models import Vet


# Create your views here.

def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request,
                  'users/user/profile.html',
                  {'user': user})


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        role = request.POST.get('role')

        user = User.objects.create_user(
            username=request.POST.get('username'),
            first_name=request.POST.get('fname'),
            last_name=request.POST.get('lname'),
            email=email,
            password=request.POST.get('password')
        )

        details = user.details
        details.role = role
        details.phone = request.POST.get('phone')
        details.address = request.POST.get('address')
        details.city = request.POST.get('city')
        details.state = request.POST.get('state')
        details.zip_code = request.POST.get('zip')
        details.clinic_name = request.POST.get('clinic')
        details.save()

        if role == 'v':
            vet, created = Vet.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': request.POST.get('fname'),
                    'last_name': request.POST.get('lname'),
                    'phone': request.POST.get('phone'),
                    'clinic_name': request.POST.get('clinic'),
                    'address': request.POST.get('address'),
                    'city': request.POST.get('city'),
                    'state': request.POST.get('state'),
                    'zip_code': request.POST.get('zip'),
                }
            )
            vet.user = user
            vet.save()

            pets = Pet.objects.filter(vet=vet)
            for pet in pets:
                pet.non_owners.add(user)

            if created:
                messages.success(request, "Vet profile created and claimed successfully!")
            else:
                messages.success(request, "Existing vet profile claimed successfully!")

        login(request, user)
        request.session['role'] = user.details.role
        role_human = ""
        if user.details.role == 'o':
            role_human = "Owner"
        elif user.details.role == 'a':
            role_human = "Admin"
        elif user.details.role == 'v':
            role_human = "Vet"
        messages.add_message(request, messages.SUCCESS,
                             "You have successfully registered as a %s with the username: %s" % (
                             role_human, user.username))
        return redirect('pets:home')
    if request.method == 'GET':
        role = request.GET.get('role')
        return render(request, 'users/user/register.html', {'role': role})


def register_select(request):
    if request.method == 'GET':
        return render(request, 'users/user/register-type-select.html')
    if request.method == 'POST':
        return redirect('users:register', request.POST.get('role'))


def login_user(request):
    if request.method == "GET":
        return render(request, "pets/home/login.html")
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['role'] = user.details.role
            messages.add_message(request, messages.SUCCESS,
                                 "You have successfully logged in.")
            return redirect('pets:home')
        else:
            messages.add_message(request, messages.ERROR,
                                 "Invalid username or password.")
            return render(request, "pets/home/login.html")

def logout_user(request):
    logout(request)
    return redirect('pets:home')


def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    if user.username == request.user.username or request.session['role'] == 'a':
        if request.method == "POST":
            old_password = request.POST.get('old-password')
            new_password = request.POST.get('register-password')
            confirm_password = request.POST.get('confirm-password')

            user.first_name = request.POST.get('fname')
            user.last_name = request.POST.get('lname')
            user.email = request.POST.get('email')
            user.save()

            details = user.details
            details.phone = request.POST.get('phone')
            details.clinic_name = request.POST.get('clinic')
            details.address = request.POST.get('address')
            details.city = request.POST.get('city')
            details.state = request.POST.get('state')
            details.zip_code = request.POST.get('zip')
            details.save()
            user.save()

            if request.session.get('role') == 'v':
                vet = Vet.objects.get(user=user)
                if vet is not None:
                    vet.first_name = request.POST.get('fname')
                    vet.last_name = request.POST.get('lname')
                    vet.clinic_name = request.POST.get('clinic')
                    vet.address = request.POST.get('address')
                    vet.city = request.POST.get('city')
                    vet.state = request.POST.get('state')
                    vet.zip_code = request.POST.get('zip')
                    vet.phone = request.POST.get('phone')
                    vet.save()

            if old_password and new_password:
                if not user.check_password(old_password):
                    messages.add_message(request, messages.ERROR,
                                         "Old password is incorrect.")
                    return render(request, 'users/user/edit.html', {'user': user})

                if new_password != confirm_password:
                    messages.add_message(request, messages.ERROR,
                                         "New passwords do not match.")
                    return render(request, 'users/user/edit.html', {'user': user})

                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)

            messages.add_message(request, messages.SUCCESS,
                                 "Changes have been saved.")
            return redirect('users:profile', user.username)

        if request.method == "GET":
            if user:
                return render(request, "users/user/edit.html", {'user': user})

    else:
        return redirect('users:profile', user.username)


def update_role(request, user_id):
    user = get_object_or_404(User, id=user_id)
    new_role = request.POST.get('role')

    if not new_role:
        messages.add_message(request, messages.ERROR,
                             'No role selected for %s', user.username)

    old_role = user.details.role

    user.details.role = new_role
    user.details.save()
    role_human = ""
    if new_role == 'o':
        role_human = "Owner"
    elif new_role == 'a':
        role_human = "Admin"
    elif new_role == 'v':
        role_human = "Vet"
    messages.add_message(request, messages.SUCCESS,
                         f"{user.username}'s role has been updated to {role_human}")

    if old_role != 'v' and new_role == 'v':
        vet, created = Vet.objects.get_or_create(
            email=user.email,
            defaults={
                'user': user,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'address': user.details.address,
                'city': user.details.city,
                'state': user.details.state,
                'zip_code': user.details.zip_code,
                'phone': user.details.phone,
                'email': user.email,
            }
        )
        vet.save()
        if created:
            messages.add_message(request, messages.SUCCESS,
                             f"{user.username}'s vet profile has been created.")
        else:
            messages.add_message(request, messages.SUCCESS,
                                 f"{user.username}'s vet profile has been updated.")
    elif old_role == 'v' and new_role != 'v':
        vet = Vet.objects.get(user=user)
        vet.user = None
        vet.save()
        messages.add_message(request, messages.SUCCESS,
                             f"{user.username}'s vet profile has been disconnected.")

    return redirect('pets:home')
