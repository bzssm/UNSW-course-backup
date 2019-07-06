import gym
import tensorflow as tf
import numpy as np
import random

tf.reset_default_graph()
# General Parameters
# -- DO NOT MODIFY --
ENV_NAME = 'CartPole-v0'
EPISODE = 200000  # Episode limitation
STEP = 200  # Step limitation in an episode
TEST = 10  # The number of tests to run every TEST_FREQUENCY episodes
TEST_FREQUENCY = 100  # Num episodes to run before visualizing test accuracy

# TODO: HyperParameters
GAMMA =  0.98# discount factor
INITIAL_EPSILON =  1.0# starting value of epsilon
FINAL_EPSILON =  0.001# final value of epsilon
EPSILON_DECAY_STEPS =  20# decay period

SYNC_PERIOD = 5
LEARNING_RATE = 1e-3
UPDATE_RATE=1
BATCH_SIZE = 124
MAX_TRAIN_EPISODE = 100 #max train num
MIN_TRAIN_STEPS = 5000 #min train num
QUIT_REWARDS_THRESHOLD=196#
MAX_REWARD_NUM=11 # maximum mean reward num
MEMORY_SIZE=20000#memory size

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

def network_template(state):
    layer1 = tf.layers.dense(inputs=state,
                             units=64,
                             activation=tf.nn.tanh,
                            kernel_initializer=tf.random_normal_initializer(),
                             use_bias=True,
                             name='layer1')
    output = tf.layers.dense(inputs=layer1,
                              activation=None,
                              units=ACTION_DIM,
                              use_bias=True,
                              kernel_initializer=tf.random_normal_initializer(),
                              name='out')

    return output

def stop_train(last_rewards, episode):
    if episode > MAX_TRAIN_EPISODE:
        return True
    # At least the number of training required
    if nb_of_training_steps < MIN_TRAIN_STEPS:
        return False
    # if latest_reward is not bigger than max_reward_num
    if len(last_rewards) < MAX_REWARD_NUM:
        return False

    mean_rewards = np.mean(last_rewards)
    if mean_rewards >= QUIT_REWARDS_THRESHOLD:
        return True
    else:
        return False

def get_variables(name_scope):
    trainable_vars = tf.get_collection(
        tf.GraphKeys.TRAINABLE_VARIABLES, scope=name_scope)
    return trainable_vars

def sync_op():
    vars_in_eval_qnet = get_variables('eval')
    vars_in_target_qnet = get_variables('target')
    sync_ops = []
    for (var_eval, var_target) in zip(vars_in_eval_qnet, vars_in_target_qnet):
        sync_ops.append(
            var_target.assign(var_eval * UPDATE_RATE + var_target * (1 - UPDATE_RATE), use_locking=True))
    return sync_ops

def build_feed_data(minibatch_exp):
    state = [elem[0] for elem in minibatch_exp]
    next_state = [elem[2] for elem in minibatch_exp]
    action = [elem[3] for elem in minibatch_exp]
    ns_qvalues = target_qvalue.eval(feed_dict={state_in: next_state})
        # this step is to calculate target value each state.
    target = []

    for i in range(len(minibatch_exp)):
        target_reward = minibatch_exp[i][1]
            # print( target_reward)
        done = minibatch_exp[i][4]
            # print(done)
        if not done:
            target_reward += GAMMA * np.max(ns_qvalues[i])
        target.append(target_reward)

    return dict(
        {target_in: target, action_in: action, state_in: state})
# TODO: Define Network Graph


# TODO: Network outputs
q_values =tf.make_template('eval', network_template)(state_in)
q_action =tf.argmax(q_values)
target_qvalue = tf.make_template('target', network_template)(state_in)

# TODO: Loss/Optimizer Definition
q_val_sel = tf.reduce_sum(tf.multiply(tf.make_template('eval', network_template)(state_in), action_in), axis=1)
target = tf.make_template('target', network_template)(state_in)
loss = tf.reduce_mean(tf.square(target_in - q_val_sel))

optimizer =tf.train.AdamOptimizer(learning_rate=LEARNING_RATE).minimize(loss)

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


random.seed(0)
env.seed(0)
nb_of_training_steps =0
last_rewards = []
replay_buffer=[]
current_location = 0
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
        if stop_train(last_rewards, episode) == True:
            break
        action = explore(state, epsilon)
        next_state, reward, done, _ = env.step(np.argmax(action))

        # nextstate_q_values = q_values.eval(feed_dict={
        #     state_in: [next_state]
        # })

        # TODO: Calculate the target q-value.
        # hint1: Bellman
        # hint2: consider if the episode has terminated
        #agent.remember([state, reward, next_state, action, done])
        if len(replay_buffer) < MEMORY_SIZE:
            replay_buffer.append([state, reward, next_state, action, done])
        else:
            replay_buffer[current_location] = [state, reward, next_state, action, done]
            current_location = (current_location + 1) % MEMORY_SIZE

        episode_reward += reward
        state = next_state

        # agent.train(episode)
        train_stop = False
        if train_stop == False and stop_train(last_rewards, episode) == False:
            # self.sync_networks()
            if nb_of_training_steps != 0 and nb_of_training_steps % SYNC_PERIOD == 0:
                session.run([sync_op()])
            # minibatch_exp = self.replay_buffer.next_minibatch(self.params['minibatch_size'])
            n_size = np.minimum(len(replay_buffer), BATCH_SIZE)
            if n_size == 0:
                minibatch_exp=[]
            else:
                minibatch_exp= random.sample(replay_buffer, n_size)
            # if None == minibatch_exp or len(minibatch_exp) == 0:
            #     return
            # else:
            #     pass

            # session.run([self.double_q_nets.get_optimizer()], feed_dict=feed_data)
            if minibatch_exp != None and len(minibatch_exp)!=0:
                # feed_data = self.build_feed_data(minibatch_exp)
                feed_data = build_feed_data(minibatch_exp)
                session.run([optimizer], feed_dict=feed_data)
                nb_of_training_steps += 1

        if done:
            break

        # target =

        # Do one training step
        # session.run([optimizer], feed_dict={
        #     target_in: [target],
        #     action_in: [action],
        #     state_in: [state]
        # })

        # Update
        state = next_state
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
