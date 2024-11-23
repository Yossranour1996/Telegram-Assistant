# Use the official AWS Lambda Python 3.12 image for Lambda compatibility
FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.12

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code into the container
COPY src/*.py .

# Specify the Lambda function handler
CMD ["lambda_function.lambda_handler"]
