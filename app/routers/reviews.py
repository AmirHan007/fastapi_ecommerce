from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db_depends import get_async_db

from app.models.reviews import Review as ReviewModel
from app.models.products import Product as ProductModel
from app.models.users import User as UserModel
from app.auth import get_current_buyer_or_admin, get_current_buyer
from app.schemas import Review as ReviewSchema, ReviewCreate


async def update_product_rating(db: AsyncSession, product_id: int):
    """
    Обновляет рейтинг о конкретном товаре
    """
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id,
            ReviewModel.is_active == True
        )
    )
    avg_rating = result.scalar() or 0.0
    product = await db.get(ProductModel, product_id)
    product.rating = avg_rating
    await db.commit()


router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/", response_model=list[ReviewSchema])
async def get_all_reviews(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список всех активных отзывов
    """
    result = await db.scalars(select(ReviewModel).where(ReviewModel.is_active == True))
    return result.all()


@router.post("/", response_model=ReviewSchema)
async def post_rev(review: ReviewCreate,
                   db: AsyncSession = Depends(get_async_db),
                   current_user: UserModel = Depends(get_current_buyer)):
    """
    Добавляет отзыв, привязанный только к покупателю ("buyer")
    """
    result = await db.scalars(select(ProductModel).where(ProductModel.id == review.product_id,
                                                         ProductModel.is_active == True))
    product = result.first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or inactive")
    
    result_to_check = await db.scalars(select(ReviewModel).where(ReviewModel.user_id == current_user.id,
                                                              ReviewModel.product_id == product.id))
    rev_to_check = result_to_check.first()
    # Если отзыв с точно такими же user_id и product_id уже существует, нельзя добавить ещё один аналогичный отзыв
    if rev_to_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Review already exists. You can't create two or more reviews for the same product")

    rev_to_add = ReviewModel(**review.model_dump(), user_id = current_user.id)
    db.add(rev_to_add)
    await db.commit()
    await update_product_rating(db, review.product_id)

    return rev_to_add


@router.delete("/{review_id}")
async def del_rev(review_id: int,
                  db: AsyncSession = Depends(get_async_db),
                  current_user: UserModel = Depends(get_current_buyer_or_admin)):
    """
    Удаляет отзыв по review_id, может только покупатель или админ.
    """
    result = await db.scalars(select(ReviewModel).where(ReviewModel.is_active == True,
                                                        ReviewModel.id == review_id))
    review = result.first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found or inactive")
    
    if review.user_id != current_user.id:
        if current_user.role != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own reviews")
    
    await db.execute(
        update(ReviewModel).where(ReviewModel.id == review_id).values(is_active = False)
    )
    await db.commit()
    await db.refresh(review)

    await update_product_rating(db, review.product_id)
    return {"message": "Review deleted"}