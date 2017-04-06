# RESTful API Server

<font color=red size=5>To Be Perfected!!!</font>

This is an example of building RESTful API Server using [Flask](http://flask.pocoo.org/). The main structure of this web server refers to the example in book *Flask Web Development: Developing Web Applications with Python* written by **Miguel Grinberg**. For the details about building web server using Flask, please turn to Miguel Grinberg's book.

## Authentation
The authentation module in this example is not recommended in production and it will not match the requirement of different application well, but it is a good case to learn the way in which authentation is achieved in Flask.

## Web Pages
Sometimes, web pages are needed in a RESTful API Server. You can simplely add your routes in views under folder `main`, or you can create a new blueprint for your routes. The steps to create a blueprint, like `life`, are as follows:

1. Create a new folder under `app` and name it as 'life'. You can use other names too, but it 
make more sense to use the same name as blueprint;

2. New two files `__init__.py` and `views.py` under the folder created at previous step;

3. Add following lines into file `__init__.py`:
```
from flask import Blueprint
life = Blueprint('life', __name__)
import views    
```

4. import blueprint in file 'views.py', like `from . import life`;

5. Register your blueprint in the function `create_app`, like:
```
from life import life as life_bp
app.register_blueprint(life_bp)
```

6. Blueprint is ready, you can add your routes into file `views.py`.

## RESTful APIs
RESTful APIs are built up using [Flask-RESTful](https://github.com/flask-restful/flask-restful), which provides the building blocks for creating a great REST APIs with Flask. If you want to add new API, you take the existing one `Todo` as example:

1. New a file named `todo.py` under folder `resources`. Create a class `Todo` in this file, and implement `Get`, `Post`, `Put` and `Delete` methods or several of them according to your need;

2. import class Todo in file `__init__.py` under folder `resources`, and add string 'Todo' to varible `__all__`;

3. finally, add route into the file `routes.py` under folder `apis`, like `api.add_resource(Todo, '/todo/')`.

More detail about Flask-RESTful, please refer to it's [document](http://flask-restful.readthedocs.io/en/latest/).

## Celery
[Celery](http://www.celeryproject.org/) is a wonderful tool for management of task queue. Celery is set up in this example, and you can add your task into file `tasks.py` under folder `app`. If your need to use celery, you can find the tutorials [here](http://www.celeryproject.org/tutorials/).

Examples for celery tasks are given in `app/tasks.py`, one normal task and two periodic ones.

## Deployment
#### Virtual Environment
It is recommended to set up a virtual environment with [virtualenv](https://virtualenv.pypa.io/en/stable/) for this web server. It is better to set up virtual environment under the root path, and name it as `env`. A empty folder `env` is put under the root path to indicate the location of virtual environment.

#### uWSGI
It is not a good choice to using the buildin server of Flask in production. [uWSGI](http://uwsgi-docs.readthedocs.io/en/latest/) and [Nginx](http://nginx.org/) are choosen here to deploy this web server.

It is worth being metionded here that uWSGI dose not run on windows. uWSGI can be started in serveral ways, like command line:
```
uwsgi --socket 0.0.0.0:8000 --protocol=http -w myproject
```
or using a configurte file(recommanded), like ini, xml, yaml or json. ini file is adopted in this example which named `myproject.ini`. The description for each option are as follows:

```
[uwsgi]

module = myproject
socket = reporter.socket
master = true
callable = app
enable-threads = true
processes = 4
chmod-socket = 660
vacuum = true
die-on-term = true
smart-attach-daemon = path_to/smees.pid celery worker -A cworker.celery --pidfile=path_to/smees.pid;
```

The description for each option are as following:

| Options             |Description                                                                    |
|:-------------------:|:------------------------------------------------------------------------------|
| module              | specify the python file to start application, without file extension          |
| socket              | soket file which will be automaticly created for the communication with Nginx |
| master              | tell uWSGI to start up in master mode                                         |
| callable            | the Flask application name in `myproject.py`                                  |
| enable-threads      | enable multible threads function                                              |
| processes           | the number of processors to be used                                           |
| chmod-socket        | set the access right of the socket file                                       |
| vacuum              | clean up the socket when the process stops                                    |
| die-on-term         | aligns the Systemd which will be metioned later and uWSGI                     |
| smart-attach-daemon | start celery worker                                                           |

It is better to run uWSGI as a service in practise. Here an example for starting uWSGI using systemd is given. Create service unit file for systemd, like:
```
[Unit]
# specify metadata and dependencies
Description=uWSGI instance to serve reporter
# a description of this service
After=network.target
# start this after the networking target has been reached

[Service]
User=user account 
Group=user group
WorkingDirectory=.../myproject
Environment="PATH=.../myproject/env/bin"
ExecStart=.../myproject/env/bin/uwsgi --ini myproject.ini

[Install]
WantedBy=multi-user.target
# start this service when the regular multi-user system is up and running
```

You can name this service file as `myproject.service`, and the put this file under the path `/usr/lib/systemd/system/`, and start service using following command lines:
```
systemctl daemon-reload
systemctl enbale myproject.service
systemctl start myproject.service
```

More details please refer to this [tutorial](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04). If you prefer to allow init system start uWSGI automatically using Upstart script, please move to another [tutorial](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04).

#### NGINX
Create a server block for this web server, and it is better to create an independent configuration file and include this file in the main configuration file of Nginx `nginx.conf` than just adding this server block into the main configuration file. 
```
server {
    listen: 80
    service_name: [Server Domain]

    location / {
        include /etc/nginx/uwsgi_params;
        uwsgi_pass /home/Admin/project/myproject/myproject/myproject.socket; 
    }
}
```
After finishing configuration, you can use `nginx -t` to check the correctness of your configuration, and then restart nginx using `nginx restart`.

