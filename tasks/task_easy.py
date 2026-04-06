from env.environment import SocialCommentEnv
from env.models import Action


class EasyTask:

    def run(self, agent):
        env = SocialCommentEnv()
        obs = env.reset()

        total_reward = 0

        for _ in range(10):
            action = agent.act(obs)
            obs, reward, done, _ = env.step(action)

            total_reward += reward.score

            if done:
                break

        return self.grade(total_reward)

    def grade(self, total_reward):
        # Normalize score to 0–1
        score = (total_reward + 10) / 20
        return max(0.0, min(1.0, score))