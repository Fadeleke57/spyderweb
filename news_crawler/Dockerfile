# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY news_crawler/requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Chrome and ChromeDriver
RUN apt-get update && apt-get install -y wget unzip \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get -fy install \
    && dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install \
    && wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.61/linux64/chromedriver-linux64.zip \
    && unzip /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ \
    && rm google-chrome-stable_current_amd64.deb /tmp/chromedriver.zip \
    && apt-get install -y \
        xvfb \
        libxi6 \
        libgconf-2-4 \
        libappindicator1 \
        libnss3 \
        libasound2

# Copy the rest of the application code into the container
COPY news_crawler /app/news_crawler

# Set the working directory to the root directory for running Scrapy
WORKDIR /app/news_crawler

# Expose port 6800 for Scrapy
EXPOSE 6800

# Run the Scrapy crawl command or keep it running by default
CMD ["tail", "-f", "/dev/null"]