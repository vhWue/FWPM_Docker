from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/clubs")
async def get_club():
   json_content = {"club": "Liverpool"}
   return JSONResponse(content=json_content, status_code=status.HTTP_200_OK)