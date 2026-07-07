# https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx
# https://testdriven.io/blog/docker-best-practices

ARG PYTHON_VERSION_ENV

###############
# First stage #
###############
FROM python:${PYTHON_VERSION_ENV} AS builder
ARG PYTHON_VERSION_ENV
COPY requirements.txt ./
RUN pip install --upgrade pip \
	&& pip install wheel \
	&& pip install -r requirements.txt


###############
# Final stage #
###############
FROM python:${PYTHON_VERSION_ENV}-slim
ARG PYTHON_VERSION_ENV

COPY --from=builder /usr/local/lib/python${PYTHON_VERSION_ENV}/site-packages \
	/usr/local/lib/python${PYTHON_VERSION_ENV}/site-packages
RUN apt-get update \
	# For mysqlclient to work:
	&& apt-get install --no-install-recommends -y libmariadb3 \
    && apt-get autoremove --purge -y \
    && mkdir -p /home/django/www

ARG APP_ROOT
ARG WWW_ROOT
WORKDIR ${WWW_ROOT}

# https://docs.python.org/3/using/cmdline.html#environment-variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --chmod=700 ./entrypoint.sh ${APP_ROOT}/

ENTRYPOINT ${APP_ROOT}/entrypoint.sh
