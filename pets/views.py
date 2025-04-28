from datetime import datetime, date

from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone

from users.models import Vet
from .models import Pet, Condition, Vaccine, Comment
from actions.models import Action
from .templatetags.pets_tags import pretty_date, get_age_from_dob


# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        role = request.session.get('role')
        # if role == 'v':
        #     vet_feed = FeedItem.objects.filter(
        #         feed_type='inq',
        #         is_solved=False,
        #     ).order_by('-date_created')
        #     return render(request,
        #                   'pets/home/vet.html',
        #                   {"feed": vet_feed}
        #                   )
        if role == 'o':
            username = request.user.username
            user = get_object_or_404(User, username=username)

            feed = Action.objects.filter(
                Q(pet__owner=user) | Q(pet__non_owners=user)
            ).distinct().order_by('-created')

            return render(request,
                          "pets/home/owner.html",
                          {"feed": feed}
                          )
        elif role == 'a':
            feed = Action.objects.all().order_by('-created')
            return render(request,
                          "pets/home/owner.html",
                          {"feed": feed}
                          )
    else:
        return redirect("users:login")


def pet_popup(request):  # pet popup from vet home
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
    if request.user.is_authenticated:
        username = request.user.username
        user = get_object_or_404(User, username=username)

        sort = request.GET.get('sort', 'updated')

        sort_map = {
            'updated': '-last_updated',
            'name': 'name',
            'dob-ascending': '-dob',
            'dob-descending': 'dob',
        }
        order_by = sort_map.get(sort, '-last_updated')
        pets = None
        clients = None
        if request.session.get('role') == 'o':
            pets = Pet.objects.filter(Q(owner=user)).order_by(order_by)

        if request.session.get('role') == 'a':
            clients = Pet.objects.all().order_by(order_by)
        else:
            clients = Pet.objects.filter(Q(non_owners=user)).order_by(order_by)

        return render(request,
                      "pets/pets-list/list.html",
                      {
                          "pets": pets,
                          "clients": clients,
                          "sort": sort,
                      })

    return redirect('pets:home')


def pet_details(request, pet_id):
    if request.user.is_authenticated:
        pet = get_object_or_404(Pet, id=pet_id)
        if pet and (request.user in pet.non_owners.all() or request.user == pet.owner or request.session.get(
                'role') == 'a'):
            conditions = Condition.objects.filter(pet_id=pet_id)
            vaccines = Vaccine.objects.filter(pet_id=pet_id)
            excluded_ids = [pet.owner.id, request.user.id] + list(pet.non_owners.values_list('id', flat=True))
            users = User.objects.exclude(id__in=excluded_ids)
            comments = Comment.objects.filter(pet=pet).order_by('-posted')
            return render(request,
                          "pets/pets-list/details.html",
                          {
                              "pet": pet,
                              "conditions": conditions,
                              "vaccines": vaccines,
                              "users": users,
                              "comments": comments,
                          })
        # return error: page not found IF pet with specified id not found
    return redirect('pets:home')


def pet_share(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        if pet.owner != request.user:
            messages.error(request, 'You do not have permission to share this pet.')
            return redirect('pets:pet-details', pet_id)

        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)

        if user != pet.owner and user not in pet.non_owners.all():
            pet.non_owners.add(user)
            messages.success(request,
                             f"{pet.name} has successfully been shared with {user.first_name} {user.last_name}.")
            action = Action(
                user=request.user,
                pet=pet,
                verb=f'pet profile was shared with <a href="{user.details.get_absolute_url()}">{user.first_name} {user.last_name}</a>.',
                target=pet
            )
            action.save()

        else:
            messages.info(request, f"{pet.name} is already shared with {user.first_name} {user.last_name}.")

    return redirect('pets:pet-details', pet_id)


def pet_create(request):
    if not request.session.get('role') == 'o' or not request.user.username:
        return redirect('pets:home')

    if request.method == "POST":
        vet_id = request.POST.get('vet_select')

        if vet_id:
            vet = Vet.objects.get(id=vet_id)
        else:
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
                    'zip_code': request.POST.get('vet_zip'),
                    'phone': request.POST.get('vet_phone'),
                }
            )

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
            owner=User.objects.get(username=request.user.username),
            pfp=request.FILES.get('pet-pfp')
        )
        new_pet.save()

        if vet.user is not None:
            new_pet.non_owners.add(vet.user)

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

        new_pet.save()
        dob_date = datetime.strptime(new_pet.dob, '%Y-%m-%d')
        pet_sex = 'female'
        if new_pet.sex == 'm':
            pet_sex = 'male'

        action = Action(
            user=request.user,
            pet=new_pet,
            verb='pet profile was created',
            target=new_pet,
            description=f"{new_pet.name} is a {pet_sex} {new_pet.breed} that is {get_age_from_dob(dob_date)}"
        )
        action.save()

        # SUCCESS message
        messages.add_message(request, messages.SUCCESS, "%s has successfully been created" % new_pet.name)
        return redirect('pets:pet-details', pet_id=new_pet.id)

    else:
        # display form
        vets = Vet.objects.all()
        return render(request,
                      "pets/pets-list/create.html", {'vets': vets})


def format_value(val):
    if isinstance(val, (datetime, date)):
        return val.strftime("%b %d, %Y")

    if isinstance(val, str):
        try:
            parsed_date = datetime.strptime(val, "%Y-%m-%d")
            return parsed_date.strftime("%b %d, %Y")
        except ValueError:
            pass

    return str(val).strip()


def format_field(val):
    if val == 'dob':
        return 'birthday'
    if val == 'pfp':
        return 'profile picture'
    else:
        return val


def format_field_capitalize(val):
    if val == 'dob':
        return 'Birthday'
    if val == 'pfp':
        return 'Profile Picture'
    else:
        return val.capitalize()


def pet_edit(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.user.is_authenticated:  # check if user is logged in
        if request.method == 'POST':
            # check if user is the owner - different edit options
            if pet.get_user_relation(get_object_or_404(User, username=request.user.username)) == 'owner':
                old_pet = {
                    'name': pet.name,
                    'type': pet.type,
                    'breed': pet.breed,
                    'sex': pet.sex,
                    'pfp': pet.pfp,
                    'dob': pet.dob,
                    'weight': pet.weight,
                    'spayed': pet.spayed,
                    'vet': pet.vet,
                }
                old_vet = pet.vet
                selected_vet_id = request.POST.get('vet_select')

                if old_vet.id != selected_vet_id:
                    if selected_vet_id:
                        vet = Vet.objects.get(id=selected_vet_id)
                    else:
                        vet = Vet.objects.create(
                            email=request.POST.get('vet_email'),
                            first_name=request.POST.get('vet_fname'),
                            last_name=request.POST.get('vet_lname'),
                            clinic_name=request.POST.get('vet_clinic'),
                            address=request.POST.get('vet_address'),
                            city=request.POST.get('vet_city'),
                            state=request.POST.get('vet_state'),
                            zip_code=request.POST.get('vet_zip'),
                            phone=request.POST.get('vet_phone'),
                        )
                    pet.vet = vet
                    pet.save()

                    if old_vet.user is not None:
                        pet.non_owners.remove(old_vet.user)

                    if pet.vet.user is not None:
                        pet.non_owners.add(pet.vet.user)

                pet.name = request.POST.get("pet-name")
                pet.type = request.POST.get("pet-type")[0]
                pet.breed = request.POST.get("pet-breed")
                pet.sex = request.POST.get("pet-sex")[0]
                pet.dob = request.POST.get("pet-dob")
                pet.weight = request.POST.get("pet-wgt")

                if "pet-spay-status" in request.POST:
                    pet.spayed = request.POST.get("pet-spay-status") == "true"
                if "pet-pfp" in request.FILES:
                    pet.pfp = request.FILES.get('pet-pfp')

                pet.save()

                changes = []
                for field, old_value in old_pet.items():
                    new_value = getattr(pet, field)

                    if isinstance(old_value, (datetime, date)):
                        old_value = old_value.strftime("%Y-%m-%d")
                    if isinstance(new_value, (datetime, date)):
                        new_value = new_value.strftime("%Y-%m-%d")

                    if field == 'weight':
                        try:
                            old_value = float(old_value)
                            new_value = float(new_value)
                        except (TypeError, ValueError):
                            pass

                    if old_value != new_value:
                        changes.append((field, old_value, new_value))

                if changes:
                    if len(changes) == 1:
                        verb = ''
                        if changes[0][0] == 'pfp':
                            verb = f"{format_field(changes[0][0])} was changed"
                        elif changes[0][0] == 'vet':
                            old_vet = changes[0][1]
                            new_vet = changes[0][2]

                            if hasattr(old_vet, 'user') and old_vet.user:
                                old_vet_name = f'<a href="{old_vet.user.details.get_absolute_url()}">{old_vet.first_name} {old_vet.last_name}</a>'
                            else:
                                old_vet_name = f'{old_vet.first_name} {old_vet.last_name}'

                            if hasattr(new_vet, 'user') and new_vet.user:
                                new_vet_name = f'<a href="{new_vet.user.details.get_absolute_url()}">{new_vet.first_name} {new_vet.last_name}</a>'
                            else:
                                new_vet_name = f'{new_vet.first_name} {new_vet.last_name}'

                            verb = f"{format_field(changes[0][0])} was changed from {old_vet_name} -> {new_vet_name}"
                        else:
                            verb = f"{format_field(changes[0][0])} was changed from {format_value(changes[0][1])} -> {format_value(changes[0][2])}"

                        Action.objects.create(
                            user=User.objects.get(username=request.user),
                            pet=pet,
                            verb=verb,
                            target=pet,
                        )
                    else:
                        changes_desc = ''
                        for field, old_value, new_value in changes:
                            if field == 'pfp':
                                changes_desc += f"<li>{format_field_capitalize(field)} was updated</li>"
                            elif field == 'vet':
                                if hasattr(old_value, 'user') and old_value.user:
                                    old_vet_name = f'<a href="{old_value.user.details.get_absolute_url()}">{old_value.first_name} {old_value.last_name}</a>'
                                else:
                                    old_vet_name = f'{old_value.first_name} {old_value.last_name}'

                                if hasattr(new_value, 'user') and new_value.user:
                                    new_vet_name = f'<a href="{new_value.user.details.get_absolute_url()}">{new_value.first_name} {new_value.last_name}</a>'
                                else:
                                    new_vet_name = f'{new_value.first_name} {new_value.last_name}'

                                changes_desc += f"<li>{format_field_capitalize(field)}: {old_vet_name} -> {new_vet_name}</li>"
                            else:
                                changes_desc += f"<li>{format_field_capitalize(field)}: {format_value(old_value)} -> {format_value(new_value)}</li>"

                        changes_desc = "<ul>" + "".join(changes_desc) + "</ul>"

                        Action.objects.create(
                            user=User.objects.get(username=request.user),
                            pet=pet,
                            verb="pet profile was updated",
                            target=pet,
                            description=changes_desc
                        )

            # save conditions and vaccines
            old_conditions = list(pet.conditions.all())
            old_vaccines = list(pet.vaccines.all())

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
                    last = request.POST.get(f"last-done-{index}")
                    next_due = request.POST.get(f"next-due-{index}") or None

                    if name and last:
                        Vaccine.objects.create(pet=pet, name=name, last_done=last, next_due=next_due)

            new_conditions = list(pet.conditions.all())
            new_vaccines = list(pet.vaccines.all())

            condition_changes = []

            for cond in new_conditions:
                if not any(c.title == cond.title for c in old_conditions):
                    condition_changes.append(f"{cond.title} was added")

            for cond in old_conditions:
                if not any(c.title == cond.title for c in new_conditions):
                    condition_changes.append(f"{cond.title} was deleted")

            for cond in new_conditions:
                updated = next((c for c in old_conditions if c.title == cond.title), None)
                if updated and updated.description != cond.description:
                    condition_changes.append(f"{cond.title} was updated")

            vaccine_changes = []

            for vac in new_vaccines:
                if not any(v.name == vac.name for v in old_vaccines):
                    vaccine_changes.append(f"{vac.name} was added")

            for vac in old_vaccines:
                if not any(v.name == vac.name for v in new_vaccines):
                    vaccine_changes.append(f"{vac.name} was deleted")

            for vac in new_vaccines:
                matching_old = next((v for v in old_vaccines if v.name == vac.name), None)
                if matching_old and (matching_old.last_done != vac.last_done or matching_old.next_due != vac.next_due):
                    vaccine_changes.append(f"{vac.name} was updated")

            if condition_changes:
                if condition_changes:
                    Action.objects.create(
                        user=request.user,
                        pet=pet,
                        verb="conditions were updated",
                        target=pet,
                        description="<ul>" + "".join(f"<li>{change}</li>" for change in condition_changes) + "</ul>",
                    )

            if vaccine_changes:
                if vaccine_changes:
                    Action.objects.create(
                        user=request.user,
                        pet=pet,
                        verb="vaccines were updated",
                        target=pet,
                        description="<ul>" + "".join(f"<li>{change}</li>" for change in vaccine_changes) + "</ul>",
                    )

            pet.save(update_fields=[
                'last_updated'])  # make sure lastUpdated changes when only conditions / vaccines are changed

            # INFO message
            messages.add_message(request, messages.INFO,
                                 "Changes to %s have successfully been saved" % pet.name)

            return redirect("pets:pet-details", pet_id=pet.id)

        if request.method == 'GET':
            if pet:
                conditions = Condition.objects.filter(pet_id=pet_id)
                vaccines = Vaccine.objects.filter(pet_id=pet_id)
                vet = get_object_or_404(Vet, id=pet.vet_id)
                vets = Vet.objects.all()
                relation = pet.get_user_relation(get_object_or_404(User, username=request.user.username))
                return render(request,
                              "pets/pets-list/edit.html",
                              {
                                  "pet": pet,
                                  "conditions": conditions,
                                  "vaccines": vaccines,
                                  "vet": vet,
                                  'vets': vets,
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
        if pet.get_user_relation(get_object_or_404(User, username=request.user.username)) == 'owner':
            pet.delete()
            # deleted message
            messages.add_message(request, messages.WARNING,
                                 "%s has successfully been deleted" % pet.name)

            return redirect('pets:pets-list')


def pet_search(request):
    if request.user.is_authenticated:
        # merge into pets_list view
        keyword = request.GET.get('query', '')
        lower_keyword = keyword.lower()
        results = []
        current_user = get_object_or_404(User, username=request.user.username)
        pets = Pet.objects.filter(Q(owner=current_user) | Q(non_owners=current_user))
        for pet in pets:
            if pet.name.lower().startswith(lower_keyword):
                results.append(pet)

        return render(request,
                      'pets/search/search.html',
                      {"results": results})
    else:
        return redirect('users:login')


def pet_create_comment(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if pet.get_user_relation(get_object_or_404(User, username=request.user.username)) != 'unauthorized':
        if request.method == 'POST':  # create comment
            content = request.POST.get('comment')
            new_comment = Comment.objects.create(user=request.user, pet=pet, content=content)
            new_comment.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Comment has successfully been added.")
            return redirect('pets:pet-details', pet_id=pet.id)
    else:
        messages.add_message(request, messages.WARNING,
                             "You do not have permission to comment on this pet profile.")
        return redirect('pets:pet-details', pet_id=pet.id)


def pet_delete_comment(request, pet_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user and comment.user.id == request.user.id:
        if request.method == 'POST':  # edit comment
            if request.POST.get('_method') == 'DELETE':
                comment.delete()
                messages.add_message(request, messages.WARNING,
                                     "Comment has been deleted.")
                return redirect('pets:pet-details', pet_id=pet_id)
    else:
        messages.add_message(request, messages.WARNING,
                             "You do not have permission to make changes to this comment.")
        return redirect('pets:pet-details', pet_id=pet_id)

def pet_edit_comment(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'GET':
            comment_id = request.GET.get('comment_id')
            comment = Comment.objects.get(id=comment_id)
            return (JsonResponse({
                'id': comment.id,
                'content': comment.content,
            }))
        if request.method == 'POST':
            comment_id = request.POST.get('comment_id')
            comment = Comment.objects.get(id=comment_id)
            new_content = request.POST.get('content')
            comment.content = new_content
            comment.edited = timezone.now()
            comment.save()
            return (JsonResponse({
                'content': comment.content,
            }))
