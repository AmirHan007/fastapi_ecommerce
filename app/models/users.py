from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String, default="buyer")

    # Отношение 2
    products: Mapped[list["Product"]] = relationship("Product", back_populates="seller") # type: ignore

    # Отношение 3
    categories: Mapped[list["Category"]] = relationship("Category", back_populates="admin") # type: ignore

    # Отношение 4
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="user") # type: ignore