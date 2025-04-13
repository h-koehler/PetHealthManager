from django.shortcuts import render, redirect
from django.template.defaultfilters import lower

from .models import pets, vetFeed, ownerFeed, owner_user, vet_user

# Create your views here.

def home_view(request):
    role = request.session.get('role')
    if role == 'vet':
        return render(request,
                      'pets/home/vet.html',
                      { "feed" : vetFeed }
                      )
    elif role == 'owner':
        return render(request,
                  "pets/home/owner.html",
                  { "feed" : ownerFeed }
                  )
    else:
        return redirect("pets:login")

def pets_view(request):
    if request.session.get('username'):
        return render(request,
                      "pets/pets-list/list.html",
                      { "pets" : pets }
                      )
    else:
        return redirect('pets:home')

def pet_details(request, pet_id):
    if request.session.get('username'):
        for pet in pets:
            if pet.id == pet_id:
                return render(request,
                              "pets/pets-list/details.html",
                              { "pet" : pet}
                              )
        # return error: page not found IF pet with specified id not found
    else:
        return redirect('pets:home')


def pet_create(request):
    if request.session.get('role') == 'owner' :
        return render(request,
                      "pets/pets-list/create.html")
    else:
        return redirect('pets:home')

def pet_edit(request, pet_id):
    if request.session.get('username'): # check if user is logged in
        if request.method == 'POST':
            return redirect('pets:details', pet_id)

        if request.method == 'GET':
            curr_pet = None

            for pet in pets:
                if pet.id == pet_id:
                    curr_pet = pet
                    # return render(request,"pets/pets-list/edit.html",{ "pet" : pet})
                # return error: page not found IF pet with specified id not found
            return render(request, "pets/pets-list/edit.html", {"pet" : curr_pet})
    else:
        return redirect('pets:home')

def pet_delete(request, pet_id):
    # delete pet from db
    return redirect('pets:home')

def login_view(request):
    if request.method == "GET":
        return render(request, "pets/home/login.html")
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == owner_user['username'] and password == owner_user['password']:
            request.session['username'] = username
            request.session['role'] = 'owner'
            return redirect('pets:home')
        elif username == vet_user['username'] and password == vet_user['password']:
            request.session['username'] = username
            request.session['role'] = 'vet'
            return redirect('pets:home')
        else:
            return redirect('pets:login')

def logout_view(request):
    request.session.flush()
    return redirect('pets:home')

def pet_search(request):
    if request.session.get('username'):
        # merge into pets_list view
        keyword = request.GET.get('query', '')
        lower_keyword = keyword.lower()
        results = []

        for pet in pets:
            if pet.name.lower().startswith(lower_keyword):
                results.append(pet)

        return render(request,
                      'pets/search/search.html',
                      { "results" : results })
    else:
        return redirect('pets:login')