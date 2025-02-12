FROM python:3.9-slim

WORKDIR /app
COPY app.py /app/
COPY templates/ /app/templates/
COPY static/ /app/static/

RUN pip install flask
ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
