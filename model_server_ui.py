"""
This is an example of how to modify your existing model_server.py
to serve the UI. You should merge these changes into your existing model_server.py
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

# Your existing imports and code...

app = FastAPI()  # This should be your existing FastAPI app

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add a route to serve the UI
@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Redirect to the static HTML file
    return RedirectResponse(url="/static/index.html")

# Your existing API routes should be below here
# @app.post("/generate")
# async def generate_text(...):
#     ...

# @app.post("/chat/completions")
# async def chat_completions(...):
#     ...
