FROM ubuntu:22.04

USER root

RUN apt update -y && apt install -y \
    python3 \
    python3-pip \
    nodejs \
    yarn

RUN mkdir /opt/swap

COPY swap /opt/swap/swap
COPY alembic.ini /opt/swap/alembic.ini
COPY alembic /opt/swap/alembic
COPY setup.sh /opt/swap/setup.sh
COPY start-container.sh /opt/swap/start-container.sh
COPY requirements.txt /opt/swap/requirements.txt
COPY fe /opt/swap/fe

ENV CLIENT_DIR=/opt/swap/fe/build
ENV PYTHONPATH=/opt/swap/
ENV ALEMBIC_INI_PATH=/opt/swap/alembic.ini
ENV ALEMBIC_SCRIPTS=/opt/swap/alembic

RUN python3 -m pip install -r /opt/swap/requirements.txt

EXPOSE 8080

CMD ["bash", "/opt/swap/start-container.sh"]