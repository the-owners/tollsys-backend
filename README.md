# Tolling System Backend
[![python-badge](https://img.shields.io/badge/Python-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![uv-badge](https://img.shields.io/badge/uv-6340ac?style=for-the-badge&logo=uv&logoColor=white)](https://astral.sh/blog/uv)
[![fastapi-badge](https://img.shields.io/badge/FastAPI-009486?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![postgresql-badge](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![render-badge](https://img.shields.io/badge/Render-000000?style=for-the-badge&logo=render&logoColor=white)](https://render.com/)

## Description

This branch is used for deployment.

Needs to have `requirements.txt` present at root as [Render doesn't support `uv` yet](https://community.render.com/t/how-to-deploy-python-app-with-astral-uv/33665) so remember to do `uv pip freeze > requirements.txt` before commiting until a better solution is found.
