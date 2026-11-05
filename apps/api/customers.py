from datetime import date

from pydantic import BaseModel


class Payment(BaseModel):
    id: str
    membership_period_start: date
    charged_on: date
    amount_cents: int
    currency: str


class Customer(BaseModel):
    id: str
    name: str
    business: str
    payments: list[Payment]


demo_customer = Customer(
    id="demo-001",
    name="Thinidu",
    business="Tunnel Express Car Wash",
    payments=[
        Payment(
            id="payment-001",
            membership_period_start=date(2026, 11, 1),
            charged_on=date(2026, 11, 1),
            amount_cents=4900,
            currency="AUD",
        ),
        Payment(
            id="payment-002",
            membership_period_start=date(2026, 11, 1),
            charged_on=date(2026, 11, 2),
            amount_cents=4900,
            currency="AUD",
        ),
    ],
)
