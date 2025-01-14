FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY app.py /app

# Install the required Python libraries (no Prometheus)
RUN pip install flask

# Expose the necessary port
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]
