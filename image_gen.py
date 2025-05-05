from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from queue import Queue
from threading import Thread
import time
import atexit
from fastapi.responses import JSONResponse, HTMLResponse

import uuid
import os

import image_gen_hf 

prodenv = os.getenv("PROD", "false")
print(f"PROD: {prodenv}")
if prodenv == "true":
    image_gen_hf.init()

# Create the FastAPI app
app = FastAPI()

# Set up the task queue for the worker
task_queue = Queue()

# Define the worker thread for background tasks
def worker():
    while True:
        job = task_queue.get()
        if job is None:  # Check for shutdown signal
            break
        try:
            print(f"Processing job: {job}")
            image_gen_hf.gen(job[0], filename=job[1], steps=10)
            print(f"Completed job: {job}")
        finally:
            task_queue.task_done()

# Start the worker thread when the application starts
worker_thread = Thread(target=worker, daemon=True)
worker_thread.start()

# Serve static files from the 'your_subdirectory' folder
app.mount("/image-gen/images", StaticFiles(directory="images"), name="images")

# Define a route to add jobs to the queue using a GET request with a 'prompt' parameter
@app.get("/image-gen/add-job/")
async def add_job(prompt: str):
    filename = f'images/{uuid.uuid1()}.png'
    # Add the 'prompt' value to the queue
    task_queue.put([prompt,filename])
    return {'prompt': prompt, 'image':filename}

# Gracefully shut down the worker thread when the app exits
def shutdown_worker():
    task_queue.put(None)  # Send shutdown signal to the worker
    worker_thread.join()  # Wait for the thread to finish

atexit.register(shutdown_worker)
