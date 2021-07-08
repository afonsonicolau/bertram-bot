FROM python:3.8-slim

COPY . /bertram-project
WORKDIR /bertram-project

# RUN apk add py3-pip autoconf automake g++ make gcc --no-cache
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
