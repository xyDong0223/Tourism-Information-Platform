# Use a Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /serviceSkyscanner

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Create the database directory
RUN mkdir -p /app/data

# Copy the SQLite database file to the container
COPY Skyscanner.sqlite /app/data/Skyscanner.sqlite

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV SQLALCHEMY_DATABASE_URI=sqlite:////app/data/Skyscanner.sqlite

# Expose the port your Flask application is listening on
EXPOSE 5003

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0","--port=5003"]
