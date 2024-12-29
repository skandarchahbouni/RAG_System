FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENV QUERY_MANAGER_API="http://query_manager:5002"
EXPOSE 3000
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=3000"]