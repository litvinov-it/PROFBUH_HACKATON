from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import articles, pages, tasks
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title = "My App",
    docs_url = "/documentation",
    redoc_url = None
)

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")

app.include_router(pages.router)
app.include_router(tasks.router)
app.include_router(articles.router)



