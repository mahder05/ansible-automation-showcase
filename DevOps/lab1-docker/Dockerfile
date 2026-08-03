# 1. Use an official, lightweight Python runtime as a parent image
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file into the container
COPY requirements.txt .

# 4. Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code into the container
COPY app.py .

# 6. Expose the port the app runs on
EXPOSE 8080

# 7. Define the command to run the application
CMD ["python", "app.py"]
