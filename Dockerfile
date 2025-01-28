# Stage 1: Build the application environment
FROM python:alpine3.21 

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Copy the application code and create the final image
#FROM python:alpine3.21

#WORKDIR /app

COPY . .

#COPY --from=builder /app/ /app

CMD ["python", "main.py"]