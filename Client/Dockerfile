# Use a Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
# Expose the port your Flask application is listening on
EXPOSE 5000

# Run the Client service
# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0","--port=5000"]