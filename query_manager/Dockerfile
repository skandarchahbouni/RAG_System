FROM python:3.10-slim
RUN apt-get update && apt-get install -y curl
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV INFORMATION_RETRIEVAL_API_HOST="http://information_retrieval:5000" \
    RESPONSE_GENERATOR_API_HOST="http://response_generator:5001" 
EXPOSE 5002
CMD ["python", "main.py"]