FROM debian

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive DEBIAN_PRIORITY=critical \
       apt-get install -y --no-install-recommends \
           python-pip python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install setuptools wheel
RUN pip3 install setuptools wheel

## setuptools must finish installation BEFORE numpy
RUN pip install numpy
RUN pip3 install numpy

COPY ./entrypoint.sh /var/www/

USER www-data:www-data

ENTRYPOINT ["/var/www/entrypoint.sh"]
