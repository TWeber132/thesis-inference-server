# routes/process_routes.py
import uuid
import msgpack
from fastapi import APIRouter, Request, BackgroundTasks
from starlette.responses import Response

from process_manager import start_processing_if_not_started, _process_queue
from shared_resources import set_result

# Create the router
router = APIRouter()


# Define the endpoint to process the numpy array
@router.post("/process_np_array")
async def process_np_array(request: Request, background_tasks: BackgroundTasks):
    # Get the data from the request
    byte_data = await request.body()
    # Create a unique task id
    task_id = str(uuid.uuid4())

    # Set the result to pending
    set_result(task_id, {"status": "pending"})

    # Add the task to the queue
    task_type = "process_np_array"
    _process_queue.put((task_type, byte_data, task_id))

    # Start the processing if it is not started
    start_processing_if_not_started(background_tasks)

    # Return the task id
    packed_response = msgpack.packb({"task_id": task_id})
    return Response(content=packed_response, media_type="application/octet-stream")
