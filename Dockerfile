# Stage 1: Build the application environment
FROM python:3.12.9-alpine3.21

# setting up working directory
WORKDIR /app

# copying the requirement file
COPY requirements.txt requirements.txt

# updating the package index and upgrading libraries
RUN apk update && apk upgrade --no-cache libcrypto3 libssl3

# installing the packages
RUN pip install  --no-cache-dir -r requirements.txt

# copying the files to the working directory
COPY . .

# executing the code
CMD ["python", "main.py"]
