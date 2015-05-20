FROM python:2.7

WORKDIR /sherparesponse
ENV HOME /root
EXPOSE 8000

COPY . /sherparesponse/
RUN pip install --src /tmp -r /sherparesponse/requirements.txt
RUN apt-get -y autoclean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*