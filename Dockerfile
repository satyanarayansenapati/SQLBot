# Stage 1: Build the application environment
FROM python:alpine3.21 

# setting up working directory
WORKDIR /app

# copying the requirement file
COPY requirements.txt requirements.txt

# installing the packages
RUN pip install --no-cache-dir -r requirements.txt

# copying the files to the working directory
COPY . .

# executing the code
CMD ["python", "main.py"]
