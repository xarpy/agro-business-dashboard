# Agro Business Api Challenge
Creating a simple API for dashboard to challenge

[![Python Version][python-image]][python-url]
[![Django Version][django-image]][django-url]
[![Django Rest Framework Version][drf-image]][drf-url]

Small challenge project, creating a REST API with Django, aimed at agrobusiness.

## Installation

### Environment Local

Using your dependency manager, create a python environment, follow a [link](https://ahmed-nafies.medium.com/pip-pipenv-poetry-or-conda-7d2398adbac9) talking about the managers!

Access the project folder and using the **pip** manager, inside the python env, apply the command below:

```bash
pip install --upgrade pip && pip install --require-hashes -r requirements/dev.txt
```

After installing all dependencies, you must create a root user and apply the database migrations. The command to execute is:

```sh
./manage.py migrate && ./manage.py loaddata test_data.json
```

To compile the project, apply the command below:

```sh
./manage.py runserver
```

**Obs:**

* The database configured in the project is sqlite, to configure another just follow this [link](https://docs.djangoproject.com/en/3.2/ref/databases/)

* Remember that you must not reconfigure the settings.py module, so you must follow good practices and create a
    [local_settings](https://djangostars.com/blogconfiguring-django-settings-best-practices/) module to run locally or for development and testing!

* Based on the good security practices of the projects, we are using **pip-tools** as a tool to generate the hashes. If you want to know a little more about it, see the documentation and links in the tips!

* Depending on your OS version, you can run django by just calling the file like this ```./manage.py <command>``` or using the python compiler ```python manage.py <command>```.

### Docker Build

You will need to have docker compose, and finally apply the command:

```sh
docker compose up --build
```

If you need to execute another command for django and python, just follow structure below:

```sh
docker compose exec backend python manage.py <command you want>
```

**Obs:**

* The project preloads some basic data, such as a list of states and a default admin, for testing purposes. The admin login and password are `admin`, `12345`.
* For local tests, simply copy `env.example` to the `.env` file in the project's root folder and run the application if building, don't forget to remove the instruction from the `DEBUG` context.
* To run the unit tests, just follow the pytest instructions.
* If the swagger doesn't work to download the copy of the file, just access its `api/schema` route and it will download the file to be used in an APIClient of your choice.


## Usage

In order to be able to normalize, we add the best practices in this project, aiming to respect the principles with example **Clean Code**, **SOLID** and others. For more details, see the tip links!

### Formatters and Linters

* [Flake8](https://flake8.pycqa.org/en/latest/index.html)
* [Black](https://black.readthedocs.io/en/stable/)
* [Isort](https://isort.readthedocs.io/en/latest/)
* [Bandit](https://bandit.readthedocs.io/en/latest/)
* [MyPy](https://mypy.readthedocs.io/en/stable/)

**Obs:**

* Programming with Python, we use the `snake_case` style for variables, functions and methods, and the `PascalCase` style for classes. Configuration variables should written in `UPPERCASE`.


### Structure

We use the **MTV(Model-Template-Views)** architecture patterns, associated with **SOA(Service Oriented Architecture)** and **Clean Code principles**, to create API resources. To example, see the content:

```sh
#For testing the APIs, follow the pattern in this block
├── agrobusiness/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── core/
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── fixtures/
│   ├── adminuser.json
│   └── state.json
├── requirements/
│   ├── base.in*
│   ├── base.txt
│   ├── dev.in*
│   └── dev.txt
├── scripts/
│   └── nginx.conf
├── tests/
│   ├── agrobusiness/
│   │   ├── conftest.py
│   │   ├── __init__.py
│   │   ├── test_customer_endpoints.py
│   │   ├── test_farm_endpoints.py
│   │   ├── test_models.py
│   │   ├── test_planting_endpoints.py
│   │   ├── test_state_endpoints.py
│   │   └── test_token.py
│   └── __init__.py
├── docker-compose.yml*
├── Dockerfile*
├── env.example*
├── LICENSE
├── manage.py*
├── .pre-commit-config.yaml  #Settings file for pre-commits hook
├── .editorconfig            #Editorconfig settings file
├── pyproject.toml*          #Formatters and project configuration file
└── README.md
```

**Obs:**

* For normalization of routes, it is ideal to use routers and viewsets from DRF.
* To include a new lib (package), insert it in the appropriate file (base.in or dev.in) and finally update it with pip-tools.

## Tests

The django test platform is based on **pytest**, therefore following the basic principles for implementation and run, follow the relative documentation [link](https://docs.djangoproject.com/en/3.2/topics/testing/overview/). Based on this, we have a practical example of how to run the tests, taken from the documentation:

```sh
# Run all the tests in the animals.tests module
$ pytest tests

# Run all the tests found within the 'animals' package
$ pytest tests/<module-you-want-test>

# Run just one test case
$ pytest tests/<module-you-want-test>::<function-you-want-test>
```

**Obs:**

* To run the tests inside a docker container, you just need to apply the following command prefix ```docker compose exec backend  pytest  tests <same commands above>```

## Tips

In this session, we include several articles related to good practices, tools and more.

* [Tips for pip-tools and multple environments](https://www.caktusgroup.com/blog/2018/09/18/python-dependency-management-pip-tools/)
* [Locking dependency with pip-tools](https://lincolnloop.com/blog/python-dependency-locking-pip-tools/)
* [Tips for environments python](https://towardsdatascience.com/virtual-environments-104c62d48c54)
* [SOLID Principle](https://medium.com/@engnogueirawgn/princ%C3%ADpios-solid-na-pr%C3%A1tica-e932608406d6)
* [Clean Code and principles](https://henriquesd.medium.com/dry-kiss-yagni-principles-1ce09d9c601f)
* [Environments python, what is have choosen?](https://ahmed-nafies.medium.com/pip-pipenv-poetry-or-conda-7d2398adbac9)
* [Overview of python dependency management tools](https://modelpredict.com/python-dependency-management-tools)
* [Best pratices for development environment with Django](https://djangostars.com/blog/configuring-django-settings-best-practices/)
* [Types of development styles](https://betterprogramming.pub/string-case-styles-camel-pascal-snake-and-kebab-case-981407998841)
* [Best pratices with Django](https://steelkiwi.com/blog/best-practices-working-django-models-python/)
* [Django Translation messages](https://medium.com/@daxita2013/django-translation-b9ecdd723285)
* [Best pratices in Python](https://towardsdatascience.com/30-python-best-practices-tips-and-tricks-caefb9f8c5f5?gi=6989d5c08d78)
* [Flake 8 best configurations](https://simpleisbetterthancomplex.com/packages/2016/08/05/flake8.html)
* [Black tips](https://www.mattlayman.com/blog/2018/python-code-black/)
* [Multiple database configuration in settings](https://docs.djangoproject.com/en/3.2/topics/db/multi-db/)
* [Defining database in settings](https://docs.djangoproject.com/en/3.2/ref/databases/)
* [DRF Routers](https://www.django-rest-framework.org/api-guide/routers/)
* [DRF Viewsets](https://www.django-rest-framework.org/api-guide/viewsets/#viewsets)
* [Difference between Views, Generics Views and Viewsets](https://medium.com/analytics-vidhya/django-rest-framework-views-generic-views-viewsets-simplified-ff997ea3205f)
* [ReDocs and Swagger with DRF](https://www.django-rest-framework.org/topics/documenting-your-api/)
* [Tips with DRF](https://medium.com/profil-software-blog/10-things-you-need-to-know-to-effectively-use-django-rest-framework-7db7728910e0)
* [Best pratices with DRF](https://www.rootstrap.com/blog/django-best-practices-and-beginner-tips/)
* [TDD with Django](https://medium.com/the-andela-way/test-driven-development-with-django-ccb179171dcd)
* [How to use Django Debug Toolbar?](https://riptutorial.com/django/example/18002/using-django-debug-toolbar)
* [Pequeno tutorial sobre Django Debug Toolbar](https://www.youtube.com/watch?v=H-vLUoXKKIs)
* [Django and Architeture MTV Pattern](https://towardsdatascience.com/working-structure-of-django-mtv-architecture-a741c8c64082)
* [Tips for Scaling Django Apps](https://medium.com/@DoorDash/tips-for-building-high-quality-django-apps-at-scale-a5a25917b2b5)
* [EditorConfig tips](https://blog.matheuscastiglioni.com.br/padronizando-seus-editores-de-texto-com-editorconfig/)
* [Pre-commits tips](https://towardsdatascience.com/getting-started-with-python-pre-commit-hooks-28be2b2d09d5)
* [Pre-commits Automating](https://towardsdatascience.com/automating-python-workflows-with-pre-commit-hooks-e5ef8e8d50bb)
* [Why use Gitignore Global?](http://egorsmirnov.me/2015/05/04/global-gitignore-file.html)

## Resources and Documentations

* [Pip (Package Installer Python)](https://pip.pypa.io/en/stable/)
* [Pip Tools](https://github.com/jazzband/pip-tools)
* [Django](https://docs.djangoproject.com/en/3.2/)
* [Django Rest Framework](https://www.django-rest-framework.org/)
* [Django Cors Headers](https://github.com/adamchainz/django-cors-headers)
* [Django Extensions](https://django-extensions.readthedocs.io/en/latest/)
* [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/)
* [Linter Flake8](https://flake8.pycqa.org/en/latest/)
* [Formatter Black](https://black.readthedocs.io/en/stable/)
* [Daphne](https://github.com/django/daphne)
* [Gunicorn](https://gunicorn.org/)
* [Docker](https://docs.docker.com/get-started/)
* [Docker Compose](https://docs.docker.com/compose/)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

[python-image]: https://img.shields.io/badge/python-v3.11-blue
[django-image]: https://img.shields.io/badge/Django-v4.2.10-blue
[drf-image]: https://img.shields.io/badge/DRF-v3.14-orange
[drf-url]: https://www.django-rest-framework.org/community/release-notes/
[django-url]: https://docs.djangoproject.com/en/4.2/releases/4.2/
[python-url]: https://www.python.org/dev/peps/pep-0596/
