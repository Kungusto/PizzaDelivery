from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from src.database import Base


class OrdersMealsORM(Base):
    __tablename__ = "orders_and_meals"

    id: Mapped[int] = mapped_column(primary_key=True)
    meal_id: Mapped[int] = mapped_column(ForeignKey("meals.meal_id"))
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id"))


class OrderORM(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str]

    meals: Mapped[list["MealsORM"]] = relationship( # type: ignore
        secondary="orders_and_meals",
        back_populates="orders"
    )