from fastapi import FastAPI, Header, HTTPException
from http import HTTPStatus
from api_build.api_models import Message, CustomerRevenueOut
from sqlalchemy import func
from sqlalchemy.orm import Session
from api_build.database_client import DatabaseClient
from api_build.database_models import Customer, Order

app = FastAPI()
database_client = DatabaseClient()

@app.get("/health_check", status_code=HTTPStatus.OK, response_model=Message)
async def health_check():
    return {"message": "API Activated"}


@app.get("/customers", status_code=HTTPStatus.OK, response_model=CustomerRevenueOut)
async def get_customers(cd_customer: str = Header(..., alias='cd_customer')):
    with Session(database_client.engine) as session:
        result = (
            session.query(Customer)
            .filter_by(cd_customer=cd_customer)
            .first()
        )

    if result is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Cliente não encontrado",
        )

    return result

@app.get("/customers/revenue", status_code=HTTPStatus.OK, response_model=CustomerRevenueOut)

async def get_customer_revenue(
    cd_customer: str = Header(..., alias='cd_customer')
):

    with Session(database_client.engine) as session:
        customer = (
            session.query(Customer)
            .filter_by(cd_customer=cd_customer)
            .first()
        )

        if customer is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Cliente não encontrado",
            )

        revenue = (
            session.query(
                func.coalesce(func.sum(Order.qt_item * Order.vl_price), 0)
            )
            .filter(Order.cd_customer == cd_customer)
            .scalar()
        )

    return {
        "cd_customer": cd_customer,
        "vl_revenue": revenue,
    }