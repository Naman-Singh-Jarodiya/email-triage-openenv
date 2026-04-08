import sys
import os
import uvicorn
import fastapi
from typing import Optional, Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from env import Env, Act

app = fastapi.FastAPI()
en = Env()

@app.post("/reset")
def rs(rq: Optional[Dict[str, Any]] = None):
    tk = 1
    if rq and "task" in rq:
        tk = rq["task"]
    ob = en.reset(tk)
    return ob

@app.post("/step")
def st(at: Act):
    ob, rw, dn, ifo = en.step(at)
    re = {"observation": ob.model_dump(), "reward": rw, "done": dn, "info": ifo}
    return re

@app.get("/state")
def sa():
    ob = en.state()
    return ob

@app.get("/")
def ok():
    re = {"msg": "ok"}
    return re

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()