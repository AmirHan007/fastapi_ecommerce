from decimal import Decimal
from sqlalchemy import String, Boolean, Float, Integer, Numeric, text
from sqlalchemy.orm import Mapped, mapped_column, relationship  
from sqlalchemy import ForeignKey  

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(200), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)  
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    rating: Mapped[float] = mapped_column(Float, default=0.0, server_default=text('0')) # средний рейтинг

    # Отношение 1
    category: Mapped["Category"] = relationship("Category", back_populates="products")  # type: ignore

    # Отношение 2
    seller: Mapped["User"] = relationship("User", back_populates="products")  # type: ignore

    # Отношение 5
    reviews: Mapped["Review"] = relationship("Review", back_populates="product") # type: ignore