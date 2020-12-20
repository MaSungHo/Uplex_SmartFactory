from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader

from .models import Instance

# Create your views here.
def index(request):
    instance_list = Instance.objects.all()
    template = loader.get_template('lens/index.html')
    context = {
        'instance_list': instance_list,
    }
    return render(request, 'lens/index.html', context)

def detail(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    return render(request, 'lens/detail.html', {'instance': instance})

def results(request, instance_id):
    response = "You're looking at the results of instance %i"
    return HttpResponse(response %instance_id)
