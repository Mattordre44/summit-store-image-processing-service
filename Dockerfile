FROM python:3.12.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application source code to the container
COPY ./src /app/src
COPY ./requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script into the container
COPY ./docker-entrypoint.sh /app/
RUN chmod +x docker-entrypoint.sh

# Set the default command to run the application
CMD ["./docker-entrypoint.sh"]