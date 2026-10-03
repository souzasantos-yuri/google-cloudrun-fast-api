from sqlalchemy import create_engine, MetaData
from faker import Faker
from hashlib import sha256
import random
import uuid

metadata = MetaData()

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5433/fake_data"
)

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