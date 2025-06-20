from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from src.database import Base


class MealsORM(Base):
    __tablename__ = "meals"

    meal_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(35))
    description: Mapped[str | None]

    orders: Mapped[list["OrderORM"]] = relationship( # type: ignore
        back_populates="meals", secondary="orders_and_meals"
    )