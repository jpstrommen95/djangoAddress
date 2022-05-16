from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Contact


# Create your views here.
# todo make an index page for login
def index(request):
    context = {}
    return render(request, 'address/index.html', context)


def home(request):
    contact_list = Contact.objects.order_by('last_name')  # todo insert filter on owner_id
    context = {'contact_list': contact_list}
    return render(request, 'address/home.html', context)


def detail(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    return render(request, 'address/detail.html', {'contact': contact})


def edit(request, contact_id):
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
        # Redisplay the question voting form.
        return render(request, 'address/detail.html', {
            'contact': old_contact,
            'error_message': "Field does not exist, report this bug to an admin.",
        })
    # delete phone numbers todo

    return HttpResponseRedirect(reverse('address:home'))

