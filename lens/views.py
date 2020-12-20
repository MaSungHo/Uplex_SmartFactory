from django.shortcuts import render
from django.http import HttpResponse
from .models import Instance

# Create your views here.
def index(request):
    inst = Instance.objects.first()
    return HttpResponse(inst.trt_lot_no)

def detail(request, instance_id):
    return HttpResponse("You're looking at instance %i" %instance_id)

def results(request, instance_id):
    response = "You're looking at the results of instance %i"
    return HttpResponse(response %instance_id)
