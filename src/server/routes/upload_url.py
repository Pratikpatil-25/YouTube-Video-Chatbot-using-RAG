from fastapi import APIRouter, Form
from components.load_vectorstore import load_vectorstore
from fastapi.responses import JSONResponse
from logger import logger


router=APIRouter()

@router.post("/upload_url/")
async def upload_url(url: str = Form(...)):
    try:
        logger.info("Recieved uploaded URL")
        load_vectorstore(url)
        logger.info("Transcript document added to vectorstore")
        return {"messages":"URL processed and vectorstore updated"}
    except Exception as e:
        logger.info("Error during URL upload")
        return JSONResponse(status_code=500,content={"error":str(e)})