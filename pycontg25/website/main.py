from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from starlette.exceptions import HTTPException as StarletteHTTPException
from config import supabase
from models import (
    Proposal,
    SponsorInquiry,
    VolunteerInquiry,
    WaitlistInquiry,
    RegistrationInquiry,
)
from datas import (
    get_something_by_field,
    get_sponsorteirs,
    get_sponsortirtbytitle,
    get_something_email,
    insert_something,
)
from datetime import datetime, timedelta
import os
import json


app = FastAPI()


static_folder = os.path.join(os.path.dirname(__file__), "static")
templates_folder = os.path.join(os.path.dirname(__file__), "templates")
app.mount("/static", StaticFiles(directory=static_folder), name="static")
templates = Jinja2Templates(directory=templates_folder)
sponsor_tiers = get_sponsorteirs()

year = datetime.now().year

event_date = datetime(2025, 9, 23, 7, 30, 0)
event_date_str = event_date.strftime("%d %B %Y at %H:%M")
regigstration_date = datetime(2025, 8, 1, 0, 0, 0)
opening_in = regigstration_date - datetime.now()
opening_in_days = opening_in.days


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return StaticFiles(directory=static_folder).get_response(
        path="favicon.ico", scope=None
    )
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
            "sponsor_tiers": sponsor_tiers,
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
    print(f"Opening in {opening_in_days} days")
    if opening_in > timedelta(days=45):
        return templates.TemplateResponse(
            request=request,
            name="registration.html",
            context={
                "year": year,
                "event_date": event_date_str,
                "registration_open": True,
                "opening_in_days": opening_in_days,
            },
        )
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "year": year,
            "event_date": event_date_str,
            "registration_open": False,
        },
    )


@app.post("/register", response_class=HTMLResponse)
def register_inquiry(request: Request, data: Annotated[RegistrationInquiry, Form()]):
    existing_entry = get_something_email("registrations", data.email)
    retry = False
    print(existing_entry)
    if existing_entry:
        return templates.TemplateResponse(
            request=request,
            name="success.html",
            context={
                "year": year,
                "event_date": event_date_str,
                "retry": retry,
                "status": "error",
                "message": [
                    "Oops! Something went wrong.",
                    "You are already registed, please check your email.",
                ],
            },
        )
    successed = insert_something("registrations", data.dict())
    if not successed:
        retry = True
        return templates.TemplateResponse(
            request=request,
            name="success.html",
            context={
                "year": year,
                "event_date": event_date_str,
                "retry": retry,
                "status": "error",
                "message": [
                    "Oops! Something went wrong.",
                    "There was an error submitting your registration. Please try again.",
                ],
            },
        )
    success_message = [
        "Thank you for your registration!",
        "We have received your registration and will review it shortly.",
    ]
    return templates.TemplateResponse(
        request=request,
        name="success.html",
        context={
            "year": year,
            "event_date": event_date_str,
            "retry": retry,
            "message": success_message,
            "status": "success",
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


@app.post("/volunteer", response_class=HTMLResponse)
def volunteer_inquiry(request: Request, data: Annotated[VolunteerInquiry, Form()]):
    """"""
    existing_entry = get_something_email("volunteerinquiry", data.email)
    retry = False
    if existing_entry:
        return templates.TemplateResponse(
            request=request,
            name="success.html",
            context={
                "year": year,
                "event_date": event_date_str,
                "retry": retry,
                "status": "error",
                "message": [
                    "Oops! Something went wrong.",
                    "You are already registered, please check your email.",
                ],
            },
        )

    successed = insert_something("volunteerinquiry", data.dict())
    if not successed:
        retry = True
        return templates.TemplateResponse(
            request=request,
            name="success.html",
            context={
                "year": year,
                "event_date": event_date_str,
                "retry": retry,
                "status": "error",
                "message": [
                    "Oops! Something went wrong.",
                    "There was an error submitting your registration. Please try again.",
                ],
            },
        )
    success_message = [
        "Thank you, We appreciate your interest in volunteering!",
        "We have received your registration and will review it shortly.",
    ]
    return templates.TemplateResponse(
        request=request,
        name="success.html",
        context={
            "year": year,
            "event_date": event_date_str,
            "retry": retry,
            "message": success_message,
            "status": "success",
        },
    )


@app.post("/waitlist", response_class=HTMLResponse)
def waitlist_inquiry(request: Request, data: Annotated[WaitlistInquiry, Form()]):
    existing_entry = get_something_email("waitlist", data.email)
    retry = False
    if existing_entry:
        return templates.TemplateResponse(
            request=request,
            name="success.html",
            context={
                "year": year,
                "event_date": event_date_str,
                "retry": retry,
                "status": "error",
                "message": [
                    "Oops! Something went wrong.",
                    "You are already on the waitlist.",
                ],
            },
        )
    successed = insert_something("waitlist", data.dict())
    if not successed:
        retry = True
        return templates.TemplateResponse(
            request=request,
            name="success.html",
            context={
                "year": year,
                "event_date": event_date_str,
                "retry": retry,
                "status": "error",
                "message": [
                    "Oops! Something went wrong.",
                    "There was an error submitting your registration. Please try again.",
                ],
            },
        )
    success_message = [
        "Thank you for your interest in our event!",
        "We have received your request and will notify you if a spot becomes available.",
    ]
    return templates.TemplateResponse(
        request=request,
        name="success.html",
        context={
            "year": year,
            "event_date": event_date_str,
            "retry": retry,
            "message": success_message,
            "status": "success",
        },
    )


@app.get("/proposal", response_class=HTMLResponse)
def proposal(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="speaker.html",
        context={"year": year},
    )


@app.post("/proposal", response_class=HTMLResponse)
def proposal_inquiry(request: Request, data: Annotated[Proposal, Form()]):
    successed = False
    retry = False

    existing_entry = get_something_email("proposals", data.email)
    print(existing_entry)
    if existing_entry:
        return templates.TemplateResponse(
            request=request,
            name="success.html",
            context={
                "year": year,
                "event_date": event_date_str,
                "retry": retry,
                "status": "error",
                "message": [
                    "Oops! Something went wrong.",
                    "We have already received a proposal from you. please feel free to reach out to us at pydevstogo@gmail.com.",
                ],
            },
        )

    successed = insert_something("proposals", data.dict())
    if not successed:
        retry = True
        return templates.TemplateResponse(
            request=request,
            name="success.html",
            context={
                "year": year,
                "event_date": event_date_str,
                "retry": retry,
                "root": "/proposal",
                "status": "error",
                "message": [
                    "Oops! Something went wrong.",
                    "There was an error submitting your proposal. Please try again.",
                ],
            },
        )
    success_message = [
        "Thank you for your proposal!",
        "We have received your proposal and will review it shortly.",
        # "We will get back to you if we have any questions or need more information.",
        # "If you have any questions, please feel free to reach out to us.",
        # "We appreciate your interest in speaking at our event.",
    ]
    return templates.TemplateResponse(
        request=request,
        name="success.html",
        context={
            "year": year,
            "event_date": event_date_str,
            "retry": retry,
            "message": success_message,
            "status": "success",
        },
    )


@app.get("/sponsor", response_class=HTMLResponse)
def sponsor(request: Request):
    
    headline = get_sponsortirtbytitle("headline")
    inkind = get_sponsortirtbytitle("inkind")

    return templates.TemplateResponse(
        request=request,
        name="sponsor.html",
        context={
            "year": year,
            "event_date": event_date_str,
            "headline": headline,
            "inkind": inkind,
            "sponsor_tiers": sponsor_tiers,
        },
    )


@app.post("/sponsor", response_class=JSONResponse)
def sponsor_inquiry(request: Request, data: Annotated[SponsorInquiry, Form()]):
    successed = False
    retry = False

    # check if the company has more than 2 inquiries
    # if company_sponsor_inquiry.count == 2 and company_email.count == 0:
    #     return templates.TemplateResponse(
    #         request=request,
    #         name="success.html",
    #         context={
    #             year": year,
    #             "event_date": event_date_str,
    #             "retry": retry,
    #             "status": "error",
    #         })

    successed = insert_something("sponsorinquiry", data.dict())
    if not successed:
        retry = True
        return templates.TemplateResponse(
            request=request,
            name="success.html",
            context={
                "year": year,
                "event_date": event_date_str,
                "retry": retry,
                "root": "/sponsor",
                "status": "error",
                "message": [
                    "Oops! Something went wrong.",
                    "There was an error submitting. Please try again.",
                ],
            },
        )

    return templates.TemplateResponse(
        request=request,
        name="success.html",
        context={
            "year": year,
            "event_date": event_date_str,
            "retry": retry,
            "message": [
                "Thank you, We appreciate your interest in sponsoring our event!",
                "We have received your inquiry and will review it shortly.",
                # "We will get back to you if we have any questions or need more information.",
                # "If you have any questions, please feel free to reach out to us.",
                # "We appreciate your interest in sponsoring our event.",
            ],
            "status": "success",
        },
    )


@app.get("/sponsors", response_class=HTMLResponse)
def sponsors(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="sponsors.html",
        context={"year": year},
    )


@app.get("/contact", response_class=HTMLResponse)
def contact(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="contact.html",
        context={
            "year": year,
            "sponsor_tiers": sponsor_tiers,
        },
    )


@app.get("/waitlist", response_class=HTMLResponse)
def waitlist(request: Request):
    if  opening_in > timedelta(days=45):
        return templates.TemplateResponse(
            request=request,
            name="waitlist.html",
            context={"year": year},
        )
    response = RedirectResponse(url="/register")
    return response


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            request=request, name="404.html", context={"year": year}, status_code=404
        )



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
