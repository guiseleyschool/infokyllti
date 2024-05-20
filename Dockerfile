FROM python:3.12-slim

WORKDIR /app

ENV PATH="/home/python/.local/bin:$PATH"

ARG UID=1000
ARG GID=1000

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl wget git libpq-dev gnupg \
  && wget -c https://github.com/nicolas-van/multirun/releases/download/1.1.3/multirun-x86_64-linux-gnu-1.1.3.tar.gz -O - | tar -xz \
  && mv multirun /bin \
  && wget https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb -O packages-microsoft-prod.deb \
  && dpkg -i packages-microsoft-prod.deb \
  && rm packages-microsoft-prod.deb \
  && apt-get update \
  && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev libgssapi-krb5-2 \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && groupadd -g "${GID}" python \
  && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python \
  && mkdir -p /app/static /app/media \
  && chown python:python -R /app

USER python

COPY --chown=python:python Pipfile Pipfile.lock ./

RUN pip install pipenv && pipenv install

ARG DEBUG="false"
ENV DEBUG="${DEBUG}" \
    PYTHONUNBUFFERED="true" \
    PYTHONPATH="." \
    PATH="${PATH}:/home/python/.local/bin" \
    USER="python"

COPY --chown=python:python . .

WORKDIR /app

VOLUME /app/data

RUN chmod +x docker-entrypoint.sh

RUN SECRET_KEY=dummyvalue pipenv run python3 manage.py collectstatic --no-input

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]