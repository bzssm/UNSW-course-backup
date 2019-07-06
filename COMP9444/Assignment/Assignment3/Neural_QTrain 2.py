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
GAMMA = 0.9 # discount factor
INITIAL_EPSILON =  0.8 # starting value of epsilon
FINAL_EPSILON =  0.01 # final value of epsilon
EPSILON_DECAY_STEPS =  100 # decay period
BATCH_SIZE = 256
BUFFER_SIZE = 5000
replay_buffer = []  # use to store experience pairs


# Create environment
# -- DO NOT MODIFY --
env = gym.make(ENV_NAME)
epsilon = INITIAL_EPSILON
STATE_DIM = env.observation_space.shape[0]
ACTION_DIM = env.action_space.n
print('state dim={}, action_dim={}'.format(STATE_DIM, ACTION_DIM))

# Placeholders
# -- DO NOT MODIFY --
state_in = tf.placeholder("float", [None, STATE_DIM])
action_in = tf.placeholder("float", [None, ACTION_DIM])
target_in = tf.placeholder("float", [None])

# TODO: Define Network Graph
# w_initializer = tf.random_normal_initializer(0., 0.3)
# b_initializer = tf.constant_initializer(0.1)
# print(w_initializer, b_initializer)


# build network: here we only use two layer MLP
fc_0 = tf.layers.dense(state_in, 256, tf.nn.tanh, name='fc_0')
fc_1 = tf.layers.dense(fc_0, 128, tf.nn.tanh, name='fc_1')

# TODO: Network outputs
q_values = tf.layers.dense(fc_1, ACTION_DIM, name='q')
# q_action = tf.reduce_max(q_values, axis=1)
q_action = tf.reduce_sum(tf.multiply(q_values, action_in), reduction_indices=1)
print('q_values={}, q_action={}'.format(q_values, q_action))

# TODO: Loss/Optimizer Definition
loss =  tf.reduce_mean(tf.squared_difference(q_action, target_in))
optimizer = tf.train.AdamOptimizer(0.001).minimize(loss)    # fixed learning rate to 0.01

# Start session - Tensorflow housekeeping
session = tf.InteractiveSession()
session.run(tf.global_variables_initializer())




def store_experience(state, action, reward):
    replay_buffer.append([state, action, reward])
    if len(replay_buffer) > BUFFER_SIZE:
        replay_buffer.pop(0)

    # print('buffer_sise={}'.format(len(replay_buffer)))



def update_nn(batch_data):
    batch_data = np.array(batch_data)
    target = batch_data[:,2]
    action = [list(a) for a in batch_data[:,1]]
    state = [list(s) for s in batch_data[:,0]]

    session.run([optimizer], feed_dict={
            target_in: target,
            action_in: action,
            state_in: state
        })



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


# Main learning loop
for episode in range(EPISODE):

    # initialize task
    state = env.reset()

    # Update epsilon once per episode
    epsilon -= (epsilon-FINAL_EPSILON) / EPSILON_DECAY_STEPS
    
    episode_reward = 0
    # Move through env according to e-greedy policy
    for step in range(STEP):
        action = explore(state, epsilon)
        next_state, reward, done, _ = env.step(np.argmax(action))

        nextstate_q_values = q_values.eval(feed_dict={
            state_in: [next_state]
        })

        # TODO: Calculate the target q-value.
        # hint1: Bellman
        # hint2: consider if the episode has terminated
        # print('next_q_values={}'.format(nextstate_q_values))
        target = reward if done else reward + GAMMA * max(nextstate_q_values[0])
        # print('state={}, action={}, target={}'.format(state, action, target))
        episode_reward += reward

        # store experience
        store_experience(state, action, target)

        # Do one training step
        # session.run([optimizer], feed_dict={
        #     target_in: [target],
        #     action_in: [action],
        #     state_in: [state]
        # })

        if len(replay_buffer) > BATCH_SIZE:
            # print('buffer size={}'.format(len(replay_buffer)))
            batch_data = random.sample(replay_buffer, BATCH_SIZE)
            update_nn(batch_data)
        # else:
        #     batch_data = random.sample(replay_buffer, len(replay_buffer))
        #     update_nn(batch_data)

        # Update
        state = next_state
        if done:
            break

    print('>>> train, epoch {}, reward={}'.format(episode, episode_reward))

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
