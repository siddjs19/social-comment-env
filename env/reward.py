from env.models import Reward

class RewardEngine:

    def compute(self, comment, action, state):
        tox = comment.get("toxicity", 0.0)

        if action.action_type == "delete":
            score = 0.8 if tox > 0.7 else 0.2

        elif action.action_type == "warn":
            score = 0.6

        elif action.action_type == "respond":
            score = 0.5

        else:  # allow
            score = 0.3

        # Optional: use state
        if state.step_count > 10:
            score *= 0.9

        # 🔥 IMPORTANT (grader requirement)
        score = max(0.01, min(0.99, score))

        return Reward(score=score)