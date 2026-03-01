from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    admin_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
   
    # Отношение 1
    products: Mapped[list["Product"]] = relationship("Product", back_populates="category") # type: ignore

    # Отношение 3
    admin: Mapped["User"] = relationship("User", back_populates="categories") # type: ignore

    # Самоссылающаяся связь
    parent: Mapped["Category | None"] = relationship("Category",
                                                        back_populates="children",
                                                        remote_side="Category.id")
    children: Mapped[list["Category"]] = relationship("Category",
                                                      back_populates="parent")