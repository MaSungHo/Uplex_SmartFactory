from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import requests

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
    ins = Instance.objects.create(trt_lot_no = instance['0'], prt_lot_no = instance['1'],
        treat_mch_no = instance['2'], treat_trt_uptime = int(instance['3']),
        print_mch_no = instance['4'], print_prt_uptime = int(instance['5']),
        print_raw_mat = instance['6'], print_dry_no = instance['7'],
        print_heat_treat = instance['8'], print_prd_type = instance['9'],
        mold_snd_mch_no = instance['10'], mold_snd_uptime = int(instance['11']),
        mold_snd_raw_mat = instance['12'], mold_snd_dry_no = instance['13'],
        mold_snd_heat = instance['14'], material_cd_no = instance['15'],
        material_mat_nm = instance['16'], material_mat_emit_no = instance['17'])

    headers = {
        'Content-Type': 'application/json; charset=utf-8',
    }
    params = {
        "instance": {
            "trt_lot_no": ins.trt_lot_no,
            "prt_lot_no": ins.prt_lot_no,
            "treat.mch_no": ins.treat_mch_no,
            "treat.trt_uptime": ins.treat_trt_uptime,
            "print.mch_no": ins.print_mch_no,
            "print.prt_uptime": ins.print_prt_uptime,
            "print.raw_mat": ins.print_raw_mat,
            "print.dry_no": ins.print_dry_no,
            "print.heat_treat": ins.print_heat_treat,
            "print.prd_type": ins.print_prd_type,
            "mold.snd_mch_no": ins.mold_snd_mch_no,
            "mold.snd_uptime": ins.mold_snd_uptime,
            "mold.snd_raw_mat": ins.mold_snd_raw_mat,
            "mold.snd_dry_no": ins.mold_snd_dry_no,
            "mold.snd_heat": ins.mold_snd_heat,
            "material.cd_no": ins.material_cd_no,
            "material.mat_nm": ins.material_mat_nm,
            "material.mat_emit_no": ins.material_mat_emit_no
        }
    }

    #predicted_res = requests.post("http://172.16.6.108:5000/uplex/predict")["predicted"][0]
    predicted_res = requests.post("http://175.123.142.155:38888").status_code
    ins.predicted=predicted_res
    ins.save()

    return HttpResponseRedirect(reverse('lens:results', args=(ins.id, )))

def detail(request, instance_id):
    return render(request, 'lens/detail.html', {'instance': instance})

def results(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    return render(request, 'lens/result.html', {'instance': instance})
