from env.models import Reward, Action


class RewardEngine:

    def compute(self, comment, action: Action, state):
        tox = comment["toxicity"]
        user_flags = comment["user"]["flags"]

        score = 0.0
        reasons = []

        # -------------------------
        # 1. Toxicity Handling
        # -------------------------
        if tox > 0.8:
            if action.action_type == "delete":
                score += 1.0
                reasons.append("correctly removed high toxicity")
            elif action.action_type == "allow":
                score -= 1.2
                reasons.append("allowed severe toxicity")
            elif action.action_type == "warn":
                score += 0.6
                reasons.append("warned toxic user")

        elif 0.4 < tox <= 0.8:
            if action.action_type == "warn":
                score += 0.7
                reasons.append("handled medium toxicity well")
            elif action.action_type == "delete":
                score += 0.3
                reasons.append("slightly harsh moderation")
            elif action.action_type == "allow":
                score -= 0.5
                reasons.append("ignored problematic comment")

        else:  # low toxicity
            if action.action_type == "delete":
                score -= 0.7
                reasons.append("over-moderation")
            elif action.action_type == "allow":
                score += 0.4
                reasons.append("correctly allowed safe content")

        # -------------------------
        # 2. User History Impact
        # -------------------------
        if user_flags > 2:
            if action.action_type == "ban":
                score += 1.0
                reasons.append("removed repeat offender")
            elif action.action_type == "allow":
                score -= 0.6
                reasons.append("trusted risky user")

        # -------------------------
        # 3. Engagement Balance
        # -------------------------
        if action.action_type == "respond":
            score += 0.5
            state.engagement_score += 0.1
            reasons.append("boosted engagement")

        if action.action_type == "delete":
            state.engagement_score -= 0.05

        # -------------------------
        # 4. Platform Toxicity Drift
        # -------------------------
        if action.action_type == "allow":
            state.toxicity_level += tox * 0.1
        elif action.action_type in ["delete", "ban"]:
            state.toxicity_level -= tox * 0.1

        # Clamp values
        state.toxicity_level = max(0, min(1, state.toxicity_level))
        state.engagement_score = max(0, min(2, state.engagement_score))

        # -------------------------
        # 5. Small Step Penalty (avoid lazy agents)
        # -------------------------
        score -= 0.05
        score = max(0.01, min(0.99,score))
        return Reward(score=score)