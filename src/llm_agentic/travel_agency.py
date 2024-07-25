from fastapi import FastAPI, Request
from starlette.templating import Jinja2Templates

from llm_agentic.utils import TEMPLATE_DIR

templates = Jinja2Templates(directory=TEMPLATE_DIR)

app = FastAPI()  # This is the app object


@app.get("/", name="home")
def home(request: Request):
    return templates.TemplateResponse("home.html", dict(request=request, title="Home"))


# Let's setup the paths for DB and Templates

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "llm_agentic.travel_agency:app", host="0.0.0.0", port=8000, reload=True
    )  # arg1 = package.module:app
