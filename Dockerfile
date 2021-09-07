FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

RUN set -ex; \
    # install prerequisites
    apk add --no-cache \
        g++ \
        jpeg-dev \
        zlib-dev \
    ;

COPY . /usr/src/fftcgtool

RUN set -ex; \
    pip3 --use-feature=in-tree-build install /usr/src/fftcgtool

ENTRYPOINT ["fftcgtool"]
