from Agent import Agent
from Environments import Environment

if __name__ == '__main__':
    agent = Agent("Scemo")
    env = Environment(10, 10, agent)
    while True:
        print(env)
        if not env.step():
            break
        input("Press Enter to step...")