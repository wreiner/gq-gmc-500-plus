FROM alpine:3.17

WORKDIR /gq-gmc500plus

COPY gq-gmc500plus.py /gq-gmc500plus
COPY gq-gmc500plus.json.example /gq-gmc500plus
COPY requirements.txt /gq-gmc500plus
COPY run.sh /gq-gmc500plus

RUN apk update \
    && apk add python3 py3-pip \
    && rm -rf /var/cache/apk/* \
    && pip install -r requirements.txt \
    && chmod +x run.sh

EXPOSE 8500

ENTRYPOINT ["./run.sh"]

