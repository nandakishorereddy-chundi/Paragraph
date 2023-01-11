FROM python:3.9.12
ADD . /Portcast
WORKDIR /Portcast
RUN pip3 install -r requirements.txt