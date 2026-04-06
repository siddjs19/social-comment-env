import random


class ThreadSimulator:

    def __init__(self):
        self.thread = []
        self.turn = 0

    def reset(self):
        self.thread = []
        self.turn = 0

        first = self._generate_base_comment()
        self.thread.append(first)
        return first

    def step(self, action_type):
        last = self.thread[-1]
        self.turn += 1

        next_comment = self._generate_reply(last, action_type)
        self.thread.append(next_comment)

        return next_comment

    # -------------------------

    def _generate_base_comment(self):
        samples = [
            {"text": "This idea is interesting", "toxicity": 0.2},
            {"text": "This is stupid", "toxicity": 0.7},
            {"text": "You're an idiot", "toxicity": 0.9},
        ]

        base = random.choice(samples)

        return {
            "text": base["text"],
            "toxicity": base["toxicity"],
            "user": {"flags": random.randint(0, 2)},
            "topic": random.choice(["tech", "gaming", "politics", "general"])
        }

    def _generate_reply(self, last_comment, action_type):
        tox = last_comment["toxicity"]

        # Escalation logic
        if action_type == "allow":
            tox = min(1.0, tox + random.uniform(0.1, 0.3))
        elif action_type in ["warn", "respond"]:
            tox = max(0.0, tox - random.uniform(0.1, 0.3))
        elif action_type in ["delete", "ban"]:
            tox = random.uniform(0.0, 0.3)

        text_templates = [
            "I disagree with you",
            "You're wrong",
            "This is getting dumb",
            "Okay chill",
            "Let’s keep it civil"
        ]

        return {
            "text": random.choice(text_templates),
            "toxicity": round(tox, 2),
            "user": {"flags": random.randint(0, 3)},
            "topic": "general"
        }