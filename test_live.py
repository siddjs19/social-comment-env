import requests
import random

BASE = "https://warriorsid-social-comment-env.hf.space"

def test_env():
    print("Resetting...")
    obs = requests.get(f"{BASE}/reset").json()

    assert "comment" in obs
    assert "toxicity_score" in obs

    actions = ["allow", "delete", "warn", "respond", "ban"]

    for step in range(10):
        action = {"action_type": random.choice(actions)}

        res = requests.post(f"{BASE}/step", json=action).json()

        assert "reward" in res
        assert "observation" in res

        print(f"Step {step}: ", res["reward"])

    print("✅ Test passed")


if __name__ == "__main__":
    test_env()