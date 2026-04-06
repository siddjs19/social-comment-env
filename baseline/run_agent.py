from env.models import Action
import random


class RandomAgent:

    def act(self, obs):
        actions = ["allow", "delete", "warn", "respond", "ban"]
        return Action(action_type=random.choice(actions))


if __name__ == "__main__":
    from tasks.task_easy import EasyTask
    from tasks.task_medium import MediumTask
    from tasks.task_hard import HardTask

    agent = RandomAgent()

    print("Easy:", EasyTask().run(agent))
    print("Medium:", MediumTask().run(agent))
    print("Hard:", HardTask().run(agent))