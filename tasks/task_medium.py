from env.environment import SocialCommentEnv


class MediumTask:

    def run(self, agent):
        env = SocialCommentEnv()
        env.simulator.current_scenario = 1
        obs = env.reset()

        escalation_penalty = 0
        total_reward = 0

        for _ in range(15):
            action = agent.act(obs)
            obs, reward, done, _ = env.step(action)

            total_reward += reward.score

            # Penalize high toxicity
            if obs.toxicity_score > 0.7:
                escalation_penalty += 1

            if done:
                break

        return self.grade(total_reward, escalation_penalty)

    def grade(self, total_reward, escalation_penalty):
        score = (total_reward + 15) / 30
        score -= escalation_penalty * 0.05

        return max(0.0, min(1.0, score))