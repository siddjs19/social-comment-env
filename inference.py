import os
import requests
from openai import OpenAI

API_BASE = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.environ["MODEL_NAME"]

ENV_URL = os.environ.get("ENV_BASE_URL", "https://warriorsid-social-comment-env.hf.space")

client = OpenAI(
    base_url=API_BASE,
    api_key=API_KEY
)

TASK_NAME = "social-moderation"
BENCHMARK = "social-comment-env"


def get_action(observation):
    tox = observation["toxicity_score"]

    if tox < 0.2:
        return "allow"
    if tox > 0.9:
        return "delete"

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": f"""
You are a moderation agent.

Comment: {observation['comment']}
Toxicity: {tox}

Choose ONE word:
allow, respond, warn, delete

Only output one word.
"""
                }
            ],
            temperature=0
        )

        raw = response.choices[0].message.content.strip().lower()

    except Exception:
        return "allow"

    if "delete" in raw:
        return "delete"
    elif "warn" in raw:
        return "warn"
    elif "respond" in raw:
        return "respond"
    else:
        return "allow"


def log_start():
    print(f"[START] task={TASK_NAME} env={BENCHMARK} model={MODEL_NAME}", flush=True)


def log_step(step, action, reward, done, error):
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )



def run_episode():
    rewards = []
    steps_taken = 0
    success = False

    log_start()

    try:
        obs = requests.post(f"{ENV_URL}/reset", json={}).json()

        for step in range(1, 25):
            if "observation" in obs:
                current_obs = obs["observation"]
            else:
                current_obs = obs

            action = get_action(current_obs)

            res = requests.post(
                f"{ENV_URL}/step",
                json={"action_type": action}
            ).json()

            obs = res["observation"]
            reward = res["reward"]["score"]
            done = res["done"]

            rewards.append(reward)
            steps_taken = step

            log_step(step, action, reward, done, None)

            if done:
                break

        total_reward = sum(rewards)

        score = min(max(total_reward / 20, 0.0), 1.0)
        success = score > 0.3

    except Exception as e:
        log_step(steps_taken, "none", 0.0, True, str(e))
        score = 0.0

    finally:
        log_end(success, steps_taken, score, rewards)


if __name__ == "__main__":
    run_episode()