from game import Game as game
import pygame
from config import *
from random import *
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import median, mean
import numpy as np
import datetime
import shortuuid
import math

steps = 600
reward_requirement = 50
games = 5000

def random_games( epochs=10, steps=300):
  for e in range(epochs):
    env = game()
    env.resetGame()
    action = 3
    pygame.event.get()

    for step in range(steps):
      action = MOVING_ACTIONS[randrange(0,3)][action]
    
      env.render()
      obs, reward, done = env.step(action)
      if done: 
        env.resetGame()
        break

def generate_population(model, games=games, noaccepted=False):
  global reward_requirement
  training_data = []
  rewards = []
  accepted_rewards = []
  env = game()

  for game_nb in range(games):
    print(f'Simulation {game_nb} out of {games} \r', end='')
    env.resetGame()
    total_reward = 0
    game_memory = []
    prev_observation = []
    direction = 3

    for step in range(steps):
      if len(prev_observation) == 0 or not model:
        action = randrange(0,3)
      else:
        prediction = model.predict(prev_observation.reshape(-1, len(prev_observation), 1))
        action = np.argmax(prediction[0])

      direction = MOVING_ACTIONS[action][direction]
      observation, reward, done = env.step(direction)

      if len(prev_observation) > 0:
        game_memory.append([prev_observation, action])
      prev_observation = observation
      total_reward += reward
      if done: break

    if total_reward >= reward_requirement:
      accepted_rewards.append(total_reward)
      for data in game_memory:
        output = [0, 0, 0]
        output[data[1]] = 1
        training_data.append([data[0], output])

    rewards.append(total_reward)

  print("-----TRAINING-----")
  print(f'Average Total Reward: {mean(rewards)}')
  if not noaccepted: print(f'Average Accepted Total Reward: {mean(accepted_rewards)}')
  print("------------------")
  if not noaccepted: reward_requirement = mean(accepted_rewards)
  return training_data

def create_neural_network_model(training_data):
  input_size = len(np.array([i[0] for i in training_data]).reshape(-1, len(training_data[0][0]), 1)[0])
  output_size = len(training_data[0][1])
  network = input_data(shape=[None, input_size, 1], name='input')
  network = tflearn.fully_connected(network, 32)
  network = tflearn.fully_connected(network, 32)
  network = fully_connected(network, output_size, activation='softmax')
  network = regression(network, name='targets')
  return tflearn.DNN(network, tensorboard_dir='tflearn_logs', tensorboard_verbose=0)

def train_model(training_data, model=False):
  x = np.array([i[0] for i in training_data]).reshape(-1, len(training_data[0][0]), 1)
  y = [i[1] for i in training_data]
  model.fit({'input': x}, {'targets': y}, n_epoch=10, batch_size=16, show_metric=False)
  return model

def evaluate(model,games=3):
    scores = []
    env = game()
    for each_game in range(games):
        score = 0
        prev_obs = []
        env.resetGame()
        direction = 3
        for _ in range(steps):
            env.render()
 
            if len(prev_obs) == 0:
                action = randrange(0, 3)
            else:
                prediction = model.predict(prev_obs.reshape(-1, len(prev_obs), 1))
                action = np.argmax(prediction[0])

            direction = MOVING_ACTIONS[action][direction]
            new_observation, reward, done = env.step(direction)
            prev_obs = np.array(new_observation)
            score += reward
            if done: break
 
        scores.append(score)
    print("-----EVALUATION-----")
    print(f'Average Score is {mean(scores)}')
    print("--------------------")
    return mean(scores)

def saveModel(model, modelname):
  model.save(modelname)

def loadModel(modelname):
  training_data = generate_population(None, games=100, noaccepted=True)
  model = create_neural_network_model(training_data)
  model.load(modelname)
  return model

def trainAI(generations=7):
  training_data = generate_population(None, games=5000)
  model = create_neural_network_model(training_data)
  model = train_model(training_data, model)
  generation = 1
  evaluations = []
  while generation <= generations:
    print(f'Generation: {generation}, Reward Requirement: {reward_requirement}')
    generation += 1
    training_data = np.append(training_data, generate_population(model, games=1000), axis=0)
    model = train_model(training_data, model)
    mean = evaluate(model)
    modelname = f"Models/model{generation}-{shortuuid.uuid()}.tfl"
    saveModel(model, modelname)
    evaluations.append([modelname, mean])

def playAsAI(modelname='PreTrainedModels/model1400.tfl', games=10):
  model = loadModel(modelname)
  evaluate(model, games=games)
