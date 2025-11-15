from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse, JSONResponse
import secrets

app = FastAPI(title="RE4CTOR core-dev")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/random")
def random(
    n: int = Query(32, ge=1, le=4096),
    fmt: str = Query("hex")
):
    raw = secrets.token_bytes(n)
    if fmt.lower() == "hex":
        # простий варіант: голий hex
        return PlainTextResponse(raw.hex(), media_type="text/plain")
    # запасний JSON-формат
    return JSONResponse({"hex": raw.hex(), "n": n, "source": "core-dev"})
