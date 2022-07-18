FROM localhost:5000/devcontainer:latest
RUN mkdir /usr/src/app
COPY ./mkilmahtk /usr/src/app
WORKDIR /usr/src/app
RUN yes | cp ./_prod/settings.py /usr/src/app/config
RUN yes | cp ./_prod/celery.py /usr/src/app/config