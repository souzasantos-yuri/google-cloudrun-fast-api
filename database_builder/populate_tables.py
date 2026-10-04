from sqlalchemy import create_engine, MetaData
from faker import Faker
from hashlib import sha256
import random
import uuid
from dotenv import load_dotenv
import pg8000
from google.cloud.sql.connector import Connector, IPTypes
import os

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
fake = Faker("pt_BR")

customer_ids = []

def insert_customers(n_records):
    table = metadata.tables["customers"]
    with engine.begin() as conn:
        for _ in range(n_records):
            insert_command = table.insert().values(
                cd_customer=sha256(fake.cpf().encode("utf-8")).hexdigest(),
                nm_customer=fake.name(),
                st_email=fake.email(),
                st_phone=fake.phone_number(),
                st_state=fake.state_abbr(),
                dt_birth=fake.date_of_birth(minimum_age=18, maximum_age=80),
            ).returning(table.c.cd_customer)

            result = conn.execute(insert_command)
            customer_ids.append(result.scalar())

def insert_orders(n_records):
    table = metadata.tables["orders"]
    if not customer_ids:
        raise Exception("No customers found — insert customers first")

    with engine.begin() as conn:
        for _ in range(n_records):
            price = fake.pyfloat(left_digits=3, right_digits=2, positive=True)
            shipping = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
            qt_item = random.randint(1, 5)
            total = round((price * qt_item) + shipping, 2)

            insert_command = table.insert().values(
                cd_order=str(uuid.uuid4()),
                cd_customer=random.choice(customer_ids),
                dt_order=fake.date_this_year(),
                nm_product=fake.word(),
                qt_item=qt_item,
                vl_price=price,
                vl_shipping=shipping,
                vl_total=total,
            )
            conn.execute(insert_command)

if __name__ == "__main__":
    with engine.begin() as conn:
        metadata.reflect(conn)

    insert_customers(100)
    insert_orders(300)
    print("Tables successfully populated")