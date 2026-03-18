from testcontainers.postgres import PostgresContainer
import pytest
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.database import Base
from sqlalchemy.ext.asyncio import async_sessionmaker
from httpx import AsyncClient
from app.main import app
import os
from sqlalchemy import text



from app.core.database import get_db
@pytest.fixture(scope='function')
def postgres_container():
    with PostgresContainer(image='postgres:15') as pg:
        yield pg

@pytest.fixture(scope='function')
async def db_engine():
    # url = postgres_container.get_connection_url()
    # url = url.replace("postgresql+psycopg2","postgresql+asyncpg")
    # engine = create_async_engine(url)

    database_url = os.environ.get("DATABASE_URL")
    
    if database_url:
        engine = create_async_engine(database_url)
        print(f"ENGINE URL: {engine.url}")

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield engine
        await engine.dispose()
    else:
        with PostgresContainer(image="postgres:16") as pg:
            url = pg.get_connection_url().replace("postgresql+psycopg2","postgresql+asyncpg")
            engine = create_async_engine(url)
            print(f"ENGINE URL: {engine.url}")

            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            yield engine
            await engine.dispose()
   


@pytest.fixture(scope='function')
async def session_factory(db_engine):
    factory = async_sessionmaker(db_engine)
    
    async with factory() as sess:
        print("TRUNCATING")
        await sess.execute(text("TRUNCATE TABLE users, alerts RESTART IDENTITY CASCADE"))
        await sess.commit()
    yield factory
        


@pytest.fixture
async def client(session_factory):
  async def override_get_db():
      print("USING TEST DB")
      async with session_factory() as fresh_session:
          yield fresh_session

  app.dependency_overrides[get_db] = override_get_db

  async with AsyncClient(app=app, base_url="http://test") as c:
    
    yield c
  app.dependency_overrides.clear()
