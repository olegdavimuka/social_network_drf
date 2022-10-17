# Dependencies build
FROM python:3.10 as build-python
LABEL maintainer="Oleh Davymuka <olegdavimuka0@gmail.com>"

# Expose port 8000
EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Cleanup apt cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
RUN apt-get install wget -y

# Install pip requirements
RUN pip install --upgrade pip
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Final build
FROM python:3.10-slim

# Remove apt chache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy installed dependencies
COPY --from=build-python /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=build-python /usr/local/bin/ /usr/local/bin/

# Copy project files
WORKDIR /social_network
COPY . /social_network
