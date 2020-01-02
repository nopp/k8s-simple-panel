FROM alpine

LABEL maintainer "Carlos Augusto Malucelli <malucellicarlos@gmail.com>"

ENV CLUSTER_NAME=clusterName
ENV AWS_DEFAULT_REGION=sa-east-1
ENV AWS_ACCESS_KEY_ID=accessKey
ENV AWS_SECRET_ACCESS_KEY=secretKey

RUN apk update \
    && apk add python3 git bash \
    && git clone https://github.com/nopp/eks-simple-panel.git \
    && cd eks-simple-panel \
    && pip3 install -r requirements.txt 

WORKDIR eks-simple-panel

COPY run.sh /eks-simple-panel

RUN chmod +x /eks-simple-panel/run.sh

EXPOSE 9191

ENTRYPOINT ["./run.sh"]
