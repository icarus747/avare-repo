FROM python:3.12-slim

WORKDIR /app

# Set the environment variable for timezone (default to UTC)
ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install the Python venv dependencies
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip requests beautifulsoup4

# Copy the Python script into the /app directory
COPY ./app/check_weather.py /app/check_weather.py

# Run the script using the virtual environment's Python
CMD ["/app/venv/bin/python", "-u", "/app/check_weather.py"]
