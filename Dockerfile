

FROM python:3.6.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt 
EXPOSE 8000 
ENTRYPOINT [ "python" ] 
CMD [ "main.py" ]