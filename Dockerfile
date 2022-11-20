
FROM python:3.8

RUN export GOVERSION="1.16.6"
RUN curl -O "https://dl.google.com/go/go$GOVERSION.linux-amd64.tar.gz"
RUN sha256sum "go$GOVERSION.linux-amd64.tar.gz"
RUN tar xvf "go$GOVERSION.linux-amd64.tar.gz"
RUN chown -R root:root ./go
RUN mv go /usr/local
ENV PATH=$PATH:/usr/local/go/bin

RUN pip --no-cache-dir install pylint

RUN apt -y update && apt install -y build-essential
