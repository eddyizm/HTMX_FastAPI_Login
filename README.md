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

Then install the FastAPI and required libraries.  
*note you can just install the requirements.txt*

```
pip install -r requirements.txt
```

launch server
```
uvicorn main:app --reload
```
and open in [browser](http://localhost:8000/)    
