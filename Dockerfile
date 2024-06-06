FROM python:3.11

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY src/index.py /app/

EXPOSE 8080

CMD [ "python", "index.py" ]