FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install git && \
git clone git@github.com:thoughtdoer/mortgagecharts.git && \
COPY . /mortgagecharts
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
