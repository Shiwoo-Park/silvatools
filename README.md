# silvatools

Useful online tools made by silva

### Tools

- JSON diff : Shows diff of results of GET requests from two URLs

### Tech Stack

- python 3.7.6
- django 3.0.7

### Installation

- Install [pyenv](https://github.com/pyenv/pyenv), [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv), docker
- [Pyenv Common Build Problems](https://github.com/pyenv/pyenv/wiki/common-build-problems) 
- [Deploying Django](https://docs.djangoproject.com/en/3.0/howto/deployment/)

```shell script
# create mysql server container
docker-compose up -d

# setup python virtualenv
pyenv install 3.7.6
pyenv virtualenv 3.7.6 silvatools

# setup pip packages
cd $PROJ_HOME
pyenv local silvatools
pip install -r requirements.txt

# create database
python manage.py migrate

# run server
python -m pip install uvicorn
uvicorn silvatools.asgi:application
```

