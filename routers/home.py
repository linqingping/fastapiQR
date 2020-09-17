from fastapi import APIRouter
from fastapi.responses import RedirectResponse


router = APIRouter()

@router.get("/")
async def read_typer():
    return RedirectResponse("/docs")