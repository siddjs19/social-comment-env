from env.environment import SocialCommentEnv
from env.models import Action

env = SocialCommentEnv()
obs = env.reset()

for _ in range(5):
    print("Comment:", obs.comment)

    action = Action(action_type="delete")

    obs, reward, done, _ = env.step(action)

    print("Reward:", reward.score, reward.reason)