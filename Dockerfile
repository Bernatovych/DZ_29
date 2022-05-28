FROM python:slim

RUN useradd contact

WORKDIR /home/contact

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY book app
COPY migrations migrations
COPY contact.py config.py boot.sh app.db ./
RUN chmod a+x boot.sh

ENV FLASK_APP contact.py

RUN chown -R contact:contact ./
USER contact

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
