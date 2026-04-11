from fastapi import FastAPI
import uvicorn
from env.environment import SocialCommentEnv
from env.models import Action
from fastapi import Request

app = FastAPI()

env = SocialCommentEnv()


@app.post("/reset")
async def reset(request: Request):
    body = await request.json()
    task = body.get("task", {})

    scenario = 0
    if task.get("name") == "medium":
        scenario = 1
    elif task.get("name") == "hard":
        scenario = 2

    obs = env.reset(scenario=scenario)

    return {
        "observation": obs.dict()
    }


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


def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()