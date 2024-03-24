from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .log_utils import CodeGenLogger
from .utils import CodeManager


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Create a single instance of CodeManager
code_manager = CodeManager()


# Dependency function to inject the code_manager instance
def get_code_manager():
    return code_manager


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, code_manager: CodeManager = Depends(get_code_manager)):
    try:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "generated_code": code_manager.generated_code},
        )
    except Exception as e:
        CodeGenLogger.lgr.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/generate_code/", response_class=HTMLResponse)
async def generate_code(
    request: Request,
    code_description: str = Form(...),
    lang: str = Form(...),
    code_manager: CodeManager = Depends(get_code_manager),
):
    try:
        generated_code = code_manager.generate_code(code_description, lang)
        return templates.TemplateResponse(
            "index.html", {"request": request, "generated_code": generated_code}
        )
    except Exception as e:
        CodeGenLogger.lgr.error(f"Error occurred while generating code: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/fix_code/", response_class=HTMLResponse)
async def fix_code(
    request: Request,
    fix_instructions: str = Form(...),
    code_manager: CodeManager = Depends(get_code_manager),
):
    try:
        fixed_code = code_manager.fix_code(fix_instructions)
        return templates.TemplateResponse(
            "index.html", {"request": request, "generated_code": fixed_code}
        )
    except Exception as e:
        CodeGenLogger.lgr.error(f"Error occurred while fixing code: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/execute_code/", response_class=HTMLResponse)
async def execute_generated_code(
    request: Request, code_manager: CodeManager = Depends(get_code_manager)
):
    try:
        execution_result = code_manager.execute_generated_code()
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "generated_code": code_manager.generated_code,
                "execution_result": execution_result,
            },
        )
    except Exception as e:
        CodeGenLogger.lgr.error(f"Error occurred while executing code: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
