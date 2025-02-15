FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy your project files into the container
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  python3 \
  python3-pip \
  python3-dev \
  git \
  curl \
  sqlite3 \
  libsqlite3-dev \
  ffmpeg \
  imagemagick \
  build-essential \
  libpq-dev && \
  rm -rf /var/lib/apt/lists/*

# Install Node.js and Prettier
RUN apt-get update && apt-get install -y nodejs npm && \
  node -v && \
  npm -v && \
  npm install -g prettier@3.4.2


# Install uv (Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
  export PATH="$HOME/.local/bin:$PATH" && \
  uv --version

# Install dependencies
RUN pip install -r requirements.txt

# Copy the startup script into the container
COPY start.sh /app/start.sh

# Ensure the startup script is executable
RUN chmod +x /app/start.sh

# Expose the port
EXPOSE 8000

# Use the startup script as the container's entrypoint
ENTRYPOINT ["/app/start.sh"]
