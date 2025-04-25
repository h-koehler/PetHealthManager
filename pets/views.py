from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

from users.models import Vet
from .models import Pet, Condition, Vaccine, FeedItem


# Create your views here.

def home_view(request):
    role = request.session.get('role')
    if role == 'v':
        vet_feed = FeedItem.objects.filter(
            feed_type='inq',
            is_solved=False,
        ).order_by('-date_created')
        return render(request,
                      'pets/home/vet.html',
                      {"feed": vet_feed}
                      )
    elif role == 'o':
        username = request.session.get('username')
        # print("Session username:", username)

        user = get_object_or_404(User, username=username)
        # print("User object:", user, type(user))

        owner_feed = FeedItem.objects.filter(Q(pet__owner=user) | Q(pet__non_owners=user), feed_type="gen").order_by('-date_created')
        return render(request,
                      "pets/home/owner.html",
                      {"feed": owner_feed}
                      )
    elif role == 'a':
        return redirect('users:profile', request.session.get('username'))
    else:
        return redirect("users:login")

def pet_popup(request): # pet popup from vet home
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'GET':
            pet_id = request.GET.get('pet_id')
            conditions = [{
                'title': c.title,
                'description': c.description,
            } for c in Condition.objects.filter(pet_id=pet_id)]

            vaccines = [{
                'name': v.name,
                'last_done': v.last_done.strftime('%b %d, %Y') if v.last_done else 'N/A',
                'next_due': v.next_due.strftime('%b %d, %Y') if v.next_due else 'N/A'
            } for v in Vaccine.objects.filter(pet_id=pet_id)]

            return JsonResponse({
                'conditions': conditions,
                'vaccines': vaccines
            })

def pets_view(request):
    if not request.session.get('username'):
        return redirect('pets:home')
    username = request.session.get('username')
    user = get_object_or_404(User, username=username)

    sort = request.GET.get('sort', 'updated')

    sort_map = {
        'updated' : '-last_updated',
        'name' : 'name',
        'dob-ascending' : '-dob',
        'dob-descending' : 'dob',
    }
    order_by = sort_map.get(sort, '-last_updated')
    pets = None
    if request.session.get('role') == 'o':
        pets = Pet.objects.filter(Q(owner=user)).order_by(order_by)
    clients = Pet.objects.filter(Q(non_owners=user)).order_by(order_by)
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
    if not request.session.get('role') == 'o' or not request.session.get('username'):
        return redirect('pets:home')

    if request.method == "POST":
        vet_email = request.POST.get('vet_email')
        vet, _ = Vet.objects.get_or_create(
            email=vet_email,  # find by email
            defaults={
                'first_name': request.POST.get('vet_fname'),
                'last_name': request.POST.get('vet_lname'),
                'clinic_name': request.POST.get('vet_clinic'),
                'address': request.POST.get('vet_address'),
                'city': request.POST.get('vet_city'),
                'state': request.POST.get('vet_state'),
                'zip': request.POST.get('vet_zip'),
                'phone': request.POST.get('vet_phone'),
            }
        )

        vet.save()

        pet_spay = request.POST.get('pet-spay-status')
        new_pet = Pet(
            name=request.POST.get('pet-name'),
            type=request.POST.get('pet-type')[0],
            breed=request.POST.get('pet-breed'),
            sex=request.POST.get('pet-sex')[0],
            dob=request.POST.get('pet-dob'),
            weight=request.POST.get('pet-wgt'),
            spayed=pet_spay == "true",
            vet=vet,
            owner=User.objects.get(username=request.session.get('username')),
            pfp=request.FILES.get('pet-pfp')
        )
        new_pet.save()

        if vet.user:
            new_pet.non_owners.add(vet) # set pet's vet as a nonOwner - allows vet to see pet's profile

        for key in request.POST:
            # create conditions
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
            # create vaccines
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

        # SUCCESS message
        messages.add_message(request, messages.SUCCESS, "%s has successfully been created" % new_pet.name)
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
                pet.save()


                new_vet_email = request.POST.get('vet_email')

                if new_vet_email != pet.vet.email:
                    new_vet, _ = Vet.objects.get_or_create(
                        email=new_vet_email, defaults={
                            'first_name': request.POST.get('vet_fname'),
                            'last_name': request.POST.get('vet_lname'),
                            'clinic_name': request.POST.get('vet_clinic'),
                            'address': request.POST.get('vet_address'),
                            'city': request.POST.get('vet_city'),
                            'state': request.POST.get('vet_state'),
                            'zip': request.POST.get('vet_zip'),
                            'phone': request.POST.get('vet_phone'),
                        }
                    )
                    pet.non_owners.remove(pet.vet.user) if pet.vet.user else None
                    pet.vet = new_vet
                    if new_vet.user:
                        pet.non_owners.add(new_vet.user)

                    pet.save()

            # save conditions and vaccines
            pet.conditions.all().delete()
            for key in request.POST:
                if key.startswith("condition-title-"):
                    index = key.split("-")[-1]
                    title = request.POST.get(f"condition-title-{index}")
                    desc = request.POST.get(f"condition-description-{index}")
                    if title and desc:
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

            pet.save(update_fields=['last_updated']) # make sure lastUpdated changes when only conditions / vaccines are changed

            # INFO message
            messages.add_message(request, messages.INFO,
                                         "Changes to %s have successfully been saved" % pet.name)

            return redirect("pets:pet-details", pet_id=pet.id)

        if request.method == 'GET':
            if pet:
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

def pet_edit_condition(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'GET':
            condition_id = request.GET.get('condition_id')
            condition = Condition.objects.get(id=condition_id)
            return JsonResponse({
                'id': condition.id,
                'title': condition.title,
                'description': condition.description
            })
        if request.method == 'POST':
            condition_id = request.POST.get('condition_id')
            condition = Condition.objects.get(id=condition_id)
            new_description = request.POST.get('description')
            condition.description = new_description
            condition.save()
            return JsonResponse({'description': condition.description})


def pet_delete(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        if pet.get_user_relation(get_object_or_404(User, username=request.session.get('username'))) == 'owner':
            pet.delete()
            # deleted message
            messages.add_message(request, messages.WARNING,
                                 "%s has successfully been deleted" % pet.name)

            return redirect('pets:pets-list')


def pet_search(request):
    if request.session.get('username'):
        # merge into pets_list view
        keyword = request.GET.get('query', '')
        lower_keyword = keyword.lower()
        results = []
        current_user = get_object_or_404(User, username=request.session.get('username'))
        pets = Pet.objects.filter(Q(owner=current_user) | Q(non_owners=current_user))
        for pet in pets:
            if pet.name.lower().startswith(lower_keyword):
                results.append(pet)

        return render(request,
                      'pets/search/search.html',
                      {"results": results})
    else:
        return redirect('users:login')