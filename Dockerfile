FROM python:3.12.0rc1
ADD ./ /workspace
WORKDIR /workspace
RUN pip install -r requirements-dev.txt
RUN pip install -e /workspace