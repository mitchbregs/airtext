FROM public.ecr.aws/lambda/python:3.8

RUN yum install \
    gcc \
    python-devel \
    postgresql-devel -y

COPY handler.py .
COPY requirements.txt  .

ARG PIP_INDEX_URL

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD [ "handler.main" ]
