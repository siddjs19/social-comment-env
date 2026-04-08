from fastapi import FastAPI
from env.environment import SocialCommentEnv
from env.models import Action

app = FastAPI()

env = SocialCommentEnv()


@app.post("/reset")
def reset():
    return {
        "observation": {
            "comment": "test",
            "toxicity_score": 0.5,
            "user_history": 1
        }
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



# -------------------------
# REQUIRED FOR OPENENV
# -------------------------
def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()