"""FastAPI app with endpoints that demonstrate several Python concepts.

This is a compact demo. Each endpoint is intentionally small and focused so
you can read and extend the example. Run with:

    uvicorn app.samples.fastapi_concepts:app --reload

Endpoints include examples for:
- Data types, control flow, GIL note
- OOP (models & methods)
- regex
- file upload and download
- JSON/YAML handling
- exception handling
- decorators
- context managers
- dataclasses
- builtin functions
- logging, async, streaming, websockets (minimal)
"""

from __future__ import annotations

import asyncio
import io
import json
import logging
import re
import tempfile
from dataclasses import dataclass, asdict
from typing import Any, AsyncGenerator, Dict, List

import yaml
from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    File,
    Form,
    HTTPException,
    Request,
    Response,
    UploadFile,
    WebSocket,
)
from fastapi.responses import StreamingResponse, JSONResponse


app = FastAPI(title="FastAPI Concepts Demo")

# logging
logger = logging.getLogger("fastapi_concepts")
logging.basicConfig(level=logging.INFO)


# --- Data model / OOP & dataclass -------------------------------------------


@dataclass
class Item:
    id: int
    name: str
    price: float

    def tax_price(self, rate: float = 0.1) -> float:
        return self.price * (1 + rate)


IN_MEMORY_DB: Dict[int, Item] = {1: Item(1, "apple", 0.5)}


def get_item_or_404(item_id: int) -> Item:
    if item_id not in IN_MEMORY_DB:
        raise HTTPException(status_code=404, detail="Item not found")
    return IN_MEMORY_DB[item_id]


# --- Decorator example (simple cache) --------------------------------------


def simple_cache(func):
    cache: Dict[Any, Any] = {}

    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key in cache:
            logger.info("cache hit")
            return cache[key]
        val = func(*args, **kwargs)
        cache[key] = val
        return val

    return wrapper


@app.get("/item/{item_id}")
def read_item(item_id: int):
    """Return item as JSON and demonstrate dataclass -> dict."""
    item = get_item_or_404(item_id)
    return asdict(item)


@app.post("/item")
def create_item(name: str = Form(...), price: float = Form(...)):
    new_id = max(IN_MEMORY_DB.keys(), default=0) + 1
    item = Item(new_id, name, price)
    IN_MEMORY_DB[new_id] = item
    return asdict(item)


# --- Regex example ---------------------------------------------------------


@app.get("/regex/find_numbers")
def regex_numbers(text: str):
    nums = re.findall(r"\d+", text)
    return {"numbers": nums}


# --- File upload/download --------------------------------------------------


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # read small files into memory for demo
    content = await file.read()
    size = len(content)
    logger.info("Uploaded %s (%d bytes)", file.filename, size)
    return {"filename": file.filename, "size": size}


@app.get("/download/sample.txt")
def download_sample():
    data = "Sample text from server\n" * 10
    return Response(content=data, media_type="text/plain")


# --- JSON and YAML handling -----------------------------------------------


@app.post("/to_yaml")
def to_yaml(payload: Dict[str, Any]):
    # convert JSON payload to YAML
    return Response(content=yaml.safe_dump(payload), media_type="text/yaml")


# --- Exception handling & custom error ------------------------------------


class AppError(Exception):
    pass


@app.get("/error_demo")
def error_demo(bad: bool = False):
    if bad:
        raise AppError("demonstration error")
    return {"ok": True}


@app.exception_handler(AppError)
def app_error_handler(request: Request, exc: AppError):
    logger.exception("AppError occurred")
    return JSONResponse(status_code=400, content={"error": str(exc)})


# --- Builtin functions demo -----------------------------------------------


@app.get("/builtins/stats")
def builtin_stats(values: str):
    # expects comma-separated ints
    nums = [int(x) for x in values.split(",") if x.strip()]
    return {
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums) if nums else None,
        "max": max(nums) if nums else None,
    }


# --- Async / streaming ----------------------------------------------------


async def number_stream() -> AsyncGenerator[bytes, None]:
    for i in range(5):
        await asyncio.sleep(0.1)
        yield f"{i}\n".encode()


@app.get("/stream/numbers")
def stream_numbers():
    return StreamingResponse(number_stream(), media_type="text/plain")


# --- WebSocket echo (minimal) ---------------------------------------------


@app.websocket("/ws/echo")
async def ws_echo(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            await ws.send_text(f"echo: {data}")
    except Exception:
        await ws.close()


# --- Simple GIL note endpoint (explanatory) -------------------------------


@app.get("/gil")
def gil_note():
    return {
        "note": "Python has a GIL in CPython — it affects CPU-bound threads; use multiprocessing or asyncio for concurrency."
    }


# --- Logging demo & background task ---------------------------------------


def background_task(name: str) -> None:
    logger.info("running background task for %s", name)


@app.post("/background")
def run_background(name: str, bg: BackgroundTasks):
    bg.add_task(background_task, name)
    return {"started": name}


if __name__ == "__main__":
    print(
        "This module is a FastAPI app. Run with uvicorn as described in the file header."
    )
