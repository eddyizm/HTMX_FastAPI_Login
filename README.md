# HTMX_FastAPI_Login
HTMX and FastAPI login demo.

### youtube video coming soon.

Start by setting up your virtual environment and activating it. 

```
# create virtual env
python -m venv env

# activate virtual env (linux)
source env/bin/activate

# activate virtual env (windows)
source env/Scripts/activate
```
Upgrade pip because for some reason this is still a thing. 

```
python -m pip install --upgrade pip
```

Then install the FastAPI and required libraries.(note you can skip this step and just install the requirements.txt file)

```
pip install fastapi email-validator pydantic
```
and the uvicorn server

```  
pip install "uvicorn[standard]"

``` 

launch server
```
uvicorn main:app --reload
```

We will need jinja templates to render pages  

```  
pip install jinja2 python-multipart
```

Next we add databases and sqlalchemy 
```
pip install sqlalchemy databases aiosqlite
```

Security and cryptography libraries
```
pip install python-jose passlib cryptography bcrypt
```
