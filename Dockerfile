FROM python:3.11

WORKDIR /polygon

COPY requirements.txt ./
RUN pip install -r requirements.txt

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y vim z3 mariadb-server

COPY . .

ENV PYTHONPATH=/polygon

ENTRYPOINT nohup mysqld_safe --lower_case_table_names=1 --skip-grant-tables & /bin/bash
