from pydantic import BaseModel, Field, ConfigDict, EmailStr
from decimal import Decimal
from datetime import datetime


class CategoryCreate(BaseModel):
    """
    Модель для создания и обновления категории.
    Используется в POST и PUT запросах.
    """
    name: str = Field(..., min_length=3, max_length=50,
                      description="Название категории (3-50 символов)")
    parent_id: int | None = Field(None, description="ID родительской категории, если есть")


class Category(BaseModel):
    """
    Модель для ответа с данными категории.
    Используется в GET-запросах.
    """
    id: int = Field(..., description="Уникальный идентификатор категории")
    name: str = Field(..., description="Название категории")
    parent_id: int | None = Field(None, description="ID родительской категории, если есть")
    is_active: bool = Field(..., description="Активность категории")

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    """
    Модель для создания и обновления товара.
    Используется в POST и PUT запросах.
    """
    name: str = Field(..., min_length=3, max_length=100,
                      description="Название товара (3-100 символов)")
    description: str | None = Field(None, max_length=500,
                                       description="Описание товара (до 500 символов)")
    price: Decimal = Field(..., gt=0, description="Цена товара (больше 0)", decimal_places=2)
    image_url: str | None = Field(None, max_length=200, description="URL изображения товара")
    stock: int = Field(..., ge=0, description="Количество товара на складе (0 или больше)")
    category_id: int = Field(..., description="ID категории, к которой относится товар")


class Product(BaseModel):
    """
    Модель для ответа с данными товара.
    Используется в GET-запросах.
    """
    id: int = Field(..., description="Уникальный идентификатор товара")
    name: str = Field(..., description="Название товара")
    description: str | None = Field(None, description="Описание товара")
    price: Decimal = Field(..., description="Цена товара в рублях", gt=0, decimal_places=2)
    image_url: str | None = Field(None, description="URL изображения товара")
    stock: int = Field(..., description="Количество товара на складе")
    category_id: int = Field(..., description="ID категории")
    is_active: bool = Field(..., description="Активность товара")
    rating: float = Field(default=0, description="Средний рейтинг товара на основе отзывов")

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """
    Модель для регистрации нового пользователя
    """
    email: EmailStr = Field(..., description="Email пользователя")
    password: str = Field(..., min_length=8, description="Пароль (минимум 8 символов)")
    role: str = Field(default="buyer", 
                      pattern="^(buyer|seller|admin)$", 
                      description="Роль: 'buyer', 'seller' или 'admin'")


class User(BaseModel):
    """
    Модель для ответа после создания нового пользователя
    """
    id: int = Field(..., description="Уникальный идентификатор пользователя")
    email: EmailStr = Field(..., description="Email пользователя")
    role: str = Field(..., description="Роль: 'buyer', 'seller' или 'admin'")
    is_active: bool = Field(..., description="Активен пользователь или удалён")

    model_config = ConfigDict(from_attributes=True)


class RefreshTokenRequest(BaseModel):
    """
    Модель для создания(получения) refresh-токена 
    """
    refresh_token: str


class ReviewCreate(BaseModel):
    """
    Модель для создания нового отзыва
    """
    product_id: int = Field(..., description="Уникальный идентификатор продукта (products.id)")
    comment: str | None = Field(description="Комментарий к товару")
    grade: int = Field(ge=1, le=5, description="Оценка товара от 1 до 5 включительно")


class Review(BaseModel):
    """
    Модель для ответа с данными отзыва
    """
    id: int = Field(..., description="Уникальный идентификатор отзыва")
    user_id: int = Field(..., description="Уникальный идентификатор пользователя (users.id)")
    product_id: int = Field(..., description="Уникальный идентификатор товара (products.id)")
    comment: str | None = Field(description="Текстовое поле для отзыва")
    comment_date: datetime = Field(description="Поле даты и времени")
    grade: int = Field(..., ge=1, le=5, description="Оценка товара от 1 до 5 включительно")
    is_active: bool = Field(default=True, description="Активен отзыв или удалён")

    model_config = ConfigDict(from_attributes=True)