from fastapi import HTTPException,Request
from fastapi.responses import JSONResponse
from app.core.config import settings


async def http_exception_handler(request: Request, exc : HTTPException):
    
    status_code = exc.status_code
    detail = exc.detail
    return JSONResponse(content={'detail' : detail},status_code=status_code)


async def unhandled_exception_handler(request : Request, exc : Exception):

    if settings.DEBUG == True:
        detail =str(exc)
        
    else:
        detail = "Internal Server Error"

    return JSONResponse(status_code=500,content={'detail' : detail})