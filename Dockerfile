FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive
ENV FLASK_ENV=production
ENV FLASK_APP=/usr/src/app/password_manager
ENV FLASK_ENCRYPTION_KEY=changethispleasenow

RUN apt update && apt-get install -y python3-pip
RUN mkdir -p /usr/src/app/password_manager
WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD password_manager /usr/src/app/password_manager
RUN flask initdb
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000","password_manager:app"]
