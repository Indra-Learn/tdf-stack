# main.py
from fastapi import FastAPI

# Create a FastAPI application instance
app = FastAPI()

# Define a GET endpoint at the root URL ("/")
@app.get("/")
def read_root():
    """
    Handles GET requests to the root endpoint.
    Returns a simple JSON response.
    """
    return {"message": "Hello, World!"}
