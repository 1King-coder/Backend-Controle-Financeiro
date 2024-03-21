FROM python:latest

WORKDIR /api

COPY . .

RUN rm -rf backendEnv

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--reload"]

EXPOSE 8000