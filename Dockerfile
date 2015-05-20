FROM python:2.7

WORKDIR /sherparesponse
ENV HOME /root
RUN apt-get -y autoclean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY requirements.txt /sherparesponse/
RUN pip install --src /tmp -r /sherparesponse/requirements.txt

COPY . /sherparesponse/
