FROM ubuntu

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY ./requirements.txt ./

EXPOSE 5000

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "script.py"]