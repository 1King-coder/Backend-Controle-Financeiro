# syntax=docker/dockerfile:1
FROM python:latest

# creates a file where all files will be 
WORKDIR /app 

# creates a enviroment variable named FASTAPI_APP that has the value of main.py
ENV FASTAPI_APP main.py 

#         local           docker
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# copy everything to workdir
COPY . .

# commands to start the api
CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000

