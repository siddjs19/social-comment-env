from env.models import Reward

class RewardEngine:

    def compute(self, comment, action, state, task="easy"):

        if comment is None:
            base = 0.5
        else:
            tox = comment.get("toxicity", 0.0)

            if action.action_type == "delete":
                base = 0.7 if tox > 0.7 else 0.3
            elif action.action_type == "warn":
                base = 0.6
            elif action.action_type == "respond":
                base = 0.5
            else:
                base = 0.4

        # 🔥 STEP VARIATION
        if state:
            base += (state.step_count % 3) * 0.05   # small variation

        # 🔥 TASK SEPARATION (IMPORTANT)
        if task == "easy":
            score = base * 0.5
        elif task == "medium":
            score = base * 0.8
        elif task == "hard":
            score = base * 1.2
        else:
            score = base

        # clamp
        score = max(0.01, min(0.99, score))

        return Reward(
            score=score,
            reason=f"{task} task grading"
        )