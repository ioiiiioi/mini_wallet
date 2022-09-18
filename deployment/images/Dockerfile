FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
COPY . /code
WORKDIR /code
RUN ls -l
RUN pip3 install -r requirements.txt --no-cache-dir
EXPOSE 8000