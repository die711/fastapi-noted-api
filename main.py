from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker
from crud import CRUD
from db import engine
from schemas import NoteModel, NoteCreateModel
from http import HTTPStatus
from typing import List
from models import Note
import uuid

app = FastAPI(
    title='Noted API',
    description='This is a simple note taking service',
    docs_url='/'
)

session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

db = CRUD()


@app.get('/notes', response_model=List[NoteModel])
async def get_all_notes():
    notes = await db.get_all(session)
    return notes


@app.get('/notes/{id}', response_model=NoteModel)
async def update_note(id: str):
    note = await db.get_by_id(session, id)
    return NoteModel.model_validate(note)


@app.post('/notes', status_code=HTTPStatus.CREATED, response_model=NoteModel)
async def create_note(note: NoteCreateModel):
    new_note = Note(
        id=str(uuid.uuid4()),
        title=note.title,
        content=note.content
    )

    note = await db.add(session, new_note)
    return NoteModel.model_validate(note)


@app.put('/notes/{id}', response_model=NoteModel)
async def update_note(id: str, data: NoteCreateModel):
    updated_note = Note(
        title=data.title,
        content=data.content
    )

    note = await db.update(session, id, updated_note)
    return NoteModel.model_validate(note)


@app.delete('/notes/{id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_note(id: str):
    note = await db.get_by_id(session, id)
    await db.delete(session, note)
