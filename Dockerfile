FROM python:3.11

WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY src/ /app/src/

EXPOSE 8000

CMD [ "uvicorn", "src.index:app" ]