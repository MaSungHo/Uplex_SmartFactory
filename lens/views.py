from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.http import *
from .models import Image
from .forms import ImageForm
from pathlib import Path
import requests
import os, json
from django.core.exceptions import ImproperlyConfigured

from .models import Instance

BASE_DIR = Path(__file__).resolve().parent.parent
secret_file = os.path.join(BASE_DIR, 'secrets.json') # secrets.json 파일 위치

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

# Create your views here.
def index(request):
    return render(request, 'lens/index.html')

def predict(request):
    return render(request, 'lens/predict.html')

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

    predicted_res = requests.post(get_secret("API_PATH"), headers = headers, data = json.dumps(params)).json()
    ins.predicted=predicted_res['predicted'][0]
    ins.save()

    return HttpResponseRedirect(reverse('lens:results', args=(ins.id, )))

def image(request):
    return render(request, 'lens/image.html')

def decision(request):
    image_form = ImageForm(request.POST, request.FILES)
    if request.method == 'POST':
        if image_form.is_valid():
            image = Image(image=request.FILES['image'])
            image.save()
            return render(request, 'lens/decision.html', {'image': image})
        else:
            raise Http404('올바르지 않은 요청입니다.')
    else:
        raise Http404('올바르지 않은 요청입니다.')

def results(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    return render(request, 'lens/result.html', {'instance': instance})
