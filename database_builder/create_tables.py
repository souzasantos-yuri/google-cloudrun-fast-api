from sqlalchemy import create_engine, MetaData, Table, Column, String, Date, Integer, Numeric, ForeignKey

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5433/fake_data"
)

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