from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.http import *
from django.conf import settings
import joblib, pickle, sklearn, cv2, math, numpy as np
import io, urllib, base64
import matplotlib.pyplot as plt
from numba import jit
import PIL.Image as pilimg
from .models import Image
from .forms import ImageForm
from pathlib import Path
from influxdb import InfluxDBClient
import os, json, requests
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

  circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 400, param1 = 50, param2 = 25, minRadius = 400, maxRadius = 0)

  circles = np.uint16(np.around(circles))

  x, y, r = circles[0, :][0]
  rows, cols = img.shape

  for i in range(cols):
    for j in range(rows):
      if math.hypot(i - x, j - y) > r:
        img[j, i] = 0
  return img

# Create your views here.
def index(request):
  return render(request, 'lens/index.html')

def predict(request):
  return render(request, 'lens/predict.html')

def delete(request):
  for img in Image.objects.all():
    img.delete()
  return HttpResponseRedirect(reverse('lens:index'))

def results(request):
  instance = request.POST

  headers = {
    'Content-Type': 'application/json; charset=utf-8',
  }
  params = {
    "instance": {
    "trt_lot_no": instance['0'],
    "prt_lot_no": instance['1'],
    "treat.mch_no": instance['2'],
    "treat.trt_uptime": instance['3'],
    "print.mch_no": instance['4'],
    "print.prt_uptime": instance['5'],
    "print.raw_mat": instance['6'],
    "print.dry_no": instance['7'],
    "print.heat_treat": instance['8'],
    "print.prd_type": instance['9'],
    "mold.snd_mch_no": instance['10'],
    "mold.snd_uptime": instance['11'],
    "mold.snd_raw_mat": instance['12'],
    "mold.snd_dry_no": instance['13'],
    "mold.snd_heat": instance['14'],
    "material.cd_no": instance['15'],
    "material.mat_nm": instance['16'],
    "material.mat_emit_no": instance['17']
    }
  }

  res = requests.post(get_secret("API_PATH"), headers = headers, data = json.dumps(params)).json()
  prediction = res['predicted'][0] * 100

  return render(request, 'lens/result.html', {'prediction': prediction})

def select(request):
  return render(request, 'lens/select.html')

def single_image(request):
  return render(request, 'lens/single_image.html')

def group_images(request):
  return render(request, 'lens/group_images.html')

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

      return render(request, 'lens/single_decision.html', {'image': image, 'result': result[0]})
    else:
      raise Http404('올바르지 않은 요청입니다.')
  else:
    raise Http404('올바르지 않은 요청입니다.')

def decisions(request):
  images = []
  preprocess_images = []
  
  if request.method == 'POST':
    images = [Image(image = img) for img in request.FILES.getlist('images')]
    Image.objects.bulk_create(images)

    for image in images:
      img = cv2.imread(image.image.path, 0)
      img = blacking(img)
      img = cv2.resize(img, (512,512))
      img = img.reshape(512 * 512)
      preprocess_images.append(img)

    pca = joblib.load(os.path.join(settings.MEDIA_ROOT, 'PCA.pkl'))
    preprocess_images = pca.transform(preprocess_images)  
    svm = joblib.load(os.path.join(settings.MEDIA_ROOT, 'SVM_Model.pkl'))
    results = svm.predict(preprocess_images)

   

    return render(request, 'lens/group_decision.html', {'results': results})

def search(request):
  client = InfluxDBClient(host=get_secret("DB_HOST"), port=get_secret("DB_PORT"), username=get_secret("DB_USERNAME"),
    password=get_secret("DB_PASSWORD"), database=get_secret("DB_NAME"))
  res = dict(client.query('SELECT * FROM "sensors", "thermo", "dust"').raw)
  results = json.dumps(res)
  return render(request, 'lens/search.html', {'results': results})
    
