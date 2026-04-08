import os
import json
import subprocess
import sys

try:
    from openai import OpenAI
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
    from openai import OpenAI

from env import Env, Act

bu = os.getenv("API_BASE_URL", "https://api-inference.huggingface.co/v1/")
mn = os.getenv("MODEL_NAME", "meta-llama/Llama-3-70b-chat-hf")
ht = os.getenv("HF_TOKEN")

def run():
    if not ht:
        print("Error: HF_TOKEN missing")
        return
    
    cl = OpenAI(api_key=ht, base_url=bu)
    ev = Env()

    for tk in [1, 2, 3]:
        print(f"START: {tk}")
        ob = ev.reset(tk)
        dn = False
        
        while not dn:
            pm = f"Obs: {ob.model_dump_json()}. Act: rd, arc, rep. JSON: act, idx, txt."
            try:
                rs = cl.chat.completions.create(
                    model=mn,
                    messages=[{"role": "user", "content": pm}]
                )
                ot = rs.choices[0].message.content
                js = json.loads(ot)
                ac = Act(**js)
            except Exception:
                ac = Act(act="rd", idx=0)

            ob, rw, dn, io = ev.step(ac)
            print(f"STEP: {rw}")

        print(f"END: {io['score']}")

if __name__ == "__main__":
    run()