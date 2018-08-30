from keras import backend as K
from keras.engine import InputSpec
from keras.layers import LSTM, activations, Wrapper, Recurrent

class Attention(Wrapper):
    """
    ```python
    model = Sequential()
    model.add(LSTM(10, return_sequences=True), batch_input_shape=(4, 5, 10))
    model.add(TFAttentionRNNWrapper(LSTM(10, return_sequences=True, consume_less='gpu')))
    model.add(Dense(5))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')     
    """
    def __init__(self, layer, **kwargs):
        assert isinstance(layer, Recurrent)
        if layer.get_config()['consume_less']=='cpu':
            raise Exception("AttentionLSTMWrapper doesn't support RNN's with consume_less='cpu'")
        self.supports_masking = True
        super(Attention, self).__init__(layer, **kwargs)

    def build(self, input_shape):
        assert len(input_shape) >= 3
        self.input_spec = [InputSpec(shape=input_shape)]
        nb_samples, nb_time, input_dim = input_shape

        if not self.layer.built:
            self.layer.build(input_shape)
            self.layer.built = True

        super(Attention, self).build()
        
        self.W1 = self.layer.init((input_dim, input_dim, 1, 1), name='{}_W1'.format(self.name))
        self.W2 = self.layer.init((self.layer.output_dim, input_dim), name='{}_W2'.format(self.name))
        self.b2 = K.zeros((input_dim,), name='{}_b2'.format(self.name))
        self.W3 = self.layer.init((input_dim*2, input_dim), name='{}_W3'.format(self.name))
        self.b3 = K.zeros((input_dim,), name='{}_b3'.format(self.name))
        self.V = self.layer.init((input_dim,), name='{}_V'.format(self.name))

        self.trainable_weights = [self.W1, self.W2, self.W3, self.V, self.b2, self.b3]

    def get_output_shape_for(self, input_shape):
        return self.layer.get_output_shape_for(input_shape)

    def step(self, x, states):
        # This is based on [tensorflows implementation](https://github.com/tensorflow/tensorflow/blob/c8a45a8e236776bed1d14fd71f3b6755bd63cc58/tensorflow/python/ops/seq2seq.py#L506).
        # First, we calculate new attention masks:
        #   attn = softmax(V^T * tanh(W2 * X +b2 + W1 * h))
        # and we make the input as a concatenation of the input and weighted inputs which is then
        # transformed back to the shape x of using W3
        #   x = W3*(x+X*attn)+b3
        # Then, we run the cell on a combination of the input and previous attention masks:
        #   h, state = cell(x, h).
        
        nb_samples, nb_time, input_dim = self.input_spec[0].shape
        h = states[0]
        X = states[-1]
        xW1 = states[-2]
        
        Xr = K.reshape(X,(-1,nb_time,1,input_dim))
        hW2 = K.dot(h,self.W2)+self.b2
        hW2 = K.reshape(hW2,(-1,1,1,input_dim)) 
        u = K.tanh(xW1+hW2)
        a = K.sum(self.V*u,[2,3])
        a = K.softmax(a)
        a = K.reshape(a,(-1, nb_time, 1, 1))
        
        # Weight attention vector by attention
        Xa = K.sum(a*Xr,[1,2])
        Xa = K.reshape(Xa,(-1,input_dim))
        
        # Merge input and attention weighted inputs into one vector of the right size.
        x = K.dot(K.concatenate([x,Xa],1),self.W3)+self.b3    
        
        h, new_states = self.layer.step(x, states)
        return h, new_states

    def get_constants(self, x):
        constants = self.layer.get_constants(x)
        
        # Calculate K.dot(x, W2) only once per sequence by making it a constant
        nb_samples, nb_time, input_dim = self.input_spec[0].shape
        Xr = K.reshape(x,(-1,nb_time,input_dim,1))
        Xrt = K.permute_dimensions(Xr, (0, 2, 1, 3))
        xW1t = K.conv2d(Xrt,self.W1,border_mode='same')     
        xW1 = K.permute_dimensions(xW1t, (0, 2, 3, 1))
        constants.append(xW1)
        
        # we need to supply the full sequence of inputs to step (as the attention_vector)
        constants.append(x)
        
        return constants

    def call(self, x, mask=None):
        # input shape: (nb_samples, time (padded with zeros), input_dim)
        input_shape = self.input_spec[0].shape
        if K._BACKEND == 'tensorflow':
            if not input_shape[1]:
                raise Exception('When using TensorFlow, you should define '
                                'explicitly the number of timesteps of '
                                'your sequences.\n'
                                'If your first layer is an Embedding, '
                                'make sure to pass it an "input_length" '
                                'argument. Otherwise, make sure '
                                'the first layer has '
                                'an "input_shape" or "batch_input_shape" '
                                'argument, including the time axis. '
                                'Found input shape at layer ' + self.name +
                                ': ' + str(input_shape))

        if self.layer.stateful:
            initial_states = self.layer.states
        else:
            initial_states = self.layer.get_initial_states(x)
        constants = self.get_constants(x)
        preprocessed_input = self.layer.preprocess_input(x)
        

        last_output, outputs, states = K.rnn(self.step, preprocessed_input,
                                             initial_states,
                                             go_backwards=self.layer.go_backwards,
                                             mask=mask,
                                             constants=constants,
                                             unroll=self.layer.unroll,
                                             input_length=input_shape[1])
        if self.layer.stateful:
            self.updates = []
            for i in range(len(states)):
                self.updates.append((self.layer.states[i], states[i]))

        if self.layer.return_sequences:
            return outputs
        else:
            return last_output