FROM python:3.13.0a4
ADD ./ /workspace
WORKDIR /workspace
RUN pip install -r requirements-dev.txt
RUN pip install -e /workspace