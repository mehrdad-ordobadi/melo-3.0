FROM python:3.11-slim

WORKDIR /melo

# Copy the application files to the container
COPY . /melo

RUN pip install -r requirements.txt

# Create the database tablesx
RUN cd app && mkdir instance && \
    python3 create_tables.py

EXPOSE 5001

# Run the application
ENTRYPOINT ["python3", "app/app.py"]
