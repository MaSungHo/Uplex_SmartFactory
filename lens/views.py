from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.http import *
from django.conf import settings
import joblib
import pickle
import sklearn
import cv2
import math
from numba import jit
import PIL.Image as pilimg
from .models import Image
from .forms import ImageForm
from pathlib import Path
from influxdb import InfluxDBClient
import requests
import os, json
import numpy as np
from django.core.exceptions import ImproperlyConfigured
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import PCA
from sklearn.svm import SVC


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

@jit
def blacking(img) :
  img = cv2.medianBlur(img,5)
  cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

  circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 400, param1=50, param2=25, minRadius=400, maxRadius=0)

  circles = np.uint16(np.around(circles))

  x, y, r = circles[0,:][0]
  rows, cols = img.shape

  for i in range(cols):
    for j in range(rows):
      if math.hypot(i-x, j-y) > r:
        img[j,i] = 0
  return img

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
    ins.predicted=predicted_res['predicted'][0] * 100
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

            img = cv2.imread(image.image.path, 0)
            img = blacking(img)
            img = cv2.resize(img, (512,512))
            img = img.reshape(512 * 512)
            source_img = []
            source_img.append(img)

            pca = joblib.load(os.path.join(settings.MEDIA_ROOT, 'PCA.pkl'))
            source_img = pca.transform(source_img)
            
            svm = joblib.load(os.path.join(settings.MEDIA_ROOT, 'SVM_Model.pkl'))
            result = svm.predict(source_img)

            return render(request, 'lens/decision.html', {'image': image, 'result': result[0]})
        else:
            raise Http404('올바르지 않은 요청입니다.')
    else:
        raise Http404('올바르지 않은 요청입니다.')

def search(request):
    client = InfluxDBClient(host=get_secret("DB_HOST"), port=get_secret("DB_PORT"), username=get_secret("DB_USERNAME"),
        password=get_secret("DB_PASSWORD"), database=get_secret("DB_NAME"))
    res = dict(client.query('SELECT * FROM "sensors", "thermo", "dust"').raw)
    results = json.dumps(res)
    return render(request, 'lens/search.html', {'results': results})

def results(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    return render(request, 'lens/result.html', {'instance': instance})
