from sqlalchemy import create_engine, MetaData, Table, Column, String, Date, Integer, Numeric, ForeignKey
from dotenv import load_dotenv
import pg8000
from google.cloud.sql.connector import Connector, IPTypes
import os

load_dotenv()

def get_conn() -> pg8000.dbapi.Connection:
    project_id = os.getenv("PROJECT_ID", "")
    region = os.getenv("REGION", "southamerica-east1")
    instance = os.getenv("INSTANCE" "athenaeum-database")
    instance_connection_name = f"{project_id}:{region}:{instance}"
    db_user = os.getenv("DB_USER", "")
    db_pass = os.getenv("DB_PASS", "")
    db_name = os.getenv("DB_NAME", "")

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC
    connector = Connector(ip_type)

    conn = connector.connect(
        instance_connection_name,
        "pg8000",
        user=db_user,
        password=db_pass,
        db=db_name
    )

    return conn

env = os.getenv("ENV", "local")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("SA_KEYFILE")

if env == 'local':
    engine = create_engine(
        "postgresql://postgres:postgres@localhost:5433/fake_data"
    )
elif env == 'prd':
    engine = create_engine("postgresql+pg8000://", creator=get_conn)
else:
    raise Exception(f"ENV {env} invalid!")

metadata = MetaData()

customers_table = Table(
    "customers",
    metadata,
    Column("cd_customer", String(256), primary_key=True),
    Column("nm_customer", String(135), nullable=False),
    Column("st_email", String(135), nullable=False),
    Column("st_phone", String(135), nullable=False),
    Column("st_state", String(2), nullable=False),
    Column("dt_birth", Date, nullable=False)
)

orders_table = Table(
    "orders",
    metadata,
    Column("cd_order", String(256), primary_key=True),
    Column("cd_customer", String(256), ForeignKey("customers.cd_customer"), nullable=False),
    Column("dt_order", Date, nullable=False),
    Column("nm_product", String(256), nullable=False),
    Column("qt_item", Integer, nullable=False),
    Column("vl_price", Numeric, nullable=False),
    Column("vl_shipping", Numeric, nullable=False),
    Column("vl_total", Numeric, nullable=False)
)

with engine.begin() as conn:
    metadata.create_all(conn)
    for table in metadata.tables.keys():
        print(f"{table} successfully created!") 