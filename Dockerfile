
FROM python:3.8

RUN export GO_ARCHIVE="go1.16.6.linux-amd64.tar.gz"
RUN curl -O "https://dl.google.com/go/$GO_ARCHIVE"
RUN sha256sum $GO_ARCHIVE
RUN tar xvf $GO_ARCHIVE
RUN chown -R root:root ./go
RUN mv go /usr/local
ENV PATH=$PATH:/usr/local/go/bin

RUN pip --no-cache-dir install pylint

RUN apt -y update && apt install -y build-essential
