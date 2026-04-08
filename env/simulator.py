class ThreadSimulator:

    def __init__(self):
        self.thread = []
        self.turn = 0

        # Predefined deterministic scenarios
        self.scenarios = [
            [
                {"text": "This is stupid", "toxicity": 0.7},
                {"text": "You're wrong", "toxicity": 0.8},
                {"text": "You're an idiot", "toxicity": 0.9},
            ],
            [
                {"text": "Nice idea!", "toxicity": 0.2},
                {"text": "I disagree", "toxicity": 0.3},
                {"text": "Let's keep it civil", "toxicity": 0.1},
            ],
            [
                {"text": "Worst post ever", "toxicity": 0.8},
                {"text": "Shut up", "toxicity": 0.9},
                {"text": "Calm down guys", "toxicity": 0.4},
            ]
        ]

        self.current_scenario = 0

    def reset(self):
        self.turn = 0
        scenario = self.scenarios[self.current_scenario]

        # rotate scenario each episode deterministically
        self.current_scenario = (self.current_scenario + 1) % len(self.scenarios)

        first = self._format_comment(scenario[0])
        self.thread = [first]

        return first

    def step(self, action_type):
        self.turn += 1

        scenario = self.scenarios[self.current_scenario - 1]

        if self.turn < len(scenario):
            next_comment = self._format_comment(scenario[self.turn])
        else:
            # stable fallback
            next_comment = self._format_comment(scenario[-1])

        self.thread.append(next_comment)

        return next_comment

    def _format_comment(self, base):
        return {
            "text": base["text"],
            "toxicity": base["toxicity"],
            "user": {"flags": int(base["toxicity"] * 3)},
            "topic": "general"
        }