# Tolling System Backend
[![python-badge](https://img.shields.io/badge/Python-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![uv-badge](https://img.shields.io/badge/uv-6340ac?style=for-the-badge&logo=uv&logoColor=white)](https://astral.sh/blog/uv)
[![fastapi-badge](https://img.shields.io/badge/FastAPI-009486?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![postgresql-badge](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

<details>
<summary><h2 style="display:inline">Table of Contents</h2></summary>

   * [Description](#description-)
   * [How to use it](#how-to-use-it-)
   * [API documentation](#api-documentation-)
   * [Useful tips for developers](#useful-tips-for-developers-)
   * [Contributing](#contributing-)
   * [Acknowledgments](#acknowledgments-)
    
</details>

## Description [↑](#tolling-system-backend)

This is a simple backend for a tolling system made with FastAPI and PostgreSQL,
we tried to make it as simple as possible to use with special thought on common
use cases.

## How to use it [↑](#tolling-system-backend)

This project uses [uv](https://github.com/astral-sh/uv) so running it is as
simple as doing `uv run fastapi dev` inside the project folder. You may see
we're using `.devcontainer` technology, we're still working on it so this got
delayed for the time being, the rationale was to have an easy way to
automatically download and set up all the project dependencies in a neat
self-contained way for development.

## API documentation [↑](#tolling-system-backend)

As this project uses FastAPI, after starting the server, you can access
to `http://127.0.0.1:8000/docs` to see a Swagger UI documentation or go to
`http://127.0.0.1:8000/alt` to see a ReDoc variant of it.

Alternatively, if you can't (or don't want to) spin up the whole project on your
machine, we have set up a GitHub Actions workflow where the latest docs for the
bleeding edge version of the project will be hosted at
[theowners.github.io/tollsys-backend](theowners.github.io/tollsys-backend). Cool
isn't?

## Useful tips for developers [↑](#tolling-system-backend)

We recommend spinning up a DevContainer through Visual Studio Code! It is
awesome and it will handle everything you need to set up the development
environment automatically. Actually, this was developed using the
"Python 3 & PostgreSQL" one. We are actively looking to add SQLite support so
the front-end teams won't have to spin up a PostgreSQL installation just to test
their UIs.

On a side-note, you might notice autocomplete might not work properly, this can
be fixed by changing the *Selected Python Interpreter* (bottom-right corner when
working on a .py file) to the one contained in the virtual env
(`.venv/bin/python3.11` in this case).

## Contributing [↑](#tolling-system-backend)

The codebase is ruled under the PEP-8 style specifications, so if you want to
contribute make sure your code is compliant with it before submitting any pull
requests! Besides that, the whole thing is meant to be programmed in English,
ranging from code itself to comments, documentation, and related affairs.
We won't be that pedantic with this tho, use a linter.

Also, consider using
[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/),
seriously!

Oh, and pushing to main is blocked. Please stick to creating branchs and doing
pull-requests.

> [!CAUTION]
> main should ALWAYS WORK NO MATTER WHAT.

## Acknowledgements [↑](#tolling-system-backend)

To these awesome projects that made this even possible:
* [FastAPI](https://github.com/fastapi/fastapi)
* [astral-sh/uv](https://github.com/astral-sh/uv)
* [column-st/fastapi-openapi-specs-action](https://github.com/marketplace/actions/fastapi-openapi-specs-generator)
* [msayson/openapi-github-pages-action](https://github.com/marketplace/actions/openapi-github-pages-documentation)