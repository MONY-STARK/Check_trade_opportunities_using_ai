# main.py

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from auth_data import AuthenticationData
from pipeline import TradePipeline
import uuid
import time



app = FastAPI()
templates = Jinja2Templates(directory="templates")
auth_data = AuthenticationData()
pipeline = TradePipeline()      
active_sessions = {}             



@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
def register_user(username: str = Form(...), password: str = Form(...)):
    auth_data.register_user(username, password)
    return RedirectResponse(url="/login", status_code=303)


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    error = request.query_params.get("error")
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": error
    })


@app.post("/login")
def login_user(username: str = Form(...), password: str = Form(...)):
    is_valid = auth_data.check_login(username, password)

    if not is_valid:
        return RedirectResponse(url="/login?error=1", status_code=303)


    session_id = str(uuid.uuid4())
    active_sessions[session_id] = {
        "username": username,
        "created_at": time.time(),
        "request_count": 0
    }

    response = RedirectResponse(url="/app", status_code=303)
    response.set_cookie(key="session_id", value=session_id)
    return response


@app.post("/logout")
def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id in active_sessions:
        del active_sessions[session_id]
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("session_id")
    return response




@app.get("/app", response_class=HTMLResponse)
def app_page(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in active_sessions:
        return RedirectResponse(url="/login", status_code=303)

    user = active_sessions[session_id]
    return templates.TemplateResponse("app.html", {
        "request": request,
        "username": user["username"]
    })


@app.get("/analyze", response_class=HTMLResponse)
def analyze(request: Request, sector: str):
    # Check session
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in active_sessions:
        return RedirectResponse(url="/login", status_code=303)
    active_sessions[session_id]["request_count"] += 1

    report = pipeline.analyze(sector)

    return templates.TemplateResponse("report.html", {
        "request": request,
        "sector": sector,
        "report": report
    })



@app.get("/download/{sector}")
def download(request: Request, sector: str):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in active_sessions:
        return RedirectResponse(url="/login", status_code=303)

    report = pipeline.analyze(sector)

    return PlainTextResponse(
        content=report,
        media_type="text/markdown",
        headers={
            "Content-Disposition": f"attachment; filename={sector}_report.md"
        }
    )
