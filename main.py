from fastapi import FastAPI
from alembic.config import Config
from alembic import command
import uvicorn


from app.handlers import router


def main():
    alembic_cfg = Config("alembic.ini")

    command.upgrade(alembic_cfg, "head")

    app = FastAPI()

    app.include_router(router)

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
