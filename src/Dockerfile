FROM python:latest
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD *.py /server/
WORKDIR /server
EXPOSE 5000
CMD ["python3", "server.py"]
