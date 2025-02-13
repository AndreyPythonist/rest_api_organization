from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


from app.settings import DATABASE_URL


engine = create_async_engine(DATABASE_URL, future=True, echo=True)


async_session = async_sessionmaker(engine, expire_on_commit=False)
