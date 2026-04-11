from env.models import Reward

class RewardEngine:

    def compute(self, comment, action, state):
        # 🔒 Safety: handle None
        if comment is None:
            return Reward(score=0.5, reason="no comment fallback")

        tox = comment.get("toxicity", 0.0)

        # 🎯 Base scoring logic
        if action.action_type == "delete":
            score = 0.8 if tox > 0.7 else 0.2
            reason = "delete decision"

        elif action.action_type == "warn":
            score = 0.6
            reason = "warn decision"

        elif action.action_type == "respond":
            score = 0.5
            reason = "respond decision"

        else:  # allow
            score = 0.3
            reason = "allow decision"

        # 📉 Optional state influence
        if state is not None and state.step_count > 10:
            score *= 0.9
            reason += " (late step penalty)"

        # 🔥 REQUIRED: clamp between (0,1)
        score = max(0.01, min(0.99, score))

        return Reward(score=score, reason=reason)