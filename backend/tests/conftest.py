from testcontainers.postgres import PostgresContainer
import pytest
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.database import Base
from sqlalchemy.ext.asyncio import async_sessionmaker
from httpx import AsyncClient
from app.main import app




from app.core.database import get_db
@pytest.fixture(scope='function')
def postgres_container():
    with PostgresContainer(image='postgres:15') as pg:
        yield pg

@pytest.fixture(scope='function')
async def db_engine(postgres_container):
    url = postgres_container.get_connection_url()
    url = url.replace("postgresql+psycopg2","postgresql+asyncpg")
    engine = create_async_engine(url)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine

    await engine.dispose()

@pytest.fixture(scope='function')
async def db_session(db_engine):
    factory = async_sessionmaker(db_engine)
    
    async with factory() as sess:
        yield sess


@pytest.fixture
async def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session

    async with AsyncClient(app=app,base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
