from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Instance

# Create your views here.
def index(request):
    instance_list = Instance.objects.all()
    template = loader.get_template('lens/index.html')
    context = {
        'instance_list': instance_list,
    }
    return render(request, 'lens/index.html', context)

def create(request):
    instance = request.POST
    ins = Instance.objects.create(trt_lot_no = instance['trt_lot_no'], prt_lot_no = instance['prt_lot_no'],
        treat_mch_no = instance['treat_mch_no'], treat_trt_uptime = instance['treat_trt_uptime'],
        print_mch_no = instance['print_mch_no'], print_prt_uptime = instance['print_prt_uptime'],
        print_raw_mat = instance['print_raw_mat'], print_dry_no = instance['print_dry_no'],
        print_heat_treat = instance['print_heat_treat'], print_prd_type = instance['print_prd_type'],
        mold_snd_mch_no = instance['mold_snd_mch_no'], mold_snd_uptime = instance['mold_snd_uptime'],
        mold_snd_raw_mat = instance['mold_snd_raw_mat'], mold_snd_dry_no = instance['mold_snd_dry_no'],
        mold_snd_heat = instance['mold_snd_heat'], material_cd_no = instance['material_cd_no'],
        material_mat_nm = instance['material_mat_nm'], material_mat_emit_no = instance['material_mat_emit_no'])
    return HttpResponseRedirect(reverse('lens:detail', args=(ins.id,)))

def detail(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    return render(request, 'lens/detail.html', {'instance': instance})

def results(request, instance_id):
    response = "You're looking at the results of instance %i"
    return HttpResponse(response %instance_id)
