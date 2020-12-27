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
Docker version: Client: Docker Engine - Community <br>
 Version:           20.10.1 <br>
 API version:       1.41 <br>
 Go version:        go1.13.15 <br>
 Git commit:        831ebea <br>
 Built:             Tue Dec 15 04:34:58 2020 <br>
 OS/Arch:           linux/amd64 <br>
 Context:           default <br>
 Experimental:      true <br> <br>

Server: Docker Engine - Community <br>
 Engine: <br>
  Version:          20.10.1 <br>
  API version:      1.41 (minimum version 1.12) <br>
  Go version:       go1.13.15 <br>
  Git commit:       f001486 <br>
  Built:            Tue Dec 15 04:32:52 2020 <br>
  OS/Arch:          linux/amd64 <br>
  Experimental:     false <br>
 containerd: <br>
  Version:          1.4.3 <br>
  GitCommit:        269548fa27e0089a8b8278fc4fc781d7f65a939b <br>
 runc: <br>
  Version:          1.0.0-rc92 <br>
  GitCommit:        ff819c7e9184c13b7c2607fe6c30ae19403a7aff <br>
 docker-init: <br>
  Version:          0.19.0 <br>
  GitCommit:        de40ad0 <br>
Docker 이미지 빌드를 위한 명령어: <b> docker-compose up --build </b>
