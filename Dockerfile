FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy your project files into the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Install curl (if not already available)
RUN apt-get update && apt-get install -y curl

# Copy the startup script into the container
COPY start.sh /app/start.sh

# Ensure the startup script is executable
RUN chmod +x /app/start.sh

# Expose the port
EXPOSE 8000

# Use the startup script as the container's entrypoint
ENTRYPOINT ["/app/start.sh"]
