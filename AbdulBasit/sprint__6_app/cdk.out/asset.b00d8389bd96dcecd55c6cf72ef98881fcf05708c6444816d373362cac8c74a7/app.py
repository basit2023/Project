
# import the Flask object from the flask package.
from flask import Flask
from flask import render_template
#from jinja2 import Markup
import random
import os


#pass the special variable __name__ that holds the name of the current Python module. 
app = Flask(__name__)

image=[
    "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/cute-cat-photos-1593441022.jpg?crop=0.669xw:1.00xh;0.166xw,0&resize=640:*",
    "https://cdn.pixabay.com/photo/2014/11/30/14/11/cat-551554__340.jpg",
    "https://www.rd.com/wp-content/uploads/2021/04/GettyImages-988013222-scaled-e1618857975729.jpg",
    "https://i.pinimg.com/originals/7e/0a/50/7e0a507de8cf8b46e0f2665f1058ef37.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXOEaZ785NGKjIVH4dA_Nh_Iqrx7mch4nYCIlNOwViIyDOceXkkaUXBE72ilIHnisKkGs&usqp=CAU",
    "https://cdn.britannica.com/22/206222-131-E921E1FB/Domestic-feline-tabby-cat.jpg"]

@app.route('/')
def index():
    #return 'Hello, World!'

             #here render_template() with index.html as an argument, this tells render_template() 
             #to look for a file called index.html in the templates folder.
    #return "hello this is me basit"
    return render_template('index.html')


@app.route('/pic')
def pic():
    #return 'Hello, World!'
    url=random.choice(image)
    return render_template('pic.html',   url=url
                          )
        
@app.route('/app')
def blog():
    return "Hello, from APP!"
    
    
    
if __name__=='__main__':
    #host=0.0.0.0-: This tells your operating system to listen on all public IPs.
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',8081)) #os.environ behaves like a python dictionary, so all the common dictionary operations like get and set can be performed.
    )
    
# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def index():
#   return "Hello world! this is me basit" 

# if __name__ == '__main__':
#     #app.debug = True
#     app.run()