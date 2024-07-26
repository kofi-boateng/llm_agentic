from datetime import datetime
from typing import Optional

from sqlmodel import create_engine, Field, SQLModel

from llm_agentic.utils import ROOT_DIR


DATABASE_URL = f"sqlite+aiosqlite:///{ROOT_DIR}/llm_agentic.db"

async_engine = create_engine(
    DATABASE_URL, echo=True
)  # We're making the SQL transactions verbose so we can see what's going on


class Thread(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str
    content: str
    created_at: datetime = Field(default=datetime.now)
    updated_at: datetime = Field(default=datetime.now)


SQLModel.metadata.create_all(async_engine)
