import os
import json
import subprocess
import sys

# Missing module fix
try:
    from openai import OpenAI
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
    from openai import OpenAI

from env import Env, Act

# Configurations
bu = os.getenv("API_BASE_URL", "https://api-inference.huggingface.co/v1/")
mn = os.getenv("MODEL_NAME", "meta-llama/Llama-3-70b-chat-hf")
ht = os.getenv("HF_TOKEN")

def run():
    if not ht:
        return
    
    cl = OpenAI(api_key=ht, base_url=bu)
    ev = Env()

    for tk in [1, 2, 3]:
        # Required START format
        print(f"[START] task={tk}", flush=True)
        
        ob = ev.reset(tk)
        dn = False
        step_count = 0
        
        while not dn:
            step_count += 1
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
            
            # Required STEP format
            print(f"[STEP] step={step_count} reward={rw}", flush=True)

        # Required END format
        print(f"[END] task={tk} score={io['score']} steps={step_count}", flush=True)

if __name__ == "__main__":
    run()