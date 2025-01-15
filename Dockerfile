FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application source code to the container
COPY ./src /app/src
COPY ./requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Set the default command to run the application
CMD ["python", "src/app.py"]