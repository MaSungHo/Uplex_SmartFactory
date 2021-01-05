FROM python:3.8.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y
ADD . /code/
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "uplex.wsgi:application"]
