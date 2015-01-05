# ECE Git Site

A university site for code and course management built on the Django framework

## Local Development

1. Create a virtual environment in this directory, typically done with
   `pyvenv venv`
2. Use the virtual environment created above, typically done with
   `source venv/bin/activate`
3. Install the requirements using `pip install -r requirements.txt`
4. Initialize the database with `python manage.py migrate`
5. Start the server with `python manage.py runserver`

## CAS

The CAS module based off [django-cas](https://bitbucket.org/cpcc/django-cas/).
This code is licensed under an MIT license. It is currently up-to-date with
`47d19f3a871fa744dabe884758f90fff6ba135d5`.

## License

Except where noted, all code is licensed under GPL v3.
