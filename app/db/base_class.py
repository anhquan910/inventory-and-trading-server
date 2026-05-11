from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

# Base declarative model class that automatically generates table names.
@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        # Derive the database table name from the model class name.
        return cls.__name__.lower()