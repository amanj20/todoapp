FROM python:3.13-slim

WORKDIR /app

# Install Python deps first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Flask runs on 5000 in our app.py
EXPOSE 5000

# Good default for containers
ENV PYTHONUNBUFFERED=1

# Run with gunicorn (production style)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
