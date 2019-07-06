import gym
import tensorflow as tf
import numpy as np
import random

# General Parameters
# -- DO NOT MODIFY --
ENV_NAME = 'CartPole-v0'
EPISODE = 200000  # Episode limitation
STEP = 200  # Step limitation in an episode
TEST = 10  # The number of tests to run every TEST_FREQUENCY episodes
TEST_FREQUENCY = 100  # Num episodes to run before visualizing test accuracy

# TODO: HyperParameters
GAMMA = 0.98
INITIAL_EPSILON = 1.0
FINAL_EPSILON = 0.001
EPSILON_DECAY_STEPS = 20

LEARNING_RATE = 1e-3
BATCH_SIZE = 124
MAX_REWARD_NUM = 11
BUFFER_SIZE = 20000  # memory size

# Create environment
# -- DO NOT MODIFY --
env = gym.make(ENV_NAME)
epsilon = INITIAL_EPSILON
STATE_DIM = env.observation_space.shape[0]
ACTION_DIM = env.action_space.n

# Placeholders
# -- DO NOT MODIFY --
state_in = tf.placeholder("float", [None, STATE_DIM])
action_in = tf.placeholder("float", [None, ACTION_DIM])
target_in = tf.placeholder("float", [None])


def network(state):
    return tf.layers.dense(inputs=tf.layers.dense(inputs=state,
                                                  units=64,
                                                  activation=tf.nn.tanh,
                                                  kernel_initializer=tf.random_normal_initializer(),
                                                  use_bias=True),
                           activation=None,
                           units=ACTION_DIM,
                           use_bias=True,
                           kernel_initializer=tf.random_normal_initializer())


# TODO: Define Network Graph


# TODO: Network outputs
q_values = tf.make_template('eval', network)(state_in)
q_action = tf.argmax(q_values)

target_v = tf.make_template('target', network)(state_in)
q_val_sel = tf.reduce_sum(tf.multiply(q_values, action_in), axis=1)

# TODO: Loss/Optimizer Definition
loss = tf.reduce_mean(tf.square(target_in - q_val_sel))
optimizer = tf.train.AdamOptimizer(learning_rate=LEARNING_RATE).minimize(loss)

# Start session - Tensorflow housekeeping
session = tf.InteractiveSession()
session.run(tf.global_variables_initializer())


# -- DO NOT MODIFY ---
def explore(state, epsilon):
    """
    Exploration function: given a state and an epsilon value,
    and assuming the network has already been defined, decide which action to
    take using e-greedy exploration based on the current q-value estimates.
    """
    Q_estimates = q_values.eval(feed_dict={
        state_in: [state]
    })
    if random.random() <= epsilon:
        action = random.randint(0, ACTION_DIM - 1)
    else:
        action = np.argmax(Q_estimates)
    one_hot_action = np.zeros(ACTION_DIM)
    one_hot_action[action] = 1
    return one_hot_action


def stop_train(step, epi, rwd):
    if epi > 100: #max training ep
        return True
    if step < 5000: #max training step
        return False
    if len(rwd) < MAX_REWARD_NUM:
        return False
    if np.mean(rwd) >= 196: #max reward, if bigger, stop training
        return True
    else:
        return False


def next_bat(l, capacity):
    if np.minimum(len(l), capacity) == 0:
        return []
    else:
        return random.sample(l, np.minimum(len(l), capacity))


def set_data(tv, exp):
    ns_qvalues = tv.eval(feed_dict={state_in: [e[2] for e in exp]})
    target = []
    for k in range(len(exp)):
        target_reward = exp[k][1]
        if not exp[k][4]:
            target_reward += GAMMA * np.max(ns_qvalues[k])
        target.append(target_reward)

    return dict({target_in: target,
                 action_in: [e[3] for e in exp],
                 state_in: [e[0] for e in exp]})


def sync():
    return [var_target.assign(var_eval, use_locking=True) for (var_eval, var_target) in
            zip(tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='eval'),
                tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='target'))]


env.seed(0)
random.seed(0)
last_rewards = []
steps = 0
replay_buffer = []
current_pos = 0
train_stop_flag = False
syncV = sync()

# Main learning loop
for episode in range(EPISODE):

    # initialize task
    state = env.reset()

    # Update epsilon once per episode
    if epsilon > FINAL_EPSILON:
        epsilon -= (epsilon - FINAL_EPSILON) / EPSILON_DECAY_STEPS

    # Move through env according to e-greedy policy
    episode_reward = 0
    for step in range(STEP):
        if stop_train(steps, episode, last_rewards):
            break
        action = explore(state, epsilon)
        next_state, reward, done, _ = env.step(np.argmax(action))
        # TODO: Calculate the target q-value.
        # hint1: Bellman
        # hint2: consider if the episode has terminated

        if len(replay_buffer) < BUFFER_SIZE:
            replay_buffer.append([state, reward, next_state, action, done])
        else:
            replay_buffer[current_pos] = [state, reward, next_state, action, done]
            current_pos = (current_pos + 1) % BUFFER_SIZE

        episode_reward += reward
        state = next_state

        if stop_train(steps, episode, last_rewards):
            train_stop_flag = True
        if not train_stop_flag:
            if steps != 0 and steps % 5 == 0:  # set sync period
                session.run([syncV])
            exp_bat = next_bat(replay_buffer, BATCH_SIZE)

            if exp_bat is None or len(exp_bat) == 0:
                pass
            else:
                session.run([optimizer], feed_dict=set_data(target_v, exp_bat))
                steps += 1
                
            if done:
                break
    last_rewards.append(episode_reward)
    if len(last_rewards) >= MAX_REWARD_NUM:
        last_rewards.pop(0)

    # Test and view sample runs - can disable render to save time
    # -- DO NOT MODIFY --
    if (episode % TEST_FREQUENCY == 0 and episode != 0):
        total_reward = 0
        for i in range(TEST):
            state = env.reset()
            for j in range(STEP):
                env.render()
                action = np.argmax(q_values.eval(feed_dict={
                    state_in: [state]
                }))
                state, reward, done, _ = env.step(action)
                total_reward += reward
                if done:
                    break
        ave_reward = total_reward / TEST
        print('episode:', episode, 'epsilon:', epsilon, 'Evaluation '
                                                        'Average Reward:', ave_reward)

env.close()
