FROM python:3.8 as builder

RUN pip install \
    folium \
    selenium \
    chromedriver-binary==84.0.4147.30.0 \
    Pillow \
    gpxpy \
    geopy

FROM python:3.8-slim as runner

WORKDIR /app/

RUN apt update \
    && apt install -y wget gnupg unzip \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && apt update \
    && apt install -y google-chrome-stable \
    && wget https://chromedriver.storage.googleapis.com/84.0.4147.30/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/

COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

COPY . ${WORKDIR}

RUN pip install .

ENTRYPOINT [ "/usr/local/bin/komamap" ]
