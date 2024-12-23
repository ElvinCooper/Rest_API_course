FROM python:3.11
EXPOSE 500
WORKDIR /app
COPY requirements.txt 
RUN pip install flask -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]