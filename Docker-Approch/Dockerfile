FROM python:3.9-slim

# Install required dependencies
RUN pip install --default-timeout=1000 kubernetes


# Copy the script
COPY cleanup.py /scripts/cleanup.py

# Set the working directory
WORKDIR /scripts

# Command to run the script
CMD ["python", "-u","cleanup.py"]
