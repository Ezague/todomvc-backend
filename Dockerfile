from python:slim

RUN useradd todomvc

WORKDIR /home/todomvc

COPY requirements.txt requirements.txt
RUN python3 -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql cryptography

COPY app app
COPY migrations migrations
COPY todomvc.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP todomvc.py

RUN chown -R todomvc:todomvc ./
USER todomvc

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]