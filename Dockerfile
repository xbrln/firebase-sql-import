FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN export GOOGLE_APPLICATION_CREDENTIALS=/firebase/credentials.json
RUN export FIREBASE_WEB_API_KEY=AIzaSyA64cOabUk8vkmwJkOym-vpOWstgjzAZPw
