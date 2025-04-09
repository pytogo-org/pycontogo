from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from datetime import datetime, timedelta
import os


app = FastAPI()


static_folder = os.path.join(os.path.dirname(__file__), "static")
templates_folder = os.path.join(os.path.dirname(__file__), "templates")
app.mount("/static", StaticFiles(directory=static_folder), name="static")
templates = Jinja2Templates(directory=templates_folder)

year = datetime.now().year

evnet_date = datetime(2025, 9, 23, 7, 30, 0)
event_date_str = evnet_date.strftime("%d %B %Y at %H:%M")


# @app.get("/favicon.ico", include_in_schema=False)
# async def favicon():
#     return StaticFiles(directory=static_folder).get_response(
#         path="favicon.ico", scope=None
#     )
# @app.get("/robots.txt", include_in_schema=False)
# async def robots_txt():
#     return StaticFiles(directory=static_folder).get_response(
#         path="robots.txt", scope=None
#     )
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "year": year,
            "event_date": event_date_str,
        },
    )


@app.get("/shop", response_class=HTMLResponse)
def shop_swag(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="shop.html",
        context={"year": year},
    )


@app.get("/register", response_class=HTMLResponse)
def register(request: Request):
    # check if the event is in exactly 1 month
    regigstration_date = datetime(2025, 8, 23, 7, 30, 0)
    te = evnet_date - regigstration_date
    print(te)
    if evnet_date - regigstration_date <= timedelta(days=30):
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "year": year,
                "event_date": event_date_str,
                "registration_open": True,
            },
        )
    return templates.TemplateResponse(
        request=request,
        name="coming-soon.html",
        context={
            "year": year,
            "event_date": event_date_str,
            "registration_open": False,
        },
    )

  


@app.get("/coming-soon", response_class=HTMLResponse)
def coming_soon(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="coming-soon.html",
        context={"year": year},
    )


@app.get("/volunteer", response_class=HTMLResponse)
def volunteer(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="volunteer.html",
        context={"year": year},
    )


@app.get("/proposal", response_class=HTMLResponse)
def proposal(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="speaker.html",
        context={"year": year},
    )


@app.get("/sponsor", response_class=HTMLResponse)
def sponsor(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="sponsor.html",
        context={"year": year},
    )


@app.get("/sponsors", response_class=HTMLResponse)
def sponsors(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="sponsors.html",
        context={"year": year},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            request=request, name="404.html", context={"year": year}, status_code=404
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
