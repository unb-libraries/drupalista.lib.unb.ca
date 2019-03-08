FROM frolvlad/alpine-glibc
MAINTAINER Jacob Sanford <jsanford_at_unb.ca>

ENV KUBE_NODE NULL
ENV KUBE_NODE_PORT NULL
ENV KUBE_ADMIN_CA_KEY NULL
ENV KUBE_ADMIN_ADMIN_PEM NULL
ENV KUBE_ADMIN_ADMIN_KEY NULL
ENV SLACK_TOKEN NULL

WORKDIR /app
COPY app /app
ADD scripts /scripts

RUN apk --update add \
  curl \
  python \
  py-pip \
  openssh-client \
  openssl && \
  pip install rtmbot prettytable && \
  rm -f /var/cache/apk/* && \
  chmod -R 755 /scripts

ENTRYPOINT ["/scripts/run.sh"]
