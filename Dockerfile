# FROM ubuntu:22.04
FROM python:3.10.5-bullseye
# Might be necessary.
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
# Install dependencies to allow open-webdriver
RUN apt-get update && apt-get install -y --force-yes --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    sudo gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 \
    libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 \
    libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 fonts-liberation \
    libnss3 lsb-release xdg-utils wget libgbm-dev
ENV DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket
ENV DISPLAY=:99

WORKDIR /app
RUN pip install --upgrade pip
# for sending files to other devices
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY --chown=root:root . .
RUN python -m pip install -e .
# Expose the port and then launch the app.

CMD ["/bin/bash", "unicorn.sh"]
