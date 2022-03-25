FROM python:latest

WORKDIR /app

EXPOSE 8080
ENV FLASK_APP=todo_app.py

COPY . /app
RUN pip install -r requirements.txt

ENTRYPOINT [ "flask"]
CMD [ "run", "--host", "0.0.0.0", "-p", "8080"]
