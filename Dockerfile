FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install virtualenv
RUN virtualenv env
RUN source env/Scripts/activate
RUN pip install -r requirements.txt
COPY . /code/
