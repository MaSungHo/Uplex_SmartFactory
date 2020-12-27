# Uplex_SmartFactory

<h3> 유플렉스 스마트공장 API 서비스</h3>

django version: 3.1.2 <br>
python version: 3.8.3 <br><br>


<h3> - 실행 명령어 </h3>
python manage.py runserver


<h3> - 이미지 모듈 </h3>
Django의 ImageField를 사용하기 위해 Pillow 설치가 필요 <br>
- <b>pip install Pillow</b> 

<h3> - InfluxDB </h3>
현재 로컬에서 InfluxDB를 설치하여 사용

<h3> - Docker </h3>
Docker version: Client: Docker Engine - Community
 Version:           20.10.1
 API version:       1.41
 Go version:        go1.13.15
 Git commit:        831ebea
 Built:             Tue Dec 15 04:34:58 2020
 OS/Arch:           linux/amd64
 Context:           default
 Experimental:      true

Server: Docker Engine - Community
 Engine:
  Version:          20.10.1
  API version:      1.41 (minimum version 1.12)
  Go version:       go1.13.15
  Git commit:       f001486
  Built:            Tue Dec 15 04:32:52 2020
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.4.3
  GitCommit:        269548fa27e0089a8b8278fc4fc781d7f65a939b
 runc:
  Version:          1.0.0-rc92
  GitCommit:        ff819c7e9184c13b7c2607fe6c30ae19403a7aff
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
Docker 이미지 빌드를 위한 명령어: <b> docker-compose up --build </b>
