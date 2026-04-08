from pydantic import BaseModel
from typing import List, Dict, Any, Tuple

class Obs(BaseModel):
    eml: List[Dict[str, str]]
    idx: int

class Act(BaseModel):
    act: str
    idx: int
    txt: str = ""

class Rew(BaseModel):
    val: float

class Env:
    def __init__(self):
        self.tsk = 1
        self.eml = []
        self.idx = 0
        self.stp = 0
        self.lmt = 15

    def reset(self, tsk: int = 1) -> Obs:
        self.tsk = tsk
        self.stp = 0
        self.idx = 0
        if tsk == 1:
            self.eml = [{"sub": "hi", "txt": "hello", "sts": "new"}]
        elif tsk == 2:
            self.eml = [{"sub": "bill", "txt": "pay 10", "sts": "new"}, {"sub": "win", "txt": "cash", "sts": "new"}]
        else:
            self.eml = [{"sub": "bug", "txt": "fix", "sts": "new"}, {"sub": "eat", "txt": "food", "sts": "new"}, {"sub": "bad", "txt": "err", "sts": "new"}]
        return self.state()

    def state(self) -> Obs:
        return Obs(eml=self.eml, idx=self.idx)

    def step(self, act: Act) -> Tuple[Obs, float, bool, Dict[str, Any]]:
        self.stp += 1
        rew = 0.0
        don = False

        if act.idx < 0 or act.idx >= len(self.eml):
            rew = -0.1
        else:
            obj = self.eml[act.idx]
            if act.act == "rd":
                obj["sts"] = "rd"
                rew = 0.1
            elif act.act == "arc":
                if obj["sts"] == "new":
                    rew = 0.2
                obj["sts"] = "arc"
            elif act.act == "rep":
                if len(act.txt) > 0:
                    rew = 0.3
                obj["sts"] = "rep"
            else:
                rew = -0.1

        don = True
        scr = 0.0
        tot = len(self.eml)
        dn = 0
        for itm in self.eml:
            if itm["sts"] == "new":
                don = False
            else:
                dn += 1

        scr = dn / tot
        if self.stp >= self.lmt:
            don = True

        return self.state(), rew, don, {"score": scr}