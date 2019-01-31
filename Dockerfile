# start from an official image
FROM python:3.6

# arbitrary location choice:
RUN mkdir -p /opt/services/djangoapp/src
WORKDIR /opt/services/djangoapp/src

# install our two dependencies
RUN pip install gunicorn django django-rest psycopg2-binary

# copy our project code
COPY . /opt/services/djangoapp/src
RUN cd sportsfes2019 && python manage.py collectstatic --no-input

# expose the port 8000
EXPOSE 8000

CMD ["gunicorn", "--chdir", "sportsfes2019", "--bind", ":8000", "sportsfes2019.wsgi:application"]
