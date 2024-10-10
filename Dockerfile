FROM python:3.12

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
  dos2unix \
  libpq-dev \
  libmariadb-dev-compat \
  libmariadb-dev \
  gcc \
  wget \
  && apt-get clean

RUN python -m pip install --upgrade pip


WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN apt-get install -y /app/scraper/selenium/bin/google-chrome-stable_current_amd64.deb