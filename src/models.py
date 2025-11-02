from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    # Relationchips parent
    favoritePlanets: Mapped[List["FavoritePlanet"]
                            ] = relationship(back_populates="user")
    favoriteCharacters: Mapped[List["FavoriteCharacter"]] = relationship(
        back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(120))

    # Relationchips parent
    favoritePlanets: Mapped[List["FavoritePlanet"]
                            ] = relationship(back_populates="planet")
    characters: Mapped[List["Character"]] = relationship(
        back_populates="planet")


class FavoritePlanet(db.Model):
    __tablename__ = "favoritePlanet"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # Relationships childrens
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="favoritePlanets")

    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    planet: Mapped["Planet"] = relationship(back_populates="favoritePlanets")


class Character(db.Model):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(120))

    # Relationchips parent
    favoriteCharacters: Mapped[List["FavoriteCharacter"]] = relationship(
        back_populates="character")

    # Relationships childrens
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    planet: Mapped["Planet"] = relationship(back_populates="characters")


class FavoriteCharacter(db.Model):
    __tablename__ = "favoriteCharacter"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # Relationships childrens
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="favoriteCharacters")

    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    character: Mapped["Character"] = relationship(
        back_populates="favoriteCharacters")