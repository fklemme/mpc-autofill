# Docker to provide interactive Chrome session over VNC
# Bits and pieces taken from https://github.com/siomiz/chrome
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND="noninteractive"

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install tools and dependencies for Google Chrome setup
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        fluxbox \
        gnupg2 \
        supervisor \
        x11vnc \
        xvfb \
    && rm -rf /var/lib/apt/lists/*

# Download and install Google Chrome
ADD https://dl.google.com/linux/linux_signing_key.pub \
    https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    /tmp/
RUN apt-key add /tmp/linux_signing_key.pub && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        /tmp/google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# Install supervisord config
COPY docker/autofill/supervisord.conf \
    /etc/supervisor/conf.d/supervisord.conf

# Now, we install all the autofill dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        python3-dev \
        python3-pip \
        wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt
COPY requirements.txt /MPCAutofill/
WORKDIR /MPCAutofill

# Install pip requirements
RUN pip3 install --no-cache-dir gunicorn wheel
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy entire repository
COPY . /MPCAutofill

# Create a non-root user and add permission to access the /MPCAutofill folder
RUN adduser -u 5678 --disabled-password --gecos "" mpcautofill && \
    chown -R mpcautofill /MPCAutofill
USER mpcautofill

# Prepare some fluxbox settings
WORKDIR /home/mpcautofill
RUN mkdir -p .fluxbox && \
    echo ' \n \
        session.screen0.toolbar.visible:  false \n \
        session.screen0.fullMaximization: true  \n \
        session.screen0.defaultDeco:      NONE  \n \
    ' >> .fluxbox/init

# Select Xvfb "display" for Google Chrome
ENV DISPLAY=":1"

# Prepare to start
EXPOSE 5900
EXPOSE 8000
USER root
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
