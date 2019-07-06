# https://www.cse.unsw.edu.au/~cs9444/18s2/hw2/index.html
import tensorflow as tf

BATCH_SIZE = 128
MAX_WORDS_IN_REVIEW = 200  # Maximum length of a review to consider
EMBEDDING_SIZE = 50  # Dimensions for each word vector

vocab_num = 10000
hidden_dim = 128
learning_rate = 0.001

stop_words = set({'ourselves', 'hers', 'between', 'yourself', 'again',
                  'there', 'about', 'once', 'during', 'out', 'very', 'having',
                  'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its',
                  'yours', 'such', 'into', 'of', 'most', 'itself', 'other',
                  'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him',
                  'each', 'the', 'themselves', 'below', 'are', 'we',
                  'these', 'your', 'his', 'through', 'don', 'me', 'were',
                  'her', 'more', 'himself', 'this', 'down', 'should', 'our',
                  'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had',
                  'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them',
                  'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does',
                  'yourselves', 'then', 'that', 'because', 'what', 'over',
                  'why', 'so', 'can', 'did','not', 'now', 'under', 'he', 'you',
                  'herself', 'has', 'just', 'where', 'too', 'only', 'myself',
                  'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being',
                  'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it',
                  'how', 'further', 'was', 'here', 'than'})

intab = r",./<>?;':|}{][~`!@#\"$%^&*()=_+0123456789"
outtab = "                                         "
transtab = str.maketrans(intab, outtab)
stopn = set([e+'n' for e in stop_words])
def preprocess(review):
    """
    Apply preprocessing to a single review. You can do anything here that is manipulation
    at a string level, e.g.
        - removing stop words
        - stripping/adding punctuation
        - changing case
        - word find/replace
    RETURN: the preprocessed review in string form.
    """
    # TODO: here just remove stop words
    processed_review = [w for w in \
                        review.replace(r"<br />", "") \
                        .translate(transtab).lower().split() \
                        if len(w) > 2 and w not in stop_words and w not in stopn]

    return processed_review


def attention_layer(inputs, seq_len, hidden_dim, attention_dim):
    """
    generate attention output
    """
    with tf.variable_scope("attention"):
        U = tf.Variable(tf.random_uniform([hidden_dim, attention_dim], -0.1, 0.1), name='attention_u')
        V = tf.Variable(tf.random_uniform([attention_dim], -0.1, 0.1), name='attention_v')
        fw = inputs[0]
        bw = inputs[1]
        print('fw={}, \nbw={}'.format(fw, bw))
        fw_probs = alpha(fw, hidden_dim, U, V, seq_len)
        bw_probs = alpha(bw, hidden_dim, U, V, seq_len)
        fw = tf.reduce_sum(fw * tf.expand_dims(fw_probs, -1), 1)
        bw = tf.reduce_sum(bw * tf.expand_dims(bw_probs, -1), 1)
        print('fw={}, \nbw={}'.format(fw, bw))

        output = tf.concat([fw, bw], 1)
    return output


def alpha(inputs, n_hidden, U, V, seq_len):
    """
    e_i=v^T * tanh(U * h_i)
    alpha=exp(e_i) / sum_k(exp(e_k))
    """
    flat = tf.reshape(inputs, [-1, n_hidden])
    flat = tf.tanh(tf.matmul(flat, U))
    flat = flat * V
    flat = tf.reduce_sum(flat, 1)
    flat = tf.reshape(flat, [-1, seq_len])
    exp = tf.exp(flat)
    exp_sum = tf.reduce_sum(exp, 1, keep_dims=True)
    probs = exp / exp_sum
    return probs


def define_graph():
    """
    Implement your model here. You will need to define placeholders, for the input and labels,
    Note that the input is not strings of words, but the strings after the embedding lookup
    has been applied (i.e. arrays of floats).

    In all cases this code will be called by an unaltered runner.py. You should read this
    file and ensure your code here is compatible.

    Consult the assignment specification for details of which parts of the TF API are
    permitted for use in this function.

    You must return, in the following order, the placeholders/tensors for;
    RETURNS: input, labels, optimizer, accuracy and loss
    """
    input_data = tf.placeholder(
        tf.float32, [None, MAX_WORDS_IN_REVIEW, EMBEDDING_SIZE], name='input_data')
    labels = tf.placeholder(tf.float32, [None, 2], name='labels')
    dropout_keep_prob = tf.placeholder_with_default(1.0,[], name='keep_prob')

    # with tf.device('/cpu:0'), tf.name_scope('embedding'):
    #     emb_W = tf.Variable(tf.random_uniform([vocab_num, EMBEDDING_SIZE], 0., 1.), name='emb_W')
    #     embedding = tf.nn.embedding_lookup(emb_W, input_data)

    """
    TODO:
    current model is BiLSTM + FC + softmax (sentence representation is the last hidden state)

    """

    with tf.variable_scope('bilstm'):
        rnn_cell_fw = tf.contrib.rnn.BasicLSTMCell(hidden_dim)
        rnn_cell_fw = tf.contrib.rnn.DropoutWrapper(rnn_cell_fw, output_keep_prob=dropout_keep_prob)
        rnn_cell_bw = tf.contrib.rnn.BasicLSTMCell(hidden_dim)
        rnn_cell_bw = tf.contrib.rnn.DropoutWrapper(rnn_cell_bw, output_keep_prob=dropout_keep_prob)

        outputs, states = tf.nn.bidirectional_dynamic_rnn(
            cell_fw=rnn_cell_fw, cell_bw=rnn_cell_bw,
            inputs=input_data, dtype=tf.float32)

        print(outputs)

        states = attention_layer(
            outputs, MAX_WORDS_IN_REVIEW, hidden_dim, hidden_dim)
        # fw_state = tf.concat(states[0], 1)
        # bw_state = tf.concat(states[1], 1)
        # states = tf.concat([fw_state, bw_state], axis=1)

        print('output ={}, \nstates={}'.format(outputs, states))

    with tf.name_scope('softmax'):
        pro_weights = tf.Variable(tf.truncated_normal([hidden_dim * 2,2],stddev = 0.2),
                                  name='pro_weights')
        pro_biases = tf.Variable(tf.constant(0.0,shape=[2]), name='pro_biases')

        logits = tf.nn.dropout(tf.nn.xw_plus_b(states, pro_weights, pro_biases), keep_prob=dropout_keep_prob)
        prob = tf.nn.softmax(logits)
        print('state={}, \nprob={}'.format(states, prob))

    prob_loss = tf.multiply(labels, tf.log(tf.clip_by_value(prob, 1e-30, 1.0)))
    l2_penalty_beta = 1e-4
    vars = tf.trainable_variables()
    l2_penalty = l2_penalty_beta * tf.add_n(
        [tf.nn.l2_loss(v) for v in vars if 'bias' not in v.name.lower()])

    loss = tf.reduce_mean(-prob_loss + l2_penalty, name='prob_loss')

    print('loss={}'.format(loss))
    prediction = tf.argmax(prob, 1, name="prediction")
    correct_prediction = tf.equal(prediction, tf.argmax(labels, 1))
    correct_num = tf.reduce_sum(tf.cast(correct_prediction, tf.float32))
    Accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="accuracy")
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(loss)
    return input_data, labels, dropout_keep_prob, optimizer, Accuracy, loss


if __name__ == "__main__":
    define_graph()
