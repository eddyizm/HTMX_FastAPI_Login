import sqlalchemy
from databases import Database
from sqlalchemy.sql.sqltypes import Boolean
DATABASE_URL = "sqlite:///./login_demo.db"

database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(
    DATABASE_URL, echo = True, connect_args={"check_same_thread": False}
)

users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True,
    autoincrement=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean, 
    server_default=sqlalchemy.sql.expression.false(), nullable=False)
    ) 

metadata.create_all(engine)