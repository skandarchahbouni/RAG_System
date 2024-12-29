FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libmagic1 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader punkt_tab
COPY . .
CMD ["tail", "-f", "/dev/null"]