FROM python:3.8
ADD ./ /workspace
WORKDIR /workspace
RUN pip install -r requirements-dev.txt
RUN pip install -e /workspace