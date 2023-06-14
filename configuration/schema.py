import sqlalchemy

from database import Base

malicious_words = sqlalchemy.Table(
    "malicious_words",
    Base.metadata,
    sqlalchemy.Column("word", sqlalchemy.String,
                      primary_key=True),
)
