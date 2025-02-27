# 1. Create and activate the environment
``
uv venv --python 3.12
source .venv/bin/activate
``

# 2. Install all the dependencies
``
uv sync
``
# 3. Run the application
``
uv run fastapi dev
``

# deactivate the environment
``
deactivate

# Documentation

## MongoBernie ORM
https://beanie-odm.dev/tutorial/finding-documents/