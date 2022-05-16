from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Contact, PhoneNumber


# Create your views here.
# todo make an index page for login
def index(request):
    context = {'isSignUp': False}
    return render(request, 'address/index.html', context)


def home(request, user_id):
    contact_list = Contact.objects.order_by('last_name')  # todo insert filter on owner_id
    context = {'contact_list': contact_list,
               'user_id': user_id}
    return render(request, 'address/home.html', context)


def add(request, user_id):
    context = {'user_id': user_id}
    return render(request, 'address/add.html', context)


def detail(request, user_id, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    return render(request, 'address/detail.html', {'contact': contact})


# *** actions ***
def do_add(request, user_id):  # fixme verify fields not empty
    try:
        Contact.objects.create(first_name=request.POST['fName'],
                               last_name=request.POST['lName'],
                               email_address=request.POST['email'],
                               street_address=request.POST['street'], )
    except (KeyError, Contact.DoesNotExist):
        return render(request, 'address/add.html', {
            'error_message': "Field does not exist, report this bug to an admin.",
        })

    return HttpResponseRedirect(reverse('address:home'))


def do_edit(request, user_id, contact_id):
    # get contact
    old_contact = get_object_or_404(Contact, pk=contact_id)
    # edit contact
    try:
        old_contact.first_name = request.POST['fName']
        old_contact.last_name = request.POST['lName']
        old_contact.email_address = request.POST['email']
        old_contact.street_address = request.POST['street']
        old_contact.save()
    except (KeyError, Contact.DoesNotExist):
        return render(request, 'address/detail.html', {
            'contact': old_contact,
            'error_message': "Field does not exist, report this bug to an admin.",
        })

    return HttpResponseRedirect(reverse('address:home'))


def do_delete(request, user_id, contact_id):
    to_delete = Contact.objects.get(pk=contact_id)
    try:
        to_delete.delete()
    except (KeyError, Contact.DoesNotExist):
        return render(request, 'address/detail.html', {
            'old-contact': to_delete,
            'error_message': "Field does not exist, report this bug to an admin.",
        })
    return HttpResponseRedirect(reverse('address:home'))


def phone_add(request, user_id, contact_id):
    phone_type = request.POST['phoneTypes']
    phone_number = request.POST['phoneNumber']
    contact = Contact.objects.get(pk=contact_id)
    try:
        PhoneNumber.objects.create(contact_id=contact_id, type=phone_type, phone_number=phone_number)
    except (KeyError, Contact.DoesNotExist):
        return render(request, 'address/detail.html', {
            'error_message': "error in phone add",
        })
    return render(request, 'address/detail.html', {'contact': contact})


def phone_delete(request, user_id, contact_id, phonenumber_id):
    to_delete = PhoneNumber.objects.get(pk=phonenumber_id)
    contact = Contact.objects.get(pk=contact_id)
    try:
        to_delete.delete()
    except (KeyError, Contact.DoesNotExist):
        return render(request, 'address/detail.html', {
            'error_message': "error in phone delete",
        })
    return render(request, 'address/detail.html', {'contact': contact})


def sign_in(request):
    print()
    user = authenticate(request, username=request.POST['username'], password=request.POST['passKey'])
    if user is not None:
        # A backend authenticated the credentials
        pass
    else:
        user = User.objects.create_user(username=request.POST['username'],
                                        password=request.POST['passKey'], )
    return HttpResponseRedirect(reverse('address:home'))


def sign_out(request, user_id):
    return HttpResponseRedirect(reverse('address:index'))
