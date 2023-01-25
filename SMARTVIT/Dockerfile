FROM python:3.7

COPY . .
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

# ENTRYPOINT ["sleep"]
CMD ["python3", "main.py"]
