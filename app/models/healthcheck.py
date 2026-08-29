from sqlmodel import SQLModel


class HealthcheckSchema(SQLModel):
    status: str = "ok"
