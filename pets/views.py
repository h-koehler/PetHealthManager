from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import lower
from django.db.models import Q
from .models import owner_user, vet_user, Pet, User, Condition, Vaccine, FeedItem


# Create your views here.

def home_view(request):
    role = request.session.get('role')
    if role == 'vet':
        vet_feed = FeedItem.objects.filter(
            feed_type='inq',
            isSolved=False,
        ).order_by('-dateCreated')
        return render(request,
                      'pets/home/vet.html',
                      {"feed": vet_feed}
                      )
    elif role == 'owner':
        username = request.session.get('username')
        user = get_object_or_404(User, username=username)
        owner_feed = FeedItem.objects.filter(Q(pet__owner=user) | Q(pet__nonOwners=user), feed_type="gen").order_by('-dateCreated')
        return render(request,
                      "pets/home/owner.html",
                      {"feed": owner_feed}
                      )
    else:
        return redirect("pets:login")


def pets_view(request):
    if not request.session.get('username'):
        return redirect('pets:home')
    username = request.session.get('username')
    user = get_object_or_404(User, username=username)

    sort = request.GET.get('sort', 'updated')

    sort_map = {
        'updated' : '-lastUpdated',
        'name' : 'name',
        'dob-ascending' : '-dob',
        'dob-descending' : 'dob',
    }
    order_by = sort_map.get(sort, '-lastUpdated')
    pets = None
    if request.session.get('role') == 'owner':
        pets = Pet.objects.filter(Q(owner=user)).order_by(order_by)
    clients = Pet.objects.filter(Q(nonOwners=user)).order_by(order_by)
    return render(request,
                  "pets/pets-list/list.html",
                  {
                      "pets": pets,
                      "clients": clients,
                      "sort" : sort,
                  })


def pet_details(request, pet_id):
    if request.session.get('username'):
        pet = get_object_or_404(Pet, id=pet_id)
        if pet:
            conditions = Condition.objects.filter(pet_id=pet_id)
            vaccines = Vaccine.objects.filter(pet_id=pet_id)
            return render(request,
                          "pets/pets-list/details.html",
                          {
                              "pet": pet,
                              "conditions": conditions,
                              "vaccines": vaccines
                          })
        # return error: page not found IF pet with specified id not found
    else:
        return redirect('pets:home')


def pet_create(request):
    if not request.session.get('role') == 'owner' or not request.session.get('username'):
        return redirect('pets:home')

    if request.method == "POST":
        # process form
        # check if vet already exists in db
        pet_vet, created = User.objects.get_or_create(
            email=request.POST['vet-email'],  # find by email
            defaults={
                'firstName': request.POST.get('vet-fname'),
                'lastName': request.POST.get('vet-lname'),
                'phone': request.POST.get('vet-phone'),
                'address': request.POST.get('vet-address'),
                'city': request.POST.get('vet-city'),
                'state': request.POST.get('vet-state'),
                'zipCode': request.POST.get('vet-zip'),
                'role': 'v',
            }
        )

        if created:
            pet_vet.save()

        pet_pfp = request.FILES.get('pet-pfp')

        pet_name = request.POST.get('pet-name')
        pet_type = request.POST.get('pet-type')[0]
        pet_breed = request.POST.get('pet-breed')
        pet_sex = request.POST.get('pet-sex')[0]
        pet_dob = request.POST.get('pet-dob')
        pet_wgt = request.POST.get('pet-wgt')
        pet_spay = request.POST.get('pet-spay-status')
        new_pet = Pet(
            name=pet_name,
            type=pet_type,
            breed=pet_breed,
            sex=pet_sex,
            dob=pet_dob,
            weight=pet_wgt,
            spayed=pet_spay == "true",
            vet=pet_vet,
            owner=User.objects.get(username=request.session.get('username')),
            pfp=pet_pfp
        )
        new_pet.save()
        new_pet.nonOwners.add(pet_vet)

        for key in request.POST:
            if key.startswith('condition-description-'):
                con_id = key.split('condition-description-')[-1]
                description = request.POST[key]
                title = request.POST.get(f'condition-title-{con_id}')

                if title and description:
                    Condition.objects.create(
                        pet=new_pet,
                        title=title,
                        description=description,
                    )
            if key.startswith('vac-name'):
                vac_id = key.split('vac-name-')[-1]
                name = request.POST[key]
                last = request.POST.get(f'last-done-{vac_id}')
                due = request.POST.get(f'next-due-{vac_id}')

                if name and last and due:
                    Vaccine.objects.create(
                        pet=new_pet,
                        name=name,
                        lastDone=last,
                        nextDue=due,
                    )

        return redirect('pets:pet-details', pet_id=new_pet.id)

    else:
        # display form
        return render(request,
                      "pets/pets-list/create.html")


def pet_edit(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.session.get('username'):  # check if user is logged in
        if request.method == 'POST':
            # check if user is the owner - different edit options
            if pet.get_user_relation(get_object_or_404(User, username=request.session.get('username'))) == 'owner':
                pet.name = request.POST.get("pet-name")
                pet.type = request.POST.get("pet-type")[0]
                pet.breed = request.POST.get("pet-breed")
                pet.sex = request.POST.get("pet-sex")[0]
                pet.dob = request.POST.get("pet-dob")
                pet.weight = request.POST.get("pet-wgt")
                pet.spayed = request.POST.get("pet-spay-status") == "true"
                if "pet-pfp" in request.FILES:
                    pet.pfp = request.FILES.get('pet-pfp')

                vet = pet.vet

                if vet.email == request.POST.get("vet-email"):
                    vet.firstName = request.POST.get("vet-fname")
                    vet.lastName = request.POST.get("vet-lname")
                    vet.phone = request.POST.get("vet-phone")
                    vet.address = request.POST.get("vet-address")
                    vet.city = request.POST.get("vet-city")
                    vet.state = request.POST.get("vet-state")
                    vet.zipCode = request.POST.get("vet-zip")
                    vet.save()
                else :
                    pet.nonOwners.remove(vet)
                    new_vet, created = User.objects.get_or_create(
                        email=request.POST['vet-email'],  # find by email
                        defaults={
                            'firstName': request.POST.get('vet-fname'),
                            'lastName': request.POST.get('vet-lname'),
                            'phone': request.POST.get('vet-phone'),
                            'address': request.POST.get('vet-address'),
                            'city': request.POST.get('vet-city'),
                            'state': request.POST.get('vet-state'),
                            'zipCode': request.POST.get('vet-zip'),
                            'role': 'v',
                        }
                    )
                    new_vet.save()
                    pet.vet = new_vet
                    pet.save()
                    pet.nonOwners.add(new_vet)



            pet.conditions.all().delete()
            for key in request.POST:
                if key.startswith("condition-title-"):
                    index = key.split("-")[-1]
                    title = request.POST.get(f"condition-title-{index}")
                    desc = request.POST.get(f"condition-description-{index}")
                    if title.strip():
                        Condition.objects.create(pet=pet, title=title, description=desc)

            pet.vaccines.all().delete()
            for key in request.POST:
                if key.startswith("vac-name-"):
                    index = key.split("-")[-1]
                    name = request.POST.get(f"vac-name-{index}")
                    last = request.POST.get(f"last-done-{index}") or None
                    next = request.POST.get(f"next-due-{index}") or None
                    if name.strip():
                        Vaccine.objects.create(pet=pet, name=name, lastDone=last, nextDue=next)

            return redirect("pets:pet-details", pet_id=pet.id)

        if request.method == 'GET':
            if pet:
                # return render(request,"pets/pets-list/edit.html",{ "pet" : pet})
                # return error: page not found IF pet with specified id not found
                conditions = Condition.objects.filter(pet_id=pet_id)
                vaccines = Vaccine.objects.filter(pet_id=pet_id)
                vet = get_object_or_404(User, id=pet.vet_id)
                relation = pet.get_user_relation(get_object_or_404(User, username=request.session.get('username')))
                return render(request,
                              "pets/pets-list/edit.html",
                              {
                                  "pet": pet,
                                  "conditions": conditions,
                                  "vaccines": vaccines,
                                  "vet": vet,
                                  "relation": relation,
                              })
    else:
        return redirect('pets:home')


def pet_delete(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        if pet.get_user_relation(get_object_or_404(User, username=request.session.get('username'))) == 'owner':
            pet.delete()
            return redirect('pets:pets-list')


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
        current_user = get_object_or_404(User, username=request.session.get('username'))
        pets = Pet.objects.filter(Q(owner=current_user) | Q(nonOwners=current_user))
        for pet in pets:
            if pet.name.lower().startswith(lower_keyword):
                results.append(pet)

        return render(request,
                      'pets/search/search.html',
                      {"results": results})
    else:
        return redirect('pets:login')