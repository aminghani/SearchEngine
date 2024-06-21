FROM python:3.9-slim

WORKDIR /SearchEngine

COPY . /SearchEngine

RUN pip install -r SearchEngine/requirements.txt

EXPOSE 8000

CMD ["./run.sh"]

