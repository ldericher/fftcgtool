FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR "/app"

RUN set -ex; \
    pip3 install \
        --no-cache-dir --no-color --disable-pip-version-check --no-python-version-warning \
        pipenv \
    ;

COPY Pipfile Pipfile.lock ./

RUN set -ex; \
    # install prerequisites
    apk add --no-cache \
        g++ \
        jpeg-dev \
        zlib-dev \
    ; \
    # build/install local packages
    pipenv install --deploy; \
    pipenv --clear; \
    # remove build-only prerequisites
    apk del --no-cache \
        g++ \
    ;

COPY . .

ENTRYPOINT ["pipenv", "run", "./fftcgtool.py"]
