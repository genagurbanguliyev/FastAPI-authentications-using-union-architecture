### Voice AI project

***

#### Recommended:

- python (version 3.12)
- Poetry (version 1.7.1)

***

#### INSTALLATIONS

use poetry for package management:
install needed dependencies from `project.toml` using

```shell
# activate venv that automatically created and used poetry
poetry shell

# install dependencies
poetry add
```

At the root directory create `.env` and past this:

```env
# Development
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=dev_app


# Production
# DB_HOST=localhost
# DB_PORT=5432
# DB_USER=postgres
# DB_PASS=postgres
# DB_NAME=prod_app


SECRET_KEY = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"
```

***
MIGRATIONS
use alembic for db migrations:
in terminal run:

```shell
alembic init
```

after that creates file `alembic.ini` and directory:  `alembic`
inside `alembic` folder has `env.py` and copy/past this:

```python
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from app.config import settings

from app.db.models import *  # noqa
from app.db.database import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

then run this:
this generates a migration, see `alembic/versions/` directiory,
inside that creates migration named like: `datetime()_initial_db.py`

> NOTE:
> inside that has `upgrade` and `downgrade` functions. that functions
> must not be `empty` or `pass`.

```shell
alembic revision --autogenerate -m "initial db"
alembic upgrade head
```

***

###### Project server can run with:

- hypercorn with trio
- hypercorn with asyncio
- uvicorn

Recommended hypercorn with trio
run project:

```shell
python runserver.py
```
