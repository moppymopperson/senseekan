FROM golang AS build-env
ADD . /go/src/senseekan
WORKDIR /go/src/senseekan
RUN go get && go build -o senseekan
CMD ./senseekan
