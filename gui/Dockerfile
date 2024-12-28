FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8000"]