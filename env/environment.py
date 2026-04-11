import random
from env.models import Observation, Action, Reward, State
from env.reward import RewardEngine
from env.simulator import ThreadSimulator

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

class SocialCommentEnv:

    def __init__(self):
        self.state_data = None
        self.current_comment = None
        self.reward_engine = RewardEngine()
        self.simulator = ThreadSimulator()
        self.current_task = "easy"

    def reset(self, scenario=0, task_name="easy"):
        self.current_task = task_name
        self.simulator.current_scenario = scenario

        self.state_data = State(
            comments_handled=0,
            toxicity_level=0.0,
            engagement_score=1.0,
            banned_users=0,
            step_count=0
        )

        first_comment = self.simulator.reset()
        self.current_comment = first_comment

        return self._get_observation()

    def step(self, action: Action):
        reward = self._compute_reward(action)

        self.state_data.comments_handled += 1
        self.state_data.step_count += 1

        # Generate next comment based on action
        self.current_comment = self.simulator.step(action.action_type)

        done = self.state_data.step_count >= 20

        return self._get_observation(), reward, done, {}

    def state(self):
        return self.state_data

    # ------------------------

    def _get_observation(self):
        comment = self.current_comment

        return Observation(
            comment=comment.get("text", ""),
            user_history=comment.get("user", {"flags": 0}),
            post_topic=comment.get("topic", "general"),
            toxicity_score=comment.get("toxicity", 0.0),
            step_count=self.state_data.step_count
        )

    def _generate_comment(self):
        samples = [
            {"text": "I love this!", "toxicity": 0.1, "topic": "tech", "user": {"flags": 0}},
            {"text": "This is trash", "toxicity": 0.6, "topic": "gaming", "user": {"flags": 1}},
            {"text": "You're an idiot", "toxicity": 0.9, "topic": "politics", "user": {"flags": 3}},
        ]
        return random.choice(samples)

    def _compute_reward(self, action: Action):
        if self.current_comment is None:
            from env.models import Reward
            return Reward(score=0.5)  # safe default

        return self.reward_engine.compute(
            self.current_comment,
            action,
            self.state_data
        )