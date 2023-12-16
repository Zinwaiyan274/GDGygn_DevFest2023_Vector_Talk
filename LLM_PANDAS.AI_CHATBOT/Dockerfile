FROM python:bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-dev \
    && rm -rf /var/lib/apt/lists/*

 
# COPY requirements.txt .
# Install dependencies
COPY . . 
RUN pip3 install --upgrade pip
RUN pip3 install pandas pandasai bs4 langchain chromadb flask openpyxl SQLAlchemy flask_sqlalchemy cachetools

COPY . .

CMD ["python", "app.py"]