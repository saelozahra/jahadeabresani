From python:3.8
LABEL MAINTAINER = "SaeloZahra | https://saelozahra.ir"
ENV PYTHONUNBUFFERED 1
run mkdir /abresani
WORKDIR /abresani
COPY . /abresani
ADD requirements.txt / abresani
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --no-input
CMD ["gunicorn" , "--chdir" , "abresani" , "--bind" , ":8000" , "abresani.wsgi:application"]