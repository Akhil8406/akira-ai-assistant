from ollama import chat


class AkiraBrain:
    def __init__(self):
        self.model = "qwen3:4b"

        self.system_prompt = """
You are AKIRA, a personal AI desktop assistant.

Your personality:
- Calm
- Intelligent
- Concise
- Helpful
- Natural

You are running locally on the user's Windows laptop.

Keep spoken responses concise unless the user asks for
a detailed explanation.

Do not pretend that you performed computer actions unless
the desktop assistant actually provides you with that ability.
"""

        self.history = []

    def ask(self, message):
        self.history.append({"role": "user", "content": message})

        messages = [{"role": "system", "content": self.system_prompt}] + self.history

        try:
            response = chat(model=self.model, messages=messages)

            answer = response.message.content.strip()

            self.history.append({"role": "assistant", "content": answer})

            return answer

        except Exception as error:
            print(f"AKIRA brain error: {error}")

            return "I'm having trouble accessing my local AI system."


if __name__ == "__main__":
    brain = AkiraBrain()

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        answer = brain.ask(user_input)

        print(f"\nAKIRA: {answer}")
