from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base, mapped_column

Column = mapped_column

metadata_obj = MetaData()

BaseModel = declarative_base(metadata=metadata_obj)
