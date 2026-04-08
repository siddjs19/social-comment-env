from fastapi import FastAPI
from env.environment import SocialCommentEnv
from env.models import Action

app = FastAPI()

env = SocialCommentEnv()


@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.dict()


@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.dict(),
        "reward": reward.dict(),
        "done": done,
        "info": info
    }


@app.get("/state")
def state():
    return env.state().dict()

@app.get("/")
def root():
    return {
        "message": "Social Comment Environment API is running 🚀",
        "endpoints": ["/reset", "/step", "/state", "/docs"]
    }