# Migration Guide: SQLAlchemy to SQLModel

This document explains the changes made when migrating from SQLAlchemy to SQLModel.

## What Changed

### Before (SQLAlchemy + Pydantic)
Previously, you needed two separate definitions:
- **ORM Model** (SQLAlchemy): Database table definition
- **Pydantic Schema**: API request/response validation

Example:
```python
# models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

# schemas/user.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

class UserRead(BaseModel):
    id: int
    name: str
    email: str
```

### After (SQLModel)
Now, you have a **single definition** that serves both purposes:

```python
# models/user.py
from sqlmodel import Field, SQLModel

# Table definition
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str

# Request schema
class UserCreate(SQLModel):
    name: str
    email: str

# Response schema  
class UserRead(SQLModel):
    id: int
    name: str
    email: str
```

## Key Benefits

1. **Less Code**: ~40% reduction in model definitions
2. **Single Source of Truth**: No need to maintain two separate definitions
3. **Type Safety**: Full Python type hints with validation
4. **Better DX**: Editor autocompletion and type checking work better
5. **Still SQLAlchemy**: SQLModel is built on top of SQLAlchemy (same engine, same queries)

## What Stays the Same

- **Database Operations**: Same SQLAlchemy async session and queries
- **FastAPI Integration**: Same dependency injection pattern
- **Migrations**: Can still use Alembic if needed
- **Engine Configuration**: Same async engine setup

## Breaking Changes

### Import Changes
```python
# Old
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select

# New
from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
```

### Model Definition Changes
```python
# Old
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

# New  
class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
```

### JSON Columns
```python
# Old
from sqlalchemy import JSON
config: Mapped[dict] = mapped_column(JSON)

# New
from sqlalchemy import Column
from sqlalchemy.types import JSON
config: dict = Field(default_factory=dict, sa_column=Column(JSON))
```

## Migration Steps

If you had existing SQLAlchemy models:

1. **Install SQLModel**:
   ```bash
   uv add sqlmodel
   ```

2. **Update imports** in model files

3. **Convert model definitions** to SQLModel syntax

4. **Update schema definitions** (or remove if using table models)

5. **Test queries** - they should work the same way

6. **Run tests** to ensure everything works

## SQLModel Resources

- **Docs**: https://sqlmodel.tiangolo.com/
- **Tutorial**: https://sqlmodel.tiangolo.com/tutorial/
- **GitHub**: https://github.com/tiangolo/sqlmodel

## Questions?

SQLModel is maintained by the creator of FastAPI, so it integrates perfectly with the framework and follows the same design principles.
