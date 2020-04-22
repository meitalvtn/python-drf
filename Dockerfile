FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /policy_engine
WORKDIR /policy_engine
ADD . /policy_engine/
RUN pip install -r requirements.txt