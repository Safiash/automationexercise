FROM python:3.12.11-slim-bookworm

RUN apt-get update && apt-get install -y \
    curl \
    chromium \
    chromium-driver \
    xauth \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 \
    libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 \
    libasound2 libatspi2.0-0 libwayland-client0 libwayland-egl1 \
    libwayland-server0 fonts-unifont fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# asennetaan python-kirjastot
COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

# tänne Jenkins mounttaa workspacen, ei tarvitse kopioida testejä
WORKDIR /home/automationexercise

# jätetään CMD neutraaliksi, pipeline päättää mitä ajetaan
CMD ["bash"]