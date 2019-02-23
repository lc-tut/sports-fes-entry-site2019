FROM python:3.6

RUN mkdir -p /opt/services/djangoapp/src
WORKDIR /opt/services/djangoapp/src

COPY . /opt/services/djangoapp/src

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


EXPOSE 8000

CMD ["gunicorn", "--chdir", "sportsfes2019", "--bind", ":8000", "sportsfes2019.wsgi:application"]
