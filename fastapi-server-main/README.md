# FastAPI Server Workspace

Workspace for developing FastAPI servers.
Included is a simple server for processing numpy arrays.

## Build

Build the image:

```bash
./build_image.sh
```

Run the container:

```bash
./run_container.sh
```

Navigate to `src/`:

```bash
cd src
```

Start server with uvcorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8076 --reload
```

## Server Structure

The `src/` directory contains the server implementation.

### Main Components:

- `main.py`: The entry point of the application. Initializes the FastAPI application, includes routers, and defines
  global
  exception handlers.
- `routes/`: Defines the API routes/endpoints.
- `processes/`: Contains the logic for processing tasks.
- `process_manager.py`: Manages task queues and background processing threads.
- `shared_resources.py`: Handles shared resources like task results and model caching.

## How it Works

The server operates by receiving requests at a specific endpoint, queuing those requests, and
processing them asynchronously in the background. Results are temporarily stored and can be retrieved via another
endpoint.

The following process flow corresponds to the example numpy array processing server included in this template:

- **Receiving Data:** Data arrives through the `/process_np_array` endpoint, gets queued, and a unique task ID is
  returned
  immediately to the requester.
- **Processing Data:** A background task picks up data from the queue and processes it using a predefined function in
  `processes/process.py`.
- **Storing and Retrieving Results:** Once processing is complete, results are stored with the task ID as the key.
  Results can
  be retrieved using the `/result/{task_id}` endpoint.

## Adapting and Extending the Server

### Adding New Routes

1. Create a new router in `src/routes/`.
2. Define endpoints and their logic.
3. Include the new router in main.py.

### Implementing Additional Processes

1. Add new processing functions in src/processes/.
2. Update process_manager.py to recognize and handle the new task types.

## Shared Resources and Process Management

### `shared_resources.py`

This module manages shared resources like:

- **Results storage:** Results of tasks are stored in a thread-safe dictionary, accessible by task ID.
- **Model caching:** If your processes require model inference, you can implement caching mechanisms here to avoid
  reloading
  models on each request.

### `process_manager.py`

Handles the task queue and background processing:

- **Queue Management:** New tasks are added to a thread-safe queue.
- **Background Processing:** A background thread picks up tasks and processes them. It ensures that processing starts
  only if
  it's not already running, using threading locks to prevent race conditions.

## Usage

You can use the included server implementation via the following steps:

- **Processing Data:** Send numpy array data to `/process_np_array` and receive a task ID.
- **Retrieving Results:** Use the task ID to fetch results from `/result/{task_id}`.
  Conclusion

Check out the example client implementation at https://gitlab.proximityrobotics.com/common/http-client for a simple
client that interacts with the server.