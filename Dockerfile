FROM django
ADD . /policy_engine
WORKDIR /policy_engine
RUN pip install -r requirements.txt
CMD [ "python", "./manage.py runserver 0.0.0.0:8000" ]