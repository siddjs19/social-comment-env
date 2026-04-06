from env.environment import SocialCommentEnv


class HardTask:

    def run(self, agent):
        env = SocialCommentEnv()
        obs = env.reset()

        total_reward = 0
        toxicity_spikes = 0
        engagement_score = 0

        for _ in range(20):
            action = agent.act(obs)
            obs, reward, done, _ = env.step(action)

            total_reward += reward.score

            if obs.toxicity_score > 0.8:
                toxicity_spikes += 1

            engagement_score += env.state().engagement_score

            if done:
                break

        return self.grade(total_reward, toxicity_spikes, engagement_score)

    def grade(self, total_reward, toxicity_spikes, engagement_score):
        score = (total_reward + 20) / 40

        # Penalize escalation
        score -= toxicity_spikes * 0.07

        # Reward engagement balance
        score += (engagement_score / 20) * 0.2

        return max(0.0, min(1.0, score))