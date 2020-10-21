# silvatools

Useful online tools made by silva

[Silvatools Demo](https://silvatools.herokuapp.com/)


### Tools

- API result (JSON) diff : Shows diff of results of GET requests from two URLs
- English Word Test Generator

### Tech Stack

- python 3.7.6
- django 3.0.7
- mysql: database

### Used pip packages

- [reportlab](https://www.reportlab.com/docs/reportlab-userguide.pdf) : PDF 생성/수정

### Installation

- Install [pyenv](https://github.com/pyenv/pyenv), [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv), docker
- [Pyenv Common Build Problems](https://github.com/pyenv/pyenv/wiki/common-build-problems) 
- [Deploying Django](https://docs.djangoproject.com/en/3.0/howto/deployment/)
- [Heroku - Deploy python](https://devcenter.heroku.com/articles/getting-started-with-python#deploy-the-app)
- [Heroku - Tracking git remote in heroku](https://devcenter.heroku.com/articles/git#tracking-your-app-in-git)

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

# apply db changes from specific app (optional)
python manage.py makemigrations {DJANGO_APP}

# create database
python manage.py migrate

# run server
gunicorn -w 4 silvatools.asgi:application
```

### Deploy to heroku

```bash
heroku apps
heroku git:remote -a silvatools
git push heroku master
```

### Useful Links

- Make batch script: [django-extension : runscript](https://django-extensions.readthedocs.io/en/latest/runscript.html)