from fastapi import FastAPI
from typing import Optional, Dict, Any
from env import Env, Act

app = FastAPI()
env = Env()

@app.post("/reset")
def rst(req: Optional[Dict[str, Any]] = None):
    tsk = 1
    if req and "task" in req:
        tsk = req["task"]
    return env.reset(tsk)

@app.post("/step")
def stp(act: Act):
    obs, rew, don, inf = env.step(act)
    return {
        "observation": obs.model_dump(),
        "reward": rew,
        "done": don,
        "info": inf
    }

@app.get("/state")
def sta():
    return env.state()

@app.get("/")
def rty():
    return {"msg": "ok"}