FROM ubuntu:latest
LABEL maintainer="Christopher Foundas <foundacg@clarkson.edu"
RUN apt-get update
RUN apt-get install -y python3 python3-pip python3-dev build-essential
RUN apt-get install git -y && \
git clone https://github.com/thoughtdoer/mortgagecharts.git && \
pip3 install -r mortgagecharts/requirements.txt
ENTRYPOINT ["python3"]
CMD ["mortgagecharts/app.py"]
