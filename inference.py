import os
import json
from openai import OpenAI
from env import Env, Act

API_BASE_URL = os.getenv("API_BASE_URL", "https://api-inference.huggingface.co/v1/")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3-70b-chat-hf")
HF_TOKEN = os.getenv("HF_TOKEN")
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

def run():
    cli = OpenAI(
        api_key=HF_TOKEN,
        base_url=API_BASE_URL
    )
    env = Env()

    for tsk in [1, 2, 3]:
        print(f"START: {tsk}")
        obs = env.reset(tsk)
        don = False
        
        while not don:
            prm = f"Obs: {obs.model_dump_json()}. Act: rd, arc, rep. JSON: act, idx, txt."
            
            try:
                res = cli.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prm}]
                )
                out = res.choices[0].message.content
                try:
                    dct = json.loads(out)
                    act = Act(**dct)
                except:
                    act = Act(act="rd", idx=0)
            except:
                act = Act(act="rd", idx=0)

            obs, rew, don, inf = env.step(act)
            print(f"STEP: {rew}")

        print(f"END: {inf['score']}")

if __name__ == "__main__":
    run()