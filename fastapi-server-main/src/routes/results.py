# routes/results.py
import msgpack
from fastapi import APIRouter
from starlette.responses import Response

from shared_resources import get_result

# Create the router
router = APIRouter()


# Define the endpoint to get the result
@router.get("/result/{task_id}")
async def get_task_result(task_id):
    result_data = get_result(task_id)
    if result_data is None:
        result_data = {"status": "not found"}
    packed_response = msgpack.packb(result_data)
    return Response(content=packed_response, media_type="application/octet-stream")
