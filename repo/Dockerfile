FROM python:3.12-slim

WORKDIR /app

# Set the environment variable for timezone (default to UTC)
ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install aria2 and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends aria2

# Copy the script into the container
COPY  app/version_checker.py app/requirements.txt /app/

# # Install necessary Python packages
# RUN pip install requests beautifulsoup4
# Install the Python dependencies
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Create a directory for downloads
RUN mkdir -p /config/www/regions

# Run the script
CMD ["venv/bin/python", "-u", "version_checker.py"]
