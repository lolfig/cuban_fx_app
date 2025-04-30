from pydantic import BaseModel

from app import app
from fastapi import Form, Cookie
from fastapi.responses import JSONResponse, RedirectResponse


class LoginObject(BaseModel):
  username: str
  password: str


@app.post("/login")
def login(login_form: LoginObject = Form()):
  """
  Login function
  """
  # Check if the username and password are correct
  if login_form.username == "admin" and login_form.password == "admin":
    # Set the session cookie
    response = RedirectResponse(url="/dash", status_code=303)
    response.set_cookie(key="session", value="session_value")
    return response
  else:
    return JSONResponse(
      content={"message": "Invalid username or password"},
      status_code=401
    )


@app.post("/logout")
def logout():
  """
  Logout function
  """
  response = RedirectResponse(url="/dash", status_code=303)
  response.delete_cookie(key="session")
  return response
