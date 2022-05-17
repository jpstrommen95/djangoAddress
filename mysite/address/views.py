from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError

from .models import Contact, PhoneNumber


# Create your views here.
def index(request):
    return render(request, 'address/index.html')


def home(request, user_id):
    contact_list = Contact.objects.filter(owner_id=user_id).order_by('last_name')
    try:
        search = request.POST['searchKey']
        if search is not None:
            contact_list = contact_list.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(email_address__icontains=search)
                | Q(street_address__icontains=search)
            )
    except MultiValueDictKeyError:
        pass  # fixme don't swallow this exception
    context = {'contact_list': contact_list,
               'user_id': user_id,
               'user': User.objects.get(pk=user_id), }
    return render(request, 'address/home.html', context)


def add(request, user_id):
    context = {'user_id': user_id}
    return render(request, 'address/add.html', context)


def detail(request, user_id, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    return render(request, 'address/detail.html', {'contact': contact, 'user_id': user_id})


# *** actions ***
def do_add(request, user_id):  # fixme verify fields not empty
    try:
        Contact.objects.create(owner_id=user_id,
                               first_name=request.POST['fName'],
                               last_name=request.POST['lName'],
                               email_address=request.POST['email'],
                               street_address=request.POST['street'], )
    except (KeyError, Contact.DoesNotExist):
        return render(request, 'address/add.html', {
            'error_message': "Field does not exist, report this bug to an admin.",
        })

    return HttpResponseRedirect(reverse('address:home', args=(user_id,)))


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

    return HttpResponseRedirect(reverse('address:home', args=(user_id,)))


def do_delete(request, user_id, contact_id):
    to_delete = Contact.objects.get(pk=contact_id)
    try:
        to_delete.delete()
    except (KeyError, Contact.DoesNotExist):
        return render(request, 'address/detail.html', {
            'old-contact': to_delete,
            'error_message': "Field does not exist, report this bug to an admin.",
        })
    return HttpResponseRedirect(reverse('address:home', args=(user_id,)))


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
    return render(request, 'address/detail.html', {'contact': contact, 'user_id': user_id})


def phone_delete(request, user_id, contact_id, phonenumber_id):
    to_delete = PhoneNumber.objects.get(pk=phonenumber_id)
    contact = Contact.objects.get(pk=contact_id)
    try:
        to_delete.delete()
    except (KeyError, Contact.DoesNotExist):
        return render(request, 'address/detail.html', {
            'error_message': "error in phone delete",
        })
    return render(request, 'address/detail.html', {'contact': contact, 'user_id': user_id})


def sign_in(request):
    try:
        user = authenticate(request, username=request.POST['username'], password=request.POST['passKey'])
        if user is not None:
            # A backend authenticated the credentials
            pass
        else:
            user = User.objects.create_user(username=request.POST['username'],
                                            password=request.POST['passKey'], )
    except IntegrityError:
        return render(request, 'address/index.html', {
            'error_message': "Could not log in, please check your credentials.",
        })
    return HttpResponseRedirect(reverse('address:home', args=(user.id,)))


def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('address:login'))
