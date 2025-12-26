from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.favorite import Favorite

router = APIRouter(prefix="/api/favorites", tags=["favorites"])

class FavoriteCreate(BaseModel):
    city: str = Field(..., min_length=2, max_length=100)
    lat: float | None = None
    lon: float | None = None

@router.post("", status_code=201)
def add_favorite(payload: FavoriteCreate, db: Session = Depends(get_db)):
    # prevent duplicates by city (simple MVP)
    existing = db.query(Favorite).filter(Favorite.city.ilike(payload.city)).first()
    if existing:
        return existing

    fav = Favorite(city=payload.city, lat=payload.lat, lon=payload.lon)
    db.add(fav)
    db.commit()
    db.refresh(fav)
    return fav

@router.get("")
def list_favorites(db: Session = Depends(get_db)):
    return db.query(Favorite).order_by(Favorite.created_at.desc()).all()

@router.delete("/{favorite_id}")
def delete_favorite(favorite_id: int, db: Session = Depends(get_db)):
    fav = db.get(Favorite, favorite_id)
    if not fav:
        raise HTTPException(status_code=404, detail="Favorite not found")

    db.delete(fav)
    db.commit()
    return {"deleted": True, "id": favorite_id}
