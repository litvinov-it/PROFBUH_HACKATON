from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import datetime

router = APIRouter(
    tags=["Pages"]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def get_base_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "date": datetime.datetime.now().strftime("%Y")
        }
    )
