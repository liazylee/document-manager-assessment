# function I need to do:

- [x] Stores files of any type and name
- [x] Stores files at any URL
- [x] Does not allow interaction by non-authenticated users
- [x] Does not allow a user to access files submitted by another user
- [x] Allows users to store multiple revisions of the same file at the same URL
- [x] Allows users to fetch any revision of any file
- [x] Demonstrate functionality that allows a client to retrieve any given version of document
  using an endpoint that implements a Content Addressable Storage mechanism.

# no_funtion but need to do:

- [x] unit testing
- [ ] clear document and code

# stretch goal:

- [x] Demonstrate basic read/write permissions enforcement on individual versions of documents.
- [ ] Create a UI for viewing differences in content between file versions.

## Getting Started

1. [Install Direnv](https://direnv.net/docs/installation.html)
2. [Install Pipenv](https://pipenv.pypa.io/en/latest/installation/)
3. This project requires Python 3.11 so you will need to ensure that this version of Python is installed on your OS
   before building the virtual environment.
4. `$ cp example.env .envrc`
5. `$ direnv allow .`
6. `$ pipenv install -r requirements/local.txt`. If Python 3.11 is not the default Python version on your system you may
   need to explicitly create the virtual environment (`$ python3.11 -m venv .venv`) prior to running the install
   command.
7. `$ pipenv run python manage.py makemigrations` to migrate the database.
8. `$ pipenv run python manage.py migrate` to create the database.
8. `$ pipenv run python manage.py load_file_fixtures` to create the fixture file versions.
9. `$ pipenv run python manage.py runserver 0.0.0.0:8001` to start the development server on port 8001.

### Type checks

Running type checks with mypy:

    $ mypy propylon_document_manager

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

## example

### response for the structure of file_version_list

```json
[
  OrderedDict(
  [
    (
    'id',
    1),
    (
    'child_file',
    [
      OrderedDict(
      [
        (
        'id',
        1),
        (
        'file_name',
        'Full Stack Engineer Test.pdf'
        ),
        (
        'version_number',
        1),
        (
        'url_file',
        '/media/upload/1/96735484/1/Full_Stack_Engineer_Test.pdf'
        ),
        (
        'extra_info',
        None),
        (
        'file_type',
        'application/pdf'
        ),
        (
        'file_size',
        88085),
        (
        'file_hash',
        '96735484'
        ),
        (
        'file_user',
        1)
      ]
      )
    ]
    ),
    (
    'file_name',
    'Full Stack Engineer Test.pdf'
    ),
    (
    'version_number',
    1),
    (
    'url_file',
    'http://testserver/media/upload/1/96735484/1/Full_Stack_Engineer_Test.pdf'
    ),
    (
    'extra_info',
    None),
    (
    'file_type',
    'application/pdf'
    ),
    (
    'file_size',
    88085),
    (
    'file_hash',
    '96735484'
    ),
    (
    'file_user',
    1)
  ]
  )
]
```

the json data is order by the file_name. user can use file_name as category to find the file_version_list.

### UI for viewing differences in content between file versions.

user can select two versions of file and open it in the browser to compare the difference.



