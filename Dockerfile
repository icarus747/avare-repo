FROM python:3.7

WORKDIR /app
COPY app/* /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "-u", "./repo_download.py" ]
