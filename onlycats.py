from dataclasses import dataclass, field
import hashlib
import os

import databases
import sqlalchemy
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

DATABASE_URL = "sqlite:///./animals.db"

assert os.path.exists("/app/images/dogs/flag.jpg")


@dataclass
class Cat:
    filename: str
    is_public: str
    species: str
    _species: str = field(init=False, repr=False)

    @property
    def species(self) -> str:
        return self._species

    @species.setter
    def species(self, data: str) -> None:
        self._species = hashlib.md5(data.encode()).hexdigest()


DEFAULT_CATS = [
    Cat(filename="tabby.jpg", is_public="yes", species="tabby"),
    Cat(filename="munchkin.jpg", is_public="yes", species="munchkin"),
    Cat(filename="russian-blue.jpg", is_public="yes", species="russian-blue"),
    Cat(filename="sphynx.jpg", is_public="yes", species="sphynx"),
    Cat(filename="netcat.jpg", is_public="yes", species="netcat"),
]


database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

cats = sqlalchemy.Table(
    "cats",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("filename", sqlalchemy.String),
    sqlalchemy.Column("is_public", sqlalchemy.String),
    sqlalchemy.Column("species", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup():
    await database.connect()

    for cat in DEFAULT_CATS:
        create_cat = cats.insert().values(
            filename=cat.filename, is_public=cat.is_public, species=cat.species
        )
        await database.execute(create_cat)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/download/")
async def download(request: Request):
    form = {**(await request.form())}
    query = {"is_public": "yes"}

    if form.get("species") is None:
        return "Fail"

    form["species"] = hashlib.md5(form["species"].encode()).hexdigest()

    query.update(form)

    result = await database.fetch_one(
        query="SELECT filename FROM cats WHERE is_public='{is_public}' AND species='{species}'".format(
            **query
        )
    )

    if not result or ".." in result["filename"]:
        return "Fail"

    return FileResponse(os.path.join("/app", "images", "cats", result["filename"]))
