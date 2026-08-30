from sqlmodel import SQLModel


class HealthcheckView(SQLModel):
    status: str = "ok"
