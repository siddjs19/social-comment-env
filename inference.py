import os
import requests
from dotenv import load_dotenv

load_dotenv()

ENV_BASE = os.getenv("ENV_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

TASK_NAME = "social-moderation"
BENCHMARK = "social-comment-env"

# -------------------------
# RULE-BASED AGENT (deterministic)
# -------------------------
def get_action(observation):
    tox = observation["toxicity_score"]

    if tox < 0.2:
        return "allow"
    elif tox < 0.4:
        return "respond"
    elif tox < 0.7:
        return "warn"
    elif tox < 0.9:
        return "delete"
    else:
        return "ban"


# -------------------------
# LOG FUNCTIONS (STRICT)
# -------------------------
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


# -------------------------
# RUN EPISODE
# -------------------------
def run_episode():
    rewards = []
    steps_taken = 0
    success = False

    log_start()

    try:
        obs = requests.get(f"{ENV_BASE}/reset").json()

        for step in range(1, 21):
            action = get_action(obs)

            res = requests.post(
                f"{ENV_BASE}/step",
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

        # normalize score (simple scaling)
        total_reward = sum(rewards)
        score = min(max(total_reward / 20, 0.0), 1.0)

        success = score > 0.3

    except Exception as e:
        log_step(steps_taken, "none", 0.0, True, str(e))
        score = 0.0

    finally:
        log_end(success, steps_taken, score, rewards)


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    run_episode()