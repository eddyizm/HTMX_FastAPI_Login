from fastapi import Depends, FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from models import User
from schema import users, database
from security import AuthHandler, RequiresLoginException


app = FastAPI()
# load static files
app.mount("/static", StaticFiles(directory="static"), name="static")
# load templates
templates = Jinja2Templates(directory="templates")
auth_handler = AuthHandler()

# redirection block
@app.exception_handler(RequiresLoginException)
async def exception_handler(request: Request, exc: RequiresLoginException) -> Response:
    ''' this handler allows me to route the login exception to the login page.'''
    return RedirectResponse(url='/')        


@app.middleware("http")
async def create_auth_header(
    request: Request,
    call_next,):
    '''
    Check if there are cookies set for authorization. If so, construct the
    Authorization header and modify the request (unless the header already
    exists!)
    '''
    if ("Authorization" not in request.headers 
        and "Authorization" in request.cookies
        ):
        access_token = request.cookies["Authorization"]
        
        request.headers.__dict__["_list"].append(
            (
                "authorization".encode(),
                 f"Bearer {access_token}".encode(),
            )
        )
    elif ("Authorization" not in request.headers 
        and "Authorization" not in request.cookies
        ): 
        request.headers.__dict__["_list"].append(
            (
                "authorization".encode(),
                 f"Bearer 12345".encode(),
            )
        )
        
    
    response = await call_next(request)
    return response    


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html",
     {"request": request})


@app.get("/register/", response_class=HTMLResponse)
async def registration(request: Request):
    return templates.TemplateResponse("register.html",
     {"request": request})


@app.post("/register/", response_class=HTMLResponse)
async def register(request: Request, email: str = Form(...), password: str = Form(...)):
    user = User(email = email,
        password= password)    
    query = users.insert().values(email = user.email,
        password= auth_handler.get_hash_password(user.password))
    result = await database.execute(query)
    # TODO verify success and handle errors
    response = templates.TemplateResponse("success.html", 
              {"request": request, "success_msg": "Registration Successful!",
              "path_route": '/', "path_msg": "Click here to login!"})
    return response
    

@app.post("/login/")
async def sign_in(request: Request, response: Response,
    username: str = Form(...), password: str = Form(...)):
    try:
        user = User(email = username,
            password= password)  
        if await auth_handler.authenticate_user(user.email, user.password):
            atoken = auth_handler.create_access_token(user.email)
            response = templates.TemplateResponse("success.html", 
              {"request": request, "USERNAME": user.email, "success_msg": "Welcome back! ",
              "path_route": '/private/', "path_msg": "Go to your private page!"})
            
            response.set_cookie(key="Authorization", value= f"{atoken}", httponly=True)
            return response
        else:
            return templates.TemplateResponse("error.html",
            {"request": request, 'detail': 'Incorrect Username or Password', 'status_code': 404 })
    
    except Exception as err:
        return templates.TemplateResponse("error.html",
            {"request": request, 'detail': 'Incorrect Username or Password', 'status_code': 401 })
        

@app.get("/private/", response_class=HTMLResponse)
async def private(request: Request, email=Depends(auth_handler.auth_wrapper)):
    try:
        return templates.TemplateResponse("private.html",
            {"request": request})
    except:
        raise RequiresLoginException() 
