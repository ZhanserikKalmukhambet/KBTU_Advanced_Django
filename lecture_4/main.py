from sqlalchemy import select, insert
from fastapi import FastAPI
from pydantic import BaseModel

import database as db

app = FastAPI()


class BaseCitizen(BaseModel):
    name: str
    age: int

    class Config:
        from_attributes = True


class Citizen(BaseCitizen):
    id: int


class CreateCitizen(BaseCitizen):
    pass


@app.get("/citizens")
def get_citizens(name: str = None):
    if name is None:
        db_citizens = db.session.execute(
            select(db.Citizen)
        ).scalars().all()
    else:
        db_citizens = db.session.execute(
            select(db.Citizen).where(db.Citizen.name == name)
        ).scalars().all()

    citizens = []
    for db_citizen in db_citizens:
        citizens.append(Citizen.model_validate(db_citizen))
    return citizens


@app.post("/citizens")
def add_citizens(citizen: CreateCitizen) -> str:
    db.session.add(db.Citizen(**citizen.model_dump()))
    db.session.commit()
    db.session.close()
    return "Citizen was added"
