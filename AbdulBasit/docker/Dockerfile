# FROM nginx:1.15

# COPY index.html /usr/share/nginx/py
# CMD ["nginx","area.py"]

# FROM debian:8

# ENV host=www.google.com

# COPY ping.sh .

# CMD ["sh", "ping.sh"]



FROM python:3.6

# Install modules
#RUN pip install Flask

# Needed by the Flask module
#ENV FLASK_APP=server.py

# Copy source files into the image
COPY . .
EXPOSE 5000

CMD ["python", "./area.py"]