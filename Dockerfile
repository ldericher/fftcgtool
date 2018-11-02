FROM python:3.7-alpine

ENV LIBRARY_PATH=/lib:/usr/lib
ENV PYTHONUNBUFFERED 1

RUN \
    # install build prerequisites \
    apk add --no-cache \
      build-base \
      jpeg-dev \
      zlib-dev \
&&  pip3 install pillow requests \
	  # remove build prerequisites \
&&  apk del --no-cache \
		  build-base

WORKDIR "/app"

COPY . .

ENTRYPOINT ["./main.py"]
