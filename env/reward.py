from env.models import Reward, Action


class RewardEngine:

    def compute(self,comment,action: Action,state):
        base_reward = self.compute(
            self.current_comment,
            action,
            self.state_data
        ).score

        # 🔥 task-specific grading
        if self.current_task == "easy":
            score = base_reward * 0.8

        elif self.current_task == "medium":
            score = base_reward

        elif self.current_task == "hard":
            score = base_reward * 1.2

        else:
            score = base_reward

        # 🔥 clamp
        score = max(0.01, min(0.99, score))

        return Reward(score=score)