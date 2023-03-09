FROM python:3.9


# set a directory for the app

WORKDIR /usr/src/app
#WORKDIR /usr/src/app

#copy all the files to the dependencies
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8081

#run the command
CMD ["python", "./app.py"]




# from thoom/pyresttest
# copy ./tests /usr/src/app
# WORKDIR /usr/src/app
# ENTRYPOINT ["pyresttest"]
# #The CMD command specifies the instruction that is to be executed when a Docker container starts.
# #CMD ["https://ifc2ccevg7.execute-api.us-west-1.amazonaws.com/","api_test_benchmark.yml"]