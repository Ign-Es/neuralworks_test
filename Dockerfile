FROM python:3.11-slim
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "scripts/get_api.py"]