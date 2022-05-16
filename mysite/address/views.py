from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
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


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
