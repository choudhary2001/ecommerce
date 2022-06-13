# Ecommerce

The clean, fast and right way to start a new Django `1.10.1` powered website.

![Web capture_30-5-2022_121447_127 0 0 1](https://user-images.githubusercontent.com/54638339/173281785-29300da5-0a82-4fb1-8cf3-c88c2ad67268.jpeg)


## Getting Started

Setup project environment with [virtualenv](https://virtualenv.pypa.io) and [pip](https://pip.pypa.io).

```bash
$ virtualenv project-env
$ source project-env/bin/activate
$ pip install -r ecommerce/requirements.txt

# You may want to change the name `projectname`.
$ django-admin startproject --template ecommerce projectname

$ cd projectname/
$ cp settings_custom.py.edit settings_custom.py
$ python manage.py migrate
$ python manage.py runserver
```

## Features

* Basic Django scaffolding (commands, templatetags, statics, media files, etc).
* Split settings in two files. `settings_custom.py` for specific environment settings (localhost, production, etc). `projectname/settings.py` for core settings.
* Simple logging setup ready for production envs.

## Contributing

I love contributions, so please feel free to fix bugs, improve things, provide documentation. Just send a pull request.
