import torch
import random
import numpy as np
from collections import deque
from controller import Controller
from model import Linear_QNet, QTrainer
from helper import plot
import time

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(10, 256, 5)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, controller):
        state = controller.get_state()
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0,0,0]
        if random.randint(0, 400) < self.epsilon:
            move = random.randint(0, 4)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    num_players = 3
    agent = Agent()

    # Load pre-trained models if available
    # try:
    #     agent.load_model()
    #     print("Pre-trained models loaded successfully.")
    # except Exception as e:
    #     print("No pre-trained models found. Starting from scratch.")

    controllers = [Controller() for _ in range(num_players)]
    for controller in controllers:
        controller.connect()

    while True:
        for player_id in range(num_players):
            # get old state
            state_old = agent.get_state(controllers[player_id])

            # get move
            final_move = agent.get_action(state_old)
            print(final_move)

            # wait 1 mili seconds
            time.sleep(0.005)

            # perform move and get new state
            reply = controllers[player_id].play_step(final_move)

            reward = reply['reward']
            game_over = reply['game_over']
            score = reply['score']

            state_new = agent.get_state(controllers[player_id])

            # train short memory
            agent.train_short_memory(state_old, final_move, reward, state_new, game_over)

            # remember
            agent.remember(state_old, final_move, reward, state_new, game_over)

            if game_over:
                # train long memory, plot result
                agent.n_games += 1
                agent.train_long_memory()

                if score > record:
                    record = score
                    agent.model.save()

                # print('Game', agent.n_games, 'Score', score, 'Record:', record)

                plot_scores.append(score)
                total_score += score
                mean_score = total_score / agent.n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)

                break


if __name__ == '__main__':
    train()