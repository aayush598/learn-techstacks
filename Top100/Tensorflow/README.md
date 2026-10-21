# TensorFlow / Keras Interview Questions and Answers

## Q1: What is TensorFlow?
**A:** TensorFlow is an open-source machine learning framework developed by Google for building, training, and deploying ML models. It supports deep learning, numerical computation using data flow graphs, and runs on CPU, GPU, and TPU. TensorFlow provides both high-level APIs (Keras) and low-level operations for maximum flexibility.
**Code:**
```python
import tensorflow as tf
print(tf.__version__)             # e.g. 2.16.1
print(tf.executing_eagerly())     # True in TF 2.x
a = tf.constant([[1., 2.], [3., 4.]])
b = tf.linalg.matmul(a, a)
print(b.numpy())
```

## Q2: What is Keras and how does it relate to TensorFlow?
**A:** Keras is a high-level neural networks API that provides a user-friendly interface for building and training models. Since TensorFlow 2.0, Keras is the official high-level API (`tf.keras`). It offers: Sequential API (linear stack of layers), Functional API (complex topologies), and Model subclassing (custom logic).
**Code:**
```python
import tensorflow as tf
model = tf.keras.Sequential([
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(1),
])
inputs = tf.keras.Input(shape=(4,))
x = tf.keras.layers.Dense(8, activation='relu')(inputs)
outputs = tf.keras.layers.Dense(1)(x)
func_model = tf.keras.Model(inputs=inputs, outputs=outputs)
print(model(tf.random.normal((2, 4))).shape)       # (2, 1)
print(func_model(tf.random.normal((2, 4))).shape)  # (2, 1)
```

## Q3: What is a Tensor in TensorFlow?
**A:** A tensor is a multi-dimensional array — the fundamental data unit in TensorFlow. Rank 0 (scalar), Rank 1 (vector), Rank 2 (matrix), Rank 3+ (higher-dimensional). Tensors have: `dtype` (data type like float32, int32), `shape` (size of each dimension), and `device` (where allocated). Unlike NumPy arrays, tensors can run on GPUs and are immutable.
**Code:**
```python
import tensorflow as tf
scalar = tf.constant(3.14)               # rank 0
vector = tf.constant([1, 2, 3])          # rank 1
matrix = tf.constant([[1, 2], [3, 4]])   # rank 2
tensor = tf.ones((2, 3, 4))              # rank 3
print(scalar.ndim, scalar.dtype, scalar.shape)
print(tf.reduce_sum(matrix).numpy())     # 10
print(tensor.shape, tensor.device)
```

## Q4: What is eager execution in TensorFlow?
**A:** Eager execution (default in TF 2.x) evaluates operations immediately when called, returning concrete values without building a computational graph first. This makes debugging easier and code more pythonic. You can mix eager execution with `tf.function` for performance — use `@tf.function` decorator to compile functions into graphs.
**Code:**
```python
import tensorflow as tf
print(tf.executing_eagerly())            # True (default in TF 2.x)
x = tf.constant([1., 2., 3.])
y = x * 2                                # executed immediately
print(y.numpy())                         # [2. 4. 6.]

@tf.function                             # graph execution for performance
def double(x):
    return x * 2
print(double(x).numpy())                 # [2. 4. 6.]
```

## Q5: What is `tf.function` and how does it work?
**A:** `@tf.function` decorator compiles a Python function into a TensorFlow graph for performance optimization. On first call, it traces the function and creates a graph. Subsequent calls execute the cached graph. Benefits: graph optimizations (constant folding, op fusion), XLA compilation, and execution on accelerators. Not all Python code is supported — only TF operations.
**Code:**
```python
import tensorflow as tf

@tf.function
def add(a, b):
    return a + b

print(add(tf.constant(1.), tf.constant(2.)))   # traces + runs -> 3.
print(add(tf.constant(30.), tf.constant(12.)).numpy())  # cached graph: 42.
concrete = add.get_concrete_function(
    tf.TensorSpec(shape=(None,), dtype=tf.float32))
print(concrete(tf.constant([1., 2., 3.])).numpy())
```

## Q6: What is the difference between `tf.constant`, `tf.Variable`, and `tf.Tensor`?
**A:** `tf.Tensor` is the base type — immutable, created from operations. `tf.constant` is a tensor with a fixed value, immutable, and can be stored in the graph definition. `tf.Variable` is mutable — used for model parameters (weights, biases). Variables must be explicitly initialized and their values persist across `tf.function` calls.
**Code:**
```python
import tensorflow as tf
t = tf.add(tf.constant(1.), tf.constant(2.))  # tf.Tensor, immutable
c = tf.constant([1., 2., 3.])                 # fixed value, immutable
v = tf.Variable([0., 0., 0.])                 # mutable, holds model weights
v.assign_add([1., 1., 1.])                    # v.assign(...) works
print(t.numpy(), c.numpy(), v.numpy())
# c.assign(...) -> AttributeError: constants are immutable
```

## Q7: How do you create a simple neural network with Keras Sequential API?
**A:** ```python
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=10, batch_size=32, validation_split=0.2)
```
**Code:**
```python
import tensorflow as tf
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax'),
])
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.summary()
```

## Q8: What is the Functional API in Keras?
**A:** The Functional API allows building complex models with non-linear topologies: multi-input, multi-output, shared layers, and residual connections. Instead of stacking layers sequentially, you define layers as callable functions: `x = Dense(64, activation='relu')(input)`. Useful for branch networks, siamese networks, and models with skip connections.
**Code:**
```python
import tensorflow as tf
inputs = tf.keras.Input(shape=(32,))
x = tf.keras.layers.Dense(64, activation='relu')(inputs)
skip = tf.keras.layers.Dense(32)(inputs)                  # branch
x = tf.keras.layers.Concatenate()([x, skip])              # merge branches
outputs = tf.keras.layers.Dense(10, activation='softmax')(x)
model = tf.keras.Model(inputs=inputs, outputs=outputs)
model.summary()
```

## Q9: What is Model subclassing in Keras?
**A:** Model subclassing involves extending `tf.keras.Model` and implementing the `call()` method. Gives full control over forward pass logic, including loops, conditionals, and custom operations. Example: `class MyModel(tf.keras.Model): def __init__(self): super().__init__(); self.dense = Dense(10); def call(self, x): return self.dense(x)`.
**Code:**
```python
import tensorflow as tf

class MyModel(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.dense1 = tf.keras.layers.Dense(32, activation='relu')
        self.dense2 = tf.keras.layers.Dense(10, activation='softmax')
    def call(self, x):
        return self.dense2(self.dense1(x))

model = MyModel()
print(model(tf.random.normal((4, 16))).shape)   # (4, 10)
```

## Q10: What are the advantages and disadvantages of each Keras API?
**A:** Sequential: simplest, good for linear stacks, limited flexibility. Functional: moderate complexity, supports branching/sharing, good for most projects. Subclassing: most flexible, supports custom logic, harder to debug, not serializable by default. Recommendation: use Sequential for simple models, Functional for multi-branch, subclass for research.
**Code:**
```python
import tensorflow as tf
# Sequential: linear stack of layers
seq = tf.keras.Sequential([tf.keras.layers.Dense(10, activation='relu'),
                           tf.keras.layers.Dense(1)])
# Functional: graph topologies (shared/branching layers)
inp = tf.keras.Input(shape=(4,))
out = tf.keras.layers.Dense(10, activation='relu')(inp)
func = tf.keras.Model(inputs=inp, outputs=tf.keras.layers.Dense(1)(out))
# Subclassing: full Pythonic control
class Sub(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.d = tf.keras.layers.Dense(1)
    def call(self, x):
        return self.d(x)
sub = Sub()
x = tf.random.normal((2, 4))
print(func(x).shape, sub(x).shape)   # (2, 1) (2, 1)
```

## Q11: What is the `compile` step in Keras?
**A:** `model.compile()` configures the model for training. Parameters: `optimizer` (adam, sgd, rmsprop), `loss` (mse, categorical_crossentropy, binary_crossentropy), `metrics` (accuracy, precision, recall, AUC). This is where you define the learning process before calling `fit()`. You can also compile with custom losses and metrics.
**Code:**
```python
import tensorflow as tf
model = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=(2,))])
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='mean_squared_error',
    metrics=['mae'],
)
x = tf.constant([[1., 2.], [3., 4.], [5., 6.]])
y = tf.constant([3., 7., 11.])
model.fit(x, y, epochs=2, verbose=0)
```

## Q12: What optimizers are available in TensorFlow?
**A:** Common optimizers: `SGD` (with/without momentum), `Adam` (adaptive moment estimation, generally recommended), `RMSprop`, `Adagrad`, `Adadelta`, `AdamW` (Adam with weight decay), `Nadam` (Adam with Nesterov). Adam is the default choice for most deep learning tasks due to adaptive learning rates and good convergence.
**Code:**
```python
import tensorflow as tf
opts = [
    tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9),
    tf.keras.optimizers.Adam(learning_rate=0.001),
    tf.keras.optimizers.RMSprop(learning_rate=0.001),
    tf.keras.optimizers.Adagrad(learning_rate=0.01),
    tf.keras.optimizers.AdamW(learning_rate=0.001, weight_decay=1e-4),
]
model = tf.keras.Sequential([tf.keras.layers.Dense(1)])
for opt in opts:
    model.compile(optimizer=opt, loss='mse')
print(model.optimizer.__class__.__name__)   # AdamW (last one compiled)
```

## Q13: What is the difference between `SGD` and `Adam`?
**A:** SGD (Stochastic Gradient Descent) uses a single learning rate, requires manual scheduling, can get stuck in local minima, but generalizes better in some cases. Adam uses adaptive learning rates per parameter, momentum, bias correction, converges faster, and requires less tuning. Adam is safer for starting projects; SGD + momentum with LR scheduling may give better final performance.
**Code:**
```python
import tensorflow as tf
x = tf.random.normal((200, 8))
y = tf.random.normal((200, 1))

def build(opt):
    m = tf.keras.Sequential([tf.keras.layers.Dense(16, activation='relu'),
                             tf.keras.layers.Dense(1)])
    m.compile(optimizer=opt, loss='mse')
    return m

sgd = build(tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9))
adam = build(tf.keras.optimizers.Adam(learning_rate=0.001))
sgd.fit(x, y, epochs=3, verbose=0)
adam.fit(x, y, epochs=3, verbose=0)
```

## Q14: What loss functions does Keras provide?
**A:** Regression: `MeanSquaredError` (MSE), `MeanAbsoluteError` (MAE), `Huber` (robust to outliers). Classification: `CategoricalCrossentropy` (multi-class, one-hot labels), `SparseCategoricalCrossentropy` (multi-class, integer labels), `BinaryCrossentropy` (binary). Others: `KLDivergence`, `CosineSimilarity`, `Hinge`, `Poisson`.
**Code:**
```python
import tensorflow as tf
mse = tf.keras.losses.MeanSquaredError()
mae = tf.keras.losses.MeanAbsoluteError()
huber = tf.keras.losses.Huber(delta=1.0)
y_true = tf.constant([1.0, 2.0, 3.0])
y_pred = tf.constant([1.5, 2.5, 2.0])
print(mse(y_true, y_pred).numpy())

scc = tf.keras.losses.SparseCategoricalCrossentropy()
print(scc(tf.constant([1]), tf.constant([[0.2, 0.7, 0.1]])).numpy())

bce = tf.keras.losses.BinaryCrossentropy()
print(bce(tf.constant([1.]), tf.constant([0.8])).numpy())
```

## Q15: What is the difference between `categorical_crossentropy` and `sparse_categorical_crossentropy`?
**A:** `categorical_crossentropy` expects labels as one-hot encoded vectors (e.g., [0, 1, 0]). `sparse_categorical_crossentropy` expects labels as integers (e.g., 1) and computes the same loss without requiring one-hot encoding. Sparse version is more memory efficient for large numbers of classes.
**Code:**
```python
import tensorflow as tf
cce = tf.keras.losses.CategoricalCrossentropy()
scc = tf.keras.losses.SparseCategoricalCrossentropy()
y_int = tf.constant([1, 0, 1, 2])
y_onehot = tf.one_hot(y_int, depth=3)          # [[0,1,0], ...]
pred = tf.nn.softmax(tf.random.normal((4, 3)))
print(cce(y_onehot, pred).numpy())             # same value:
print(scc(y_int, pred).numpy())                # identical loss, int labels
```

## Q16: What is the `fit()` method and what are its key parameters?
**A:** `model.fit()` trains the model. Key params: `x` (training data), `y` (labels), `batch_size` (samples per gradient update), `epochs` (passes over data), `validation_data`/`validation_split` (eval set), `callbacks` (list of callback objects), `shuffle` (shuffle per epoch), `class_weight` (handle imbalance), `verbose` (0/1/2).
**Code:**
```python
import tensorflow as tf
import numpy as np
x = np.random.randn(200, 8).astype('float32')
y = np.random.randn(200, 1).astype('float32')
model = tf.keras.Sequential([tf.keras.layers.Dense(1)])
model.compile(optimizer='adam', loss='mse')
history = model.fit(
    x, y,
    batch_size=32,
    epochs=3,
    validation_split=0.2,
    shuffle=True,
    verbose=0,
)
print(list(history.history.keys()))   # ['loss', 'val_loss']
```

## Q17: What is the difference between an epoch, batch, and iteration?
**A:** Epoch: one complete pass through the entire training dataset. Batch: a subset of training samples processed before updating weights. Iteration: one batch processed (number of iterations per epoch = total samples / batch size). Example: 1000 samples, batch size 100 = 10 iterations per epoch.
**Code:**
```python
total_samples = 1000
batch_size = 100
iterations_per_epoch = total_samples // batch_size    # 10
print(f'{iterations_per_epoch} iterations per epoch')
epochs = 5
print(f'{iterations_per_epoch * epochs} gradient updates total')
```

## Q18: What is a callback in Keras?
**A:** Callbacks are objects that perform actions at various stages of training (start/end of epoch, batch, training). Built-in: `ModelCheckpoint` (save weights), `EarlyStopping` (stop when metric stops improving), `ReduceLROnPlateau` (reduce LR on plateau), `TensorBoard` (logging), `CSVLogger`, `LearningRateScheduler`. Custom callbacks can extend `tf.keras.callbacks.Callback`.
**Code:**
```python
import tensorflow as tf
x = tf.random.normal((200, 8)); y = tf.random.normal((200, 1))
model = tf.keras.Sequential([tf.keras.layers.Dense(64, activation='relu'),
                             tf.keras.layers.Dense(1)])
model.compile(optimizer='adam', loss='mse')
callbacks = [
    tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5,
                                     restore_best_weights=True),
    tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5,
                                         patience=3),
    tf.keras.callbacks.ModelCheckpoint('checkpoint.keras',
                                       save_best_only=True),
]
model.fit(x, y, epochs=100, validation_split=0.2,
          callbacks=callbacks, verbose=0)
```

## Q19: What is EarlyStopping and how do you configure it?
**A:** `EarlyStopping` stops training when a monitored metric stops improving. Params: `monitor` (e.g., 'val_loss'), `patience` (epochs with no improvement before stopping), `min_delta` (minimum change considered improvement), `restore_best_weights` (revert to best epoch), `mode` ('auto', 'min', 'max'). Prevents overfitting and saves time.
**Code:**
```python
import tensorflow as tf
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',          # metric to watch
    patience=5,                  # epochs without improvement before stopping
    min_delta=1e-3,              # min change counted as improvement
    restore_best_weights=True,
    mode='min',                  # lower val_loss is better
)
model = tf.keras.Sequential([tf.keras.layers.Dense(1)])
model.compile(optimizer='adam', loss='mse')
x = tf.random.normal((100, 4)); y = tf.random.normal((100, 1))
model.fit(x, y, epochs=100, validation_split=0.2,
          callbacks=[early_stop], verbose=0)
```

## Q20: What is ModelCheckpoint?
**A:** `ModelCheckpoint` saves model weights during training. Params: `filepath` (path to save), `monitor` (metric to track), `save_best_only` (only save when metric improves), `save_weights_only` (vs. full model), `mode` ('min'/'max'). Ensures you don't lose progress and can recover the best model.
**Code:**
```python
import tensorflow as tf
checkpoint = tf.keras.callbacks.ModelCheckpoint(
    filepath='best_model.keras',
    monitor='val_loss',
    save_best_only=True,       # overwrite only when val_loss improves
    save_weights_only=False,   # full model incl. optimizer state
    mode='min',
)
model = tf.keras.Sequential([tf.keras.layers.Dense(1)])
model.compile(optimizer='adam', loss='mse')
x = tf.random.normal((100, 4)); y = tf.random.normal((100, 1))
model.fit(x, y, epochs=5, validation_split=0.2,
          callbacks=[checkpoint], verbose=0)
```

## Q21: What is the difference between model.save() and model.save_weights()?
**A:** `model.save()` saves the entire model: architecture, weights, training config, optimizer state. Creates a SavedModel directory (or .h5 file). `model.save_weights()` saves only the weight values (smaller file). To reconstruct a model from weights, you need the architecture code or a separate config. Full save is preferred for deployment.
**Code:**
```python
import tensorflow as tf
model = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=(4,))])
model.compile(optimizer='adam', loss='mse')
model.save('full_model.keras')           # arch + weights + optimizer state
model.save_weights('only_weights.ckpt')  # just weight values

restored = tf.keras.models.load_model('full_model.keras')   # one call

rebuilt = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=(4,))])
rebuilt.load_weights('only_weights.ckpt')                     # arch required first
print(restored.predict(tf.random.normal((2, 4)), verbose=0).shape)
```

## Q22: What is the SavedModel format?
**A:** SavedModel is TensorFlow's standard serialization format. It contains: `saved_model.pb` (graph definition, signature), `variables/` (weight values), `assets/` (external files). It's self-contained, language-neutral, and supports serving via TensorFlow Serving. Use `tf.saved_model.save()` or `model.export()` (Keras 3).
**Code:**
```python
import tensorflow as tf
model = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=(4,))])
model.save('saved_model_dir')            # no file extension -> SavedModel
import os
print(sorted(os.listdir('saved_model_dir')))
# ['assets', 'fingerprint.pb', 'keras_metadata.pb', 'saved_model.pb', 'variables']
```

## Q23: What is TensorFlow Serving?
**A:** TensorFlow Serving is a production-serving system for ML models. It handles: model versioning, automatic A/B testing, batching requests, gRPC and REST APIs, and model reloading without downtime. Deploy SavedModel format. Can be extended with custom ops and pre/post-processing pipelines.
**Code:**
```python
import tensorflow as tf
model = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=(4,))])
model.save('serving_model')    # SavedModel dir that TF Serving can load
# docker run -p 8501:8501 tensorflow/serving --model_name=serving_model
# POST /v1/models/serving_model:predict  with {"instances": [[...]]}
loaded = tf.saved_model.load('serving_model')
print(loaded(tf.zeros((1, 4), dtype=tf.float32)))
```

## Q24: What is TensorFlow Lite?
**A:** TensorFlow Lite (TFLite) is a lightweight solution for deploying models on mobile, embedded, and edge devices. It converts TF models to `.tflite` format, optimizes for latency and size (quantization, pruning), and runs on Android, iOS, microcontrollers, and Linux. Minimal binary size and hardware acceleration via GPU/Neural Networks API.
**Code:**
```python
import tensorflow as tf
model = tf.keras.Sequential([tf.keras.layers.Dense(8, input_shape=(4,))])
model.save('model.keras')
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)

interpreter = tf.lite.Interpreter(model_content=tflite_model)
interpreter.allocate_tensors()
print([t['name'] for t in interpreter.get_output_details()])
```

## Q25: What is TensorFlow.js?
**A:** TensorFlow.js enables ML model training and inference in the browser and Node.js. Supports: loading pre-trained models (TF Hub, Keras), transfer learning in the browser, and training from scratch. Uses WebGL/WebGPU for GPU acceleration. Use cases: client-side image classification, pose estimation, sentiment analysis.
**Code:**
```python
import tensorflow as tf
model = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=(4,))])
model.save('model.keras')
# pip install tensorflowjs
import tensorflowjs as tfjs
tfjs.converters.save_keras_model(model, 'tfjs_model')
# in the browser:
# const model = await tf.loadLayersModel('/tfjs_model/model.json');
```

## Q26: What is the difference between `tf.data.Dataset` and NumPy arrays for model input?
**A:** `tf.data.Dataset` provides: efficient data pipelining (parallel loading, prefetching, caching), on-the-fly preprocessing, shuffling, batching, and infinite data generation. It integrates with TF's execution pipelines. NumPy arrays must be loaded entirely in memory. For large datasets, use `tf.data` for performance and memory efficiency.
**Code:**
```python
import tensorflow as tf
import numpy as np
x = np.random.randn(5000, 8).astype('float32')
y = np.random.randn(5000, 1).astype('float32')
model = tf.keras.Sequential([tf.keras.layers.Dense(1)])
model.compile(optimizer='adam', loss='mse')

model.fit(x, y, epochs=2, verbose=0)   # NumPy: whole array must fit in RAM

ds = tf.data.Dataset.from_tensor_slices((x, y))
ds = ds.cache().shuffle(5000).batch(64).prefetch(tf.data.AUTOTUNE)
model.fit(ds, epochs=2, verbose=0)     # streamed, prefetched pipeline
```

## Q27: How do you create a tf.data pipeline?
**A:** ```python
dataset = tf.data.Dataset.from_tensor_slices((x, y))
dataset = dataset.shuffle(1000).batch(32).prefetch(tf.data.AUTOTUNE)
dataset = dataset.map(preprocess_fn, num_parallel_calls=tf.data.AUTOTUNE)
```
Key methods: `map` (apply function), `filter` (select samples), `batch` (group), `shuffle` (randomize), `prefetch` (overlap preparation and execution), `cache` (cache in memory/disk), `repeat` (loop indefinitely).
**Code:**
```python
import tensorflow as tf
x = tf.random.normal((1000, 8)); y = tf.random.normal((1000, 1))
dataset = tf.data.Dataset.from_tensor_slices((x, y))
dataset = dataset.shuffle(500).batch(32)
dataset = dataset.map(lambda a, b: (a * 2.0, b),
                      num_parallel_calls=tf.data.AUTOTUNE)
dataset = dataset.prefetch(tf.data.AUTOTUNE)
for batch_x, batch_y in dataset.take(2):
    print(batch_x.shape, batch_y.shape)   # (32, 8) (32, 1)
```

## Q28: What is prefetch in tf.data?
**A:** `dataset.prefetch(tf.data.AUTOTUNE)` overlaps data preprocessing and model execution. While the model trains on batch N, the CPU prepares batch N+1. This reduces idle time and improves throughput. `AUTOTUNE` lets TF dynamically tune the buffer size. Prefetch is typically the last transformation in a pipeline.
**Code:**
```python
import tensorflow as tf
def heavy_preprocess(x):
    return tf.sqrt(x) * 2.0
ds = tf.data.Dataset.range(1, 1000).map(
    lambda a: (heavy_preprocess(a), heavy_preprocess(a)))
ds = ds.batch(64).prefetch(tf.data.AUTOTUNE)   # prep batch N+1 while training N
model = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=(1,))])
model.compile(optimizer='adam', loss='mse')
model.fit(ds, epochs=2, verbose=0)
```

## Q29: What is a convolutional layer (Conv2D)?
**A:** `Conv2D` is a layer that applies convolution filters to input images. Parameters: `filters` (number of output channels), `kernel_size` (filter size, e.g., 3x3), `strides`, `padding` ('valid' or 'same'), `activation`, `dilation_rate`. Convolution preserves spatial structure, learns local patterns, and uses parameter sharing (same filter across image).
**Code:**
```python
import tensorflow as tf
conv = tf.keras.layers.Conv2D(
    filters=32, kernel_size=(3, 3), strides=(1, 1),
    padding='same', activation='relu', input_shape=(28, 28, 1))
x = tf.random.normal((1, 28, 28, 1))
print(conv(x).shape)   # (1, 28, 28, 32): 32 filters, channels-last
```

## Q30: What is pooling in CNNs?
**A:** Pooling reduces spatial dimensions and provides translation invariance. `MaxPooling2D` takes the maximum value in each window — preserves sharp features. `AveragePooling2D` takes the average — smoother. `GlobalAveragePooling2D` reduces each feature map to a single value — used before classification layers. Pooling reduces parameters and computation.
**Code:**
```python
import tensorflow as tf
x = tf.random.normal((1, 28, 28, 32))               # (batch, h, w, channels)
print(tf.keras.layers.MaxPooling2D(2)(x).shape)            # (1, 14, 14, 32)
print(tf.keras.layers.AveragePooling2D(2)(x).shape)        # (1, 14, 14, 32)
print(tf.keras.layers.GlobalAveragePooling2D()(x).shape)   # (1, 32)
```

## Q31: What is the difference between 'valid' and 'same' padding?
**A:** 'valid' padding: no padding, output size shrinks (e.g., 32x32 input + 3x3 filter = 30x30 output). 'same' padding: pad with zeros so output size equals input size (rounded up). 'same' is typically used to preserve spatial dimensions, especially in deep networks with many conv layers.
**Code:**
```python
import tensorflow as tf
x = tf.random.normal((1, 32, 32, 3))
out_valid = tf.keras.layers.Conv2D(8, 3, padding='valid')(x)
out_same  = tf.keras.layers.Conv2D(8, 3, padding='same')(x)
print(out_valid.shape)   # (1, 30, 30, 8) -> shrinks by (kernel-1)
print(out_same.shape)    # (1, 32, 32, 8) -> same spatial size
```

## Q32: What is batch normalization?
**A:** `BatchNormalization` normalizes layer outputs by mean and variance across the batch, then applies learnable scale (gamma) and shift (beta). Benefits: faster convergence (allows higher learning rates), reduces internal covariate shift, provides regularization, reduces sensitivity to initialization. Applied before or after activation depending on convention.
**Code:**
```python
import tensorflow as tf
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, input_shape=(8,)),
    tf.keras.layers.BatchNormalization(),     # normalize + learnable gamma/beta
    tf.keras.layers.Activation('relu'),
])
x = tf.random.normal((16, 8))
print(model(x).shape)   # (16, 64)
print(model.layers[1].trainable_weights[0].shape)   # gamma, shape (64,)
```

## Q33: What is dropout?
**A:** `Dropout` randomly sets a fraction of input units to 0 at each training step. Prevents co-adaptation of neurons and acts as regularization. Rate (0.2–0.5) controls fraction dropped. During inference, dropout is disabled and outputs are scaled. `Dropout` is effective in fully-connected layers; spatial dropout is used for conv layers.
**Code:**
```python
import tensorflow as tf
dropout = tf.keras.layers.Dropout(0.5)
x = tf.ones((8, 10))
kept = dropout(x, training=True)
print(tf.reduce_mean(tf.cast(tf.not_equal(kept, 0.), tf.float32)).numpy())
# ~0.5 -> roughly half the units are zeroed during training
print(tf.reduce_all(tf.equal(dropout(x, training=False), 1.0)).numpy())
# True -> dropout is disabled at inference, output unchanged
```

## Q34: What is a recurrent layer (LSTM, GRU)?
**A:** Recurrent layers process sequential data (text, time series, audio). `LSTM` (Long Short-Term Memory) uses input/forget/output gates and cell state to capture long-range dependencies. `GRU` (Gated Recurrent Unit) is simpler (two gates, no cell state). Both handle vanishing gradient problems in vanilla RNNs.
**Code:**
```python
import tensorflow as tf
x = tf.random.normal((4, 20, 32))       # (batch, timesteps, features)
lstm = tf.keras.layers.LSTM(64)(x)
gru  = tf.keras.layers.GRU(64)(x)
print(lstm.shape, gru.shape)            # (4, 64) (4, 64)
seq = tf.keras.layers.LSTM(64, return_sequences=True)(x)
print(seq.shape)                        # (4, 20, 64) one hidden state per step
```

## Q35: What is the difference between LSTM and GRU?
**A:** LSTM has three gates (input, forget, output) and a separate cell state — more expressive, more parameters, can capture longer dependencies. GRU has two gates (reset, update) and no cell state — simpler, faster, fewer parameters. GRU often performs similarly to LSTM with less computation. Use LSTM for very long sequences.
**Code:**
```python
import tensorflow as tf
inp = tf.keras.Input(shape=(20, 16))
lstm_model = tf.keras.Model(inp, tf.keras.layers.LSTM(32)(inp))
gru_model  = tf.keras.Model(inp, tf.keras.layers.GRU(32)(inp))
print(lstm_model.count_params())   # 6272  (3 gates + cell state -> more params)
print(gru_model.count_params())    # 4704  (2 gates, fewer parameters)
```

## Q36: What is an embedding layer?
**A:** `Embedding` layer maps discrete tokens (words, categories) to dense vector representations. Input: integer indices. Output: dense vectors. Parameters: `input_dim` (vocabulary size), `output_dim` (embedding size). Embeddings are learned during training. Pre-trained embeddings (Word2Vec, GloVe) can be loaded. Useful for: NLP, recommendation systems, categorical features.
**Code:**
```python
import tensorflow as tf
embed = tf.keras.layers.Embedding(input_dim=1000, output_dim=128)
tokens = tf.constant([[3, 27, 500, 41]])          # integer vocab ids
vecs = embed(tokens)
print(vecs.shape)                                  # (1, 4, 128)
print(vecs[0, 2, :4])                              # dense vector for id 500
```

## Q37: What is transfer learning?
**A:** Transfer learning uses a pre-trained model (trained on a large dataset like ImageNet) as a starting point for a new task. Approaches: feature extraction (freeze pre-trained layers, train new classifier on top) and fine-tuning (unfreeze some layers and train with a low learning rate). Saves time, requires less data, often performs better.
**Code:**
```python
import tensorflow as tf
base = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3), include_top=False, weights='imagenet')
base.trainable = False                           # freeze for feature extraction
model = tf.keras.Sequential([
    base,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(10, activation='softmax'),
])
model.compile(optimizer='adam', loss='categorical_crossentropy')
print(model(tf.random.normal((1, 224, 224, 3))).shape)   # (1, 10)
```

## Q38: How do you implement transfer learning with Keras?
**A:** ```python
base_model = tf.keras.applications.ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Freeze base
model = tf.keras.Sequential([base_model, GlobalAveragePooling2D(), Dense(10, activation='softmax')])
model.compile(optimizer='adam', loss='categorical_crossentropy')
```
After initial training, optionally unfreeze layers and fine-tune with a lower learning rate.
**Code:**
```python
import tensorflow as tf
base_model = tf.keras.applications.ResNet50(
    weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False                    # freeze the base model
model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(10, activation='softmax'),
])
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# fine-tuning stage: unfreeze and train with a low learning rate
base_model.trainable = True
model.compile(optimizer=tf.keras.optimizers.Adam(1e-5),
              loss='categorical_crossentropy',
              metrics=['accuracy'])
```

## Q39: What are common pre-trained models in Keras?
**A:** `tf.keras.applications` includes: ResNet50/101/152, VGG16/19, InceptionV3, Xception, MobileNetV2/V3 (lightweight), EfficientNetB0-B7 (state-of-the-art efficiency), DenseNet121/169/201, NASNetLarge/Mobile. Each has different trade-offs between accuracy, speed, and size.
**Code:**
```python
import tensorflow as tf
backbones = {
    'VGG16': tf.keras.applications.VGG16,
    'MobileNetV2': tf.keras.applications.MobileNetV2,
    'ResNet50': tf.keras.applications.ResNet50,
    'EfficientNetB0': tf.keras.applications.EfficientNetB0,
}
for name, app in backbones.items():
    model = app(include_top=False, weights='imagenet',
                input_shape=(224, 224, 3))
    print(f'{name}: {model.count_params():,} params')
```

## Q40: What is data augmentation in Keras?
**A:** `tf.keras.layers.Random*` and `tf.keras.preprocessing.image.ImageDataGenerator` generate training variations to improve generalization. Augmentations: rotation, zoom, flip, shift, brightness, contrast, shear. In TF 2.x, use Keras preprocessing layers: `RandomFlip`, `RandomRotation`, `RandomZoom`, `RandomContrast`, `Rescaling`. Applied on-the-fly during training.
**Code:**
```python
import tensorflow as tf
aug = tf.keras.Sequential([
    tf.keras.layers.RandomFlip('horizontal'),
    tf.keras.layers.RandomRotation(0.1),
    tf.keras.layers.RandomZoom(0.1),
    tf.keras.layers.RandomContrast(0.2),
])
img = tf.random.uniform((4, 224, 224, 3))
print(aug(img, training=True).shape)    # (4, 224, 224, 3), varied per call
print(tf.reduce_all(tf.equal(aug(img, training=False), img)).numpy())
# True -> augmentation is off during validation/inference
```

## Q41: How do you use Keras preprocessing layers for data augmentation?
**A:** ```python
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.1),
    tf.keras.layers.RandomZoom(0.1),
])
model = tf.keras.Sequential([data_augmentation, base_model, ...])
```
Preprocessing layers are part of the model, so they run on GPU during training and are automatically disabled during inference.
**Code:**
```python
import tensorflow as tf
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip('horizontal'),
    tf.keras.layers.RandomRotation(0.1),
    tf.keras.layers.RandomZoom(0.1),
])
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(224, 224, 3)),
    data_augmentation,                          # active only during training
    tf.keras.layers.Rescaling(1. / 255),
    tf.keras.layers.Conv2D(32, 3, activation='relu'),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(10, activation='softmax'),
])
model.compile(optimizer='adam', loss='categorical_crossentropy')
model.fit(tf.random.uniform((16, 224, 224, 3)),
          tf.keras.utils.to_categorical(
              tf.random.uniform((16,), 0, 10, tf.int32), 10),
          epochs=1, verbose=0)
```

## Q42: What is the Adam optimizer and how does it work?
**A:** Adam (Adaptive Moment Estimation) combines: 1) Momentum — accumulates past gradients (like SGD with momentum), 2) RMSprop — adaptive learning rates per parameter. It maintains exponentially decaying averages of past gradients (m) and squared gradients (v), with bias correction. Default LR: 0.001. Robust to sparse gradients, works well out of the box.
**Code:**
```python
import tensorflow as tf
opt = tf.keras.optimizers.Adam(
    learning_rate=0.001,
    beta_1=0.9,     # momentum: decaying avg of past gradients (m)
    beta_2=0.999,   # RMSprop:  decaying avg of squared gradients (v)
    epsilon=1e-7,   # bias-corrected m, v are used for the update step
)
model = tf.keras.Sequential([tf.keras.layers.Dense(1)])
model.compile(optimizer=opt, loss='mse')
x = tf.random.normal((100, 4)); y = tf.random.normal((100, 1))
model.fit(x, y, epochs=2, verbose=0)
```

## Q43: What is gradient clipping?
**A:** Gradient clipping prevents exploding gradients by capping gradient values. Methods: clip by value (`clipvalue=1.0` — clip each gradient component to [-1, 1]) and clip by norm (`clipnorm=1.0` — scale down if gradient norm exceeds 1). Essential for RNNs, transformers, and deep networks. Configure in optimizer: `Adam(clipnorm=1.0)`.
**Code:**
```python
import tensorflow as tf
opt_clip_value = tf.keras.optimizers.Adam(clipvalue=1.0)  # each grad in [-1, 1]
opt_clip_norm  = tf.keras.optimizers.Adam(clipnorm=1.0)   # grad norm capped at 1
model = tf.keras.Sequential([tf.keras.layers.Dense(1)])
model.compile(optimizer=opt_clip_norm, loss='mse')
x = tf.random.normal((100, 4)); y = tf.random.normal((100, 1))
model.fit(x, y, epochs=2, verbose=0)
```

## Q44: What is the learning rate and how do you schedule it?
**A:** Learning rate controls step size during gradient descent. Scheduling strategies: step decay (reduce by factor every N epochs), exponential decay (`ExponentialDecay`), cosine decay (`CosineDecay`), ReduceLROnPlateau (reduce when metric plateaus), warmup (gradually increase from small to target LR). Keras provides `LearningRateScheduler` and `ReduceLROnPlateau` callbacks.
**Code:**
```python
import tensorflow as tf
decay = tf.keras.optimizers.schedules.ExponentialDecay(
    initial_learning_rate=0.1,
    decay_steps=500,
    decay_rate=0.9,
    staircase=True,
)
opt = tf.keras.optimizers.SGD(learning_rate=decay)
print(opt.learning_rate(tf.constant(0)).numpy())     # 0.1
print(opt.learning_rate(tf.constant(500)).numpy())   # 0.09

plateau = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss',
                                               factor=0.5, patience=3)
model = tf.keras.Sequential([tf.keras.layers.Dense(1)])
model.compile(optimizer=opt, loss='mse')
```

## Q45: What is overfitting and how do you prevent it?
**A:** Overfitting occurs when a model learns training data too well (including noise) but fails to generalize. Prevention: more training data, data augmentation, simpler architectures, regularization (L1/L2), dropout, batch normalization, early stopping, cross-validation, and reducing model capacity.
**Code:**
```python
import tensorflow as tf
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(8,),
                          kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1),
])
model.compile(optimizer='adam', loss='mse')
callbacks = [tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)]
x = tf.random.normal((200, 8)); y = tf.random.normal((200, 1))
model.fit(x, y, epochs=100, validation_split=0.2,
          callbacks=callbacks, verbose=0)   # L2 + dropout + early stop
```

## Q46: What is the difference between L1 and L2 regularization?
**A:** L1 (Lasso) adds absolute weight values to the loss — encourages sparsity (some weights become exactly zero), useful for feature selection. L2 (Ridge) adds squared weight values — encourages small weights but not zero, keeps all features. L2 is more common in deep learning. Apply via `kernel_regularizer=tf.keras.regularizers.l2(0.01)`.
**Code:**
```python
import tensorflow as tf
l2_layer = tf.keras.layers.Dense(16, activation='relu',
                                 kernel_regularizer=tf.keras.regularizers.l2(0.01))
l1_layer = tf.keras.layers.Dense(16, activation='relu',
                                 kernel_regularizer=tf.keras.regularizers.l1(0.01))
x = tf.random.normal((4, 8))
print(l2_layer(x).shape)
print(l2_layer.losses)    # 0.01 * sum(w^2) -> small but non-zero weights
print(l1_layer.losses)    # 0.01 * sum(|w|)  -> drives small weights to 0
```

## Q47: What is a custom training loop in TensorFlow?
**A:** Instead of `model.fit()`, you write your own training loop for full control: ```python
for epoch in range(epochs):
    for batch in dataset:
        with tf.GradientTape() as tape:
            preds = model(batch_x)
            loss = loss_fn(batch_y, preds)
        grads = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))
```
Useful for: custom loss logic, multi-loss, adversarial training, gradient surgery, and research.
**Code:**
```python
import tensorflow as tf
model = tf.keras.Sequential([tf.keras.layers.Dense(1)])
optimizer = tf.keras.optimizers.SGD(0.05)
loss_fn = tf.keras.losses.MeanSquaredError()
x = tf.random.normal((100, 4)); y = tf.random.normal((100, 1))
dataset = tf.data.Dataset.from_tensor_slices((x, y)).batch(32)

for epoch in range(3):
    for batch_x, batch_y in dataset:
        with tf.GradientTape() as tape:
            loss = loss_fn(batch_y, model(batch_x, training=True))
        grads = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))
    tf.print('epoch', epoch, 'loss', loss)
```

## Q48: What is `tf.GradientTape`?
**A:** `tf.GradientTape` records operations for automatic differentiation. Inside the `with` block, all trainable operations are recorded. `tape.gradient(loss, variables)` computes gradients. Supports: nested tapes (higher-order gradients), persistent tapes (multiple gradient calls), and watching non-trainable variables.
**Code:**
```python
import tensorflow as tf
x = tf.Variable(3.0)
with tf.GradientTape() as tape:
    loss = x ** 2
print(tape.gradient(loss, x).numpy())   # d(x^2)/dx = 2*x = 6.0

with tf.GradientTape(persistent=True) as tape:   # multiple gradient() calls
    a, b = tf.Variable(2.0), tf.Variable(3.0)
    z = a * b
print(tape.gradient(z, a).numpy(), tape.gradient(z, b).numpy())  # 3.0 2.0
```

## Q49: How do you use GPUs with TensorFlow?
**A:** TF automatically uses available GPUs. Control GPU usage: `os.environ['CUDA_VISIBLE_DEVICES']='0'` to restrict visible GPUs. `tf.config.list_physical_devices('GPU')` to list. `tf.config.experimental.set_memory_growth(device, True)` for dynamic memory allocation. `tf.distribute.MirroredStrategy` for multi-GPU training.
**Code:**
```python
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'     # restrict to GPU 0
import tensorflow as tf
print(tf.config.list_physical_devices('GPU'))
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    tf.config.experimental.set_memory_growth(gpus[0], True)   # grow as needed
with tf.device('/GPU:0'):
    a = tf.random.normal((2000, 2000))
    print(tf.linalg.matmul(a, a).device)     # a GPU device name
```

## Q50: What is distributed training in TensorFlow?
**A:** `tf.distribute.Strategy` abstracts distributed training. Strategies: `MirroredStrategy` (sync SGD, single-host multi-GPU), `MultiWorkerMirroredStrategy` (multi-host), `TPUStrategy` (TPU pods), `ParameterServerStrategy` (async, parameter servers). MirroredStrategy copies model to each GPU, computes gradients in parallel, synchronizes via all-reduce.
**Code:**
```python
import tensorflow as tf
strategy = tf.distribute.MirroredStrategy()   # model copy per GPU, all-reduce sync
with strategy.scope():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(32, activation='relu', input_shape=(8,)),
        tf.keras.layers.Dense(1),
    ])
    model.compile(optimizer='adam', loss='mse')
x = tf.random.normal((256, 8)); y = tf.random.normal((256, 1))
model.fit(x, y, batch_size=32, epochs=2, verbose=0)
# others: MultiWorkerMirroredStrategy, TPUStrategy, ParameterServerStrategy
```

## Q51: What is mixed precision training?
**A:** Mixed precision uses float16 (half precision) for most operations while keeping float32 for critical parts (loss scaling, weight updates). Benefits: ~2x speedup on compatible GPUs (Tesla V100, A100, RTX series), 50% less memory. Enable with: `tf.keras.mixed_precision.set_global_policy('mixed_float16')` and add loss scaling.
**Code:**
```python
import tensorflow as tf
tf.keras.mixed_precision.set_global_policy('mixed_float16')
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', dtype='float32',
                          input_shape=(8,)),   # keep critical part in float32
    tf.keras.layers.Dense(1),
])
model.compile(optimizer='adam', loss='mse')   # Keras adds automatic loss scaling
x = tf.random.normal((64, 8)); y = tf.random.normal((64, 1))
model.fit(x, y, epochs=2, verbose=0)
print(model.dtype_policy.name)   # e.g. mixed_float16
```

## Q52: What is the `tf.keras.metrics` module?
**A:** Provides metric classes for evaluation: `Accuracy`, `Precision`, `Recall`, `AUC`, `MeanSquaredError`, `MeanAbsoluteError`, `TopKCategoricalAccuracy`, etc. Metrics can be updated per batch and queried at epoch end. For custom metrics, extend `tf.keras.metrics.Metric` and implement `update_state()`, `result()`, `reset_state()`.
**Code:**
```python
import tensorflow as tf
auc = tf.keras.metrics.AUC()                 # update per batch, query at end
auc.update_state(tf.constant([0, 1, 1, 0]),
                 tf.constant([0.1, 0.9, 0.7, 0.3]))
print(auc.result().numpy())

model = tf.keras.Sequential([tf.keras.layers.Dense(1, activation='sigmoid')])
model.compile(optimizer='adam', loss='binary_crossentropy',
              metrics=['accuracy', tf.keras.metrics.Precision(),
                       tf.keras.metrics.Recall(), tf.keras.metrics.AUC()])
x = tf.random.normal((200, 8))
y = tf.cast(tf.random.uniform((200, 1)) > 0.5, tf.float32)
model.fit(x, y, epochs=3, verbose=0)
```

## Q53: How do you create a custom layer in Keras?
**A:** Extend `tf.keras.layers.Layer`: implement `__init__` (define sublayers), `build()` (create weights, called on first use with input shape), `call()` (forward pass logic). Optionally implement `get_config()` for serialization. Example: define a custom activation or a specialized computation layer.
**Code:**
```python
import tensorflow as tf
class MyLinear(tf.keras.layers.Layer):
    def __init__(self, units=4):
        super().__init__()
        self.units = units

    def build(self, input_shape):            # weights are created here
        self.kernel = self.add_weight(
            shape=(input_shape[-1], self.units),
            initializer='random_normal', trainable=True)
        self.bias = self.add_weight(shape=(self.units,), initializer='zeros')

    def call(self, inputs):                  # forward pass logic
        return tf.matmul(inputs, self.kernel) + self.bias

layer = MyLinear(8)
print(layer(tf.random.normal((3, 5))).shape)   # (3, 8)
```

## Q54: What is the `call()` method in Keras layers?
**A:** `call()` defines the forward pass computation. Parameters: `inputs` (tensor), `training` (bool — to distinguish train vs inference behavior, e.g., for dropout/batchnorm), `mask` (for masking sequences). The method must return one tensor or a list of tensors.
**Code:**
```python
import tensorflow as tf
class DropoutDense(tf.keras.layers.Layer):
    def __init__(self, units):
        super().__init__()
        self.dense = tf.keras.layers.Dense(units)
        self.dropout = tf.keras.layers.Dropout(0.5)

    def call(self, inputs, training=None, mask=None):
        x = self.dense(inputs)
        return self.dropout(x, training=training)   # trains vs inference differ

layer = DropoutDense(8)
x = tf.random.normal((4, 6))
print(layer(x, training=True).shape)    # (4, 8)
print(layer(x, training=False).shape)   # (4, 8)
```

## Q55: How do you create a custom loss function in Keras?
**A:** Define a function that takes `y_true` and `y_pred` and returns a scalar loss: `def custom_loss(y_true, y_pred): return tf.reduce_mean(tf.square(y_true - y_pred))`. Pass to `compile(loss=custom_loss)`. For stateful losses, subclass `tf.keras.losses.Loss` with `call()` method.
**Code:**
```python
import tensorflow as tf
def huber_loss(y_true, y_pred):
    err = tf.abs(y_true - y_pred)
    return tf.reduce_mean(tf.where(err < 1.0, 0.5 * err ** 2, err - 0.5))

model = tf.keras.Sequential([tf.keras.layers.Dense(1)])
model.compile(optimizer='adam', loss=huber_loss, metrics=['mae'])
x = tf.random.normal((100, 4)); y = tf.random.normal((100, 1))
model.fit(x, y, epochs=2, verbose=0)

class HuberLoss(tf.keras.losses.Loss):      # stateful/subclassed variant
    def call(self, y_true, y_pred):
        err = tf.abs(y_true - y_pred)
        return tf.where(err < 1.0, 0.5 * err ** 2, err - 0.5)
model.compile(optimizer='adam', loss=HuberLoss())
```

## Q56: What are callbacks and how do you create a custom callback?
**A:** Custom callbacks extend `tf.keras.callbacks.Callback` and override methods: `on_epoch_begin/end`, `on_batch_begin/end`, `on_train_begin/end`, etc. Access `self.model` for the model, `self.model.history` for metrics, `self.params` for training parameters. Useful for custom logging, model manipulation, or external integrations.
**Code:**
```python
import tensorflow as tf
class BatchLogger(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        print(f'epoch {epoch}: loss={logs["loss"]:.4f} '
              f'val_loss={logs["val_loss"]:.4f}')

model = tf.keras.Sequential([tf.keras.layers.Dense(1)])
model.compile(optimizer='adam', loss='mse')
x = tf.random.normal((100, 4)); y = tf.random.normal((100, 1))
model.fit(x, y, epochs=2, validation_split=0.2,
          callbacks=[BatchLogger()], verbose=0)
```

## Q57: What is the TensorBoard callback?
**A:** `TensorBoard` callback logs metrics, histograms, graph, and embeddings for visualization in TensorBoard. Enable: `callbacks=[TensorBoard(log_dir='./logs')]`. View with: `tensorboard --logdir ./logs`. Visualizes: training metrics, model graph, layer histograms, image summaries, embeddings, and profiling data.
**Code:**
```python
import tensorflow as tf
tensorboard = tf.keras.callbacks.TensorBoard(
    log_dir='./logs',
    histogram_freq=1,      # log weight/gradient histograms each epoch
    write_graph=True,
    profile_batch=0,       # leave the profiler off for this snippet
)
model = tf.keras.Sequential([tf.keras.layers.Dense(16, input_shape=(8,)),
                             tf.keras.layers.Dense(1)])
model.compile(optimizer='adam', loss='mse')
x = tf.random.normal((128, 8)); y = tf.random.normal((128, 1))
model.fit(x, y, epochs=3, callbacks=[tensorboard], verbose=0)
# view: tensorboard --logdir ./logs
```

## Q58: What are Keras applications?
**A:** `tf.keras.applications` provides pre-trained model architectures with pre-trained weights. Common models: ResNet, VGG, Inception, MobileNet, EfficientNet, DenseNet. Each provides: `preprocess_input()` (proper input scaling), `decode_predictions()` (class label decoding), and configurable `include_top` (with/without classifier head).
**Code:**
```python
import tensorflow as tf
model = tf.keras.applications.MobileNetV2(weights='imagenet',
                                          input_shape=(224, 224, 3))
img = tf.random.uniform((1, 224, 224, 3), maxval=256)     # raw-looking image
prepared = tf.keras.applications.mobilenet_v2.preprocess_input(img)
preds = model(prepared)
print(tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3))
```

## Q59: What is the Functional API use case for multi-input models?
**A:** Multi-input models take multiple independent inputs that are combined later: ```python
input_a = Input(shape=(32,))
input_b = Input(shape=(64,))
merged = Concatenate()([Dense(16)(input_a), Dense(32)(input_b)])
output = Dense(1, activation='sigmoid')(merged)
model = Model(inputs=[input_a, input_b], outputs=output)
```
Used for: multi-modal data, ensemble-like architectures, siamese networks.
**Code:**
```python
import tensorflow as tf
input_a = tf.keras.Input(shape=(32,), name='text_input')
input_b = tf.keras.Input(shape=(64,), name='image_input')
a = tf.keras.layers.Dense(16, activation='relu')(input_a)
b = tf.keras.layers.Dense(32, activation='relu')(input_b)
merged = tf.keras.layers.Concatenate()([a, b])
output = tf.keras.layers.Dense(1, activation='sigmoid')(merged)
model = tf.keras.Model(inputs=[input_a, input_b], outputs=output)
model.compile(optimizer='adam', loss='binary_crossentropy')
x_a = tf.random.normal((64, 32)); x_b = tf.random.normal((64, 64))
y = tf.cast(tf.random.uniform((64, 1)) > 0.5, tf.float32)
model.fit([x_a, x_b], y, epochs=2, verbose=0)
```

## Q60: What is a siamese network in Keras?
**A:** A siamese network uses shared weights between two subnetworks to compare inputs. Built with Functional API: same Dense layers applied to two inputs via shared layers. Output is a similarity score (e.g., cosine distance). Used for: face verification, signature comparison, similarity learning, one-shot learning.
**Code:**
```python
import tensorflow as tf
shared = tf.keras.layers.Dense(8, activation='relu')   # shared weights
input1 = tf.keras.Input(shape=(4,))
input2 = tf.keras.Input(shape=(4,))
emb1 = shared(input1); emb2 = shared(input2)           # same layer, two inputs
dist = tf.keras.layers.Lambda(
    lambda v: tf.reduce_sum(tf.square(v[0] - v[1]),
                            axis=1, keepdims=True))([emb1, emb2])
model = tf.keras.Model(inputs=[input1, input2], outputs=dist)
model.compile(optimizer='adam', loss='mse')
print(model([tf.ones((3, 4)), tf.zeros((3, 4))]).shape)   # (3, 1)
```

## Q61: How do you handle imbalanced datasets?
**A:** Approaches: 1) `class_weight` in `model.fit()` — higher weight for minority classes, 2) Oversampling (duplicate minority), 3) Undersampling (reduce majority), 4) SMOTE (synthetic samples), 5) Focal Loss (focus on hard examples), 6) Weighted loss function, 7) Stratified splitting for validation.
**Code:**
```python
import tensorflow as tf
model = tf.keras.Sequential([tf.keras.layers.Dense(1, activation='sigmoid')])
model.compile(optimizer='adam', loss='binary_crossentropy',
              metrics=['accuracy'])
x = tf.random.normal((800, 8))
y = tf.concat([tf.zeros((700,)), tf.ones((100,))], 0)   # 7:1 imbalance
model.fit(x, y, epochs=3, verbose=0,
          class_weight={0: 1.0, 1: 7.0})   # up-weight the minority class
```

## Q62: What is focal loss?
**A:** Focal Loss down-weights easy examples and focuses on hard, misclassified examples. It adds a modulating factor `(1 - p_t)^γ` to the cross-entropy loss. When γ=0, focal loss = cross-entropy. Higher γ (e.g., 2) focuses more on hard examples. Commonly used in object detection (RetinaNet) and severe class imbalance.
**Code:**
```python
import tensorflow as tf
def focal_loss(alpha=0.25, gamma=2.0):
    def loss(y_true, y_pred):
        p = tf.clip_by_value(y_pred, 1e-7, 1 - 1e-7)
        ce = tf.keras.losses.binary_crossentropy(y_true, p)
        p_t = tf.where(y_true == 1.0, p, 1 - p)
        return tf.reduce_mean(alpha * (1 - p_t) ** gamma * ce)  # gamma=0 -> CE
    return loss
model = tf.keras.Sequential([tf.keras.layers.Dense(1, activation='sigmoid')])
model.compile(optimizer='adam', loss=focal_loss(gamma=2.0))
x = tf.random.normal((100, 4))
y = tf.cast(tf.random.uniform((100, 1)) > 0.8, tf.float32)   # imbalanced labels
model.fit(x, y, epochs=2, verbose=0)
```

## Q63: How do you perform hyperparameter tuning in TensorFlow?
**A:** Methods: 1) Grid search (exhaustive combinations), 2) Random search (random combinations — more efficient), 3) Bayesian optimization (Keras Tuner), 4) Early stopping-based methods (Hyperband). Keras Tuner provides: `RandomSearch`, `Hyperband`, `BayesianOptimization` with intuitive API for defining search spaces.
**Code:**
```python
import tensorflow as tf
import keras_tuner as kt   # pip install keras-tuner

def build_model(hp):
    units = hp.Int('units', 32, 128, step=32)
    lr = hp.Choice('lr', [1e-3, 1e-2])
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(units, activation='relu', input_shape=(8,)),
        tf.keras.layers.Dense(1)])
    model.compile(optimizer=tf.keras.optimizers.Adam(lr), loss='mse')
    return model

tuner = kt.RandomSearch(build_model, objective='val_loss', max_trials=4)
x = tf.random.normal((200, 8)); y = tf.random.normal((200, 1))
tuner.search(x, y, epochs=10, validation_split=0.2, verbose=0)
print(tuner.get_best_hyperparameters(1)[0].values)   # best hp combination
```

## Q64: What is the Keras Tuner?
**A:** Keras Tuner is a library for hyperparameter tuning. Define a model-building function with `hp.Choice`, `hp.Int`, `hp.Float` for searchable parameters. Run: `tuner = RandomSearch(build_model, objective='val_accuracy', max_trials=100)` then `tuner.search(x_train, y_train)`. Supports: search algorithms, distribution strategies, and callback integration.
**Code:**
```python
import tensorflow as tf
import keras_tuner as kt

def build(hp):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(hp.Int('units', 8, 64, step=8),
                              input_shape=(8,)),
        tf.keras.layers.Dense(1)])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            hp.Float('lr', 1e-4, 1e-2, sampling='log')),
        loss='mse')
    return model

tuner = kt.Hyperband(build, objective='val_loss', max_epochs=10, factor=3)
x = tf.random.normal((200, 8)); y = tf.random.normal((200, 1))
tuner.search(x, y, validation_split=0.2, verbose=0)
print(tuner.get_best_hyperparameters(1)[0].values)
```

## Q65: What is the difference between `model.fit()` and `model.fit_generator()`?
**A:** `model.fit()` accepts data as arrays or `tf.data.Dataset`. `model.fit_generator()` (deprecated in TF 2.1+) accepted Python generators for data loading. In TF 2.x, always use `model.fit()` with `tf.data.Dataset` or arrays. The unified API handles both cases efficiently.
**Code:**
```python
import tensorflow as tf
x = tf.random.normal((200, 8)); y = tf.random.normal((200, 1))
model = tf.keras.Sequential([tf.keras.layers.Dense(1)])
model.compile(optimizer='adam', loss='mse')

def generator():
    for i in range(0, 200, 32):
        yield x[i:i + 32], y[i:i + 32]

ds = tf.data.Dataset.from_generator(
    generator,
    output_signature=(tf.TensorSpec((None, 8), tf.float32),
                      tf.TensorSpec((None, 1), tf.float32)))
model.fit(ds, epochs=3, verbose=0)   # fit_generator() is deprecated; use fit()
```

## Q66: How does TensorFlow handle model serialization for serving?
**A:** `model.save('path')` creates a SavedModel. TensorFlow Serving loads SavedModels and exposes gRPC/REST endpoints. For mobile: convert to TFLite. For JS: convert to TFJS format. For cloud: deploy to Vertex AI, Sagemaker, or custom containers with TF Serving.
**Code:**
```python
import tensorflow as tf
model = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=(4,))])
model.compile(optimizer='adam', loss='mse')
model.save('deploy_model')                  # SavedModel -> TF Serving / cloud

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite = converter.convert()                # mobile / edge (.tflite)
with open('model.tflite', 'wb') as f:
    f.write(tflite)

# pip install tensorflowjs
import tensorflowjs as tfjs
tfjs.converters.save_keras_model(model, 'web_model')   # browser (TF JS)
```

## Q67: What is ONNX and can TensorFlow export to it?
**A:** ONNX (Open Neural Network Exchange) is an open format for ML models. TF models can be converted to ONNX via `tf2onnx` library. Benefits: interoperability with PyTorch, ONNX Runtime optimization, deployment on edge devices. However, some TF ops may not have ONNX equivalents, requiring workarounds.
**Code:**
```python
import tensorflow as tf
import tf2onnx                       # pip install tf2onnx
model = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=(4,))])
model.compile(optimizer='adam', loss='mse')
onnx_model, _ = tf2onnx.convert.from_keras(model, opset=13)
with open('model.onnx', 'wb') as f:
    f.write(onnx_model.SerializeToString())
# now interchangeable with PyTorch / ONNX Runtime tooling
```

## Q68: What is TensorFlow Extended (TFX)?
**A:** TFX is a production ML pipeline platform. Components: ExampleGen (data ingestion), StatisticsGen (data analysis), SchemaGen (schema inference), Transform (feature engineering), Trainer (model training), Tuner (hyperparameter tuning), Evaluator (model validation), Pusher (deployment). Uses Apache Beam for distributed pipeline execution.
**Code:**
```python
# TFX pipeline components (pip install tfx; orchestrated via Apache Beam)
from tfx import v1 as tfx
from tfx.components import CsvExampleGen, StatisticsGen, Trainer
from tfx.proto import trainer_pb2

example_gen = CsvExampleGen(input_base='data/')               # data ingestion
statistics_gen = StatisticsGen(examples=example_gen.outputs['examples'])
trainer = Trainer(
    module_file='trainer.py',                                 # training code
    examples=example_gen.outputs['examples'],
    train_args=trainer_pb2.TrainArgs(num_steps=1000),
    eval_args=trainer_pb2.EvalArgs(num_steps=100),
)
# full graph also adds SchemaGen, Transform, Evaluator, Pusher
```

## Q69: What is TensorFlow Data Validation (TFDV)?
**A:** TFDV analyzes and validates data to detect anomalies. Features: schema inference, statistics computation, data drift detection, skew detection (train vs serving), and anomaly visualization. Helps catch data quality issues before they affect model performance in production.
**Code:**
```python
import tensorflow_data_validation as tfdv   # pip install tensorflow-data-validation
train_stats = tfdv.generate_statistics_from_csv('train.csv')
schema = tfdv.infer_schema(train_stats)      # infer a schema from the data

eval_stats = tfdv.generate_statistics_from_csv('eval.csv')
anomalies = tfdv.validate_statistics(eval_stats, schema)   # drift / mismatch
print(anomalies)
```

## Q70: What is TensorFlow Model Analysis (TFMA)?
**A:** TFMA evaluates models on large datasets and provides detailed slicing and fairness analysis. Computes metrics across slices (e.g., accuracy by age group, gender). Detects model bias and fairness issues. Integrates with TFX for continuous evaluation.
**Code:**
```python
import tensorflow_model_analysis as tfma   # pip install tensorflow-model-analysis
eval_config = tfma.EvalConfig(
    model_specs=[tfma.ModelSpec(label_key='label')],
    metrics_specs=[tfma.MetricsSpec(metrics=[
        tfma.MetricConfig(class_name='SparseCategoricalAccuracy'),
        tfma.MetricConfig(class_name='ExampleCount'),
    ])],
    slicing_specs=[tfma.SlicingSpec(feature_keys=['age_group'])],  # fairness slice
)
results = tfma.run_model_analysis(eval_config=eval_config,
                                  model='deploy_model',
                                  data_location='eval.tfrecords')
tfma.view.render_slicing_metrics(results)
```

## Q71: What are Keras callbacks for model checkpointing?
**A:** `ModelCheckpoint` saves weights during training. `BackupAndRestore` enables recovery from interruptions. `EarlyStopping` halts training when no improvement. `ReduceLROnPlateau` adapts learning rate. `TerminateOnNaN` stops on NaN loss. `CSVLogger` logs metrics to CSV. `ProgbarLogger` displays progress.
**Code:**
```python
import tensorflow as tf
callbacks = [
    tf.keras.callbacks.ModelCheckpoint('best.keras', save_best_only=True,
                                       monitor='val_loss'),
    tf.keras.callbacks.BackupAndRestore(backup_dir='./backup'),
    tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5),
    tf.keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=3),
    tf.keras.callbacks.TerminateOnNaN(),
    tf.keras.callbacks.CSVLogger('training_log.csv'),
]
model = tf.keras.Sequential([tf.keras.layers.Dense(1)])
model.compile(optimizer='adam', loss='mse')
x = tf.random.normal((100, 4)); y = tf.random.normal((100, 1))
model.fit(x, y, epochs=10, validation_split=0.2,
          callbacks=callbacks, verbose=0)
```

## Q72: How do you implement learning rate warmup?
**A:** ```python
def warmup_schedule(epoch):
    if epoch < 5:
        return 0.001 * (epoch + 1) / 5  # Linear warmup
    else:
        return 0.001 * 0.1 ** (epoch // 10)  # Then decay
callback = LearningRateScheduler(warmup_schedule)
```
Or use `tf.keras.optimizers.schedules.CosineDecay` with warmup via custom schedule.
**Code:**
```python
import tensorflow as tf
def warmup_then_decay(epoch, total=100, warmup_epochs=5, peak_lr=0.001):
    if epoch < warmup_epochs:                       # linear warmup
        return peak_lr * (epoch + 1) / warmup_epochs
    progress = (epoch - warmup_epochs) / max(1, total - warmup_epochs)
    return peak_lr * (1 - progress)                 # linear decay afterwards

scheduler = tf.keras.callbacks.LearningRateScheduler(warmup_then_decay)
print(scheduler.schedule(0))    # 0.0002
print(scheduler.schedule(5))    # 0.001   warmup complete
print(scheduler.schedule(55))   # ~0.0005 halfway through decay
model = tf.keras.Sequential([tf.keras.layers.Dense(1)])
model.compile(optimizer=tf.keras.optimizers.SGD(), loss='mse')
```

## Q73: What is gradient accumulation?
**A:** Gradient accumulation simulates larger batch sizes by accumulating gradients over multiple forward passes before updating weights. Used when GPU memory limits batch size. Pseudocode: loop N batches, sum gradients, then apply optimizer step. Not built into standard Keras — requires custom training loop.
**Code:**
```python
import tensorflow as tf
model = tf.keras.Sequential([tf.keras.layers.Dense(1)])
opt = tf.keras.optimizers.Adam(0.01)
loss_fn = tf.keras.losses.MeanSquaredError()
accum_steps = 4                       # emulate a 4x larger batch on GPU
x = tf.random.normal((96, 4)); y = tf.random.normal((96, 1))
ds = tf.data.Dataset.from_tensor_slices((x, y)).batch(8)

accum_grads = [tf.zeros_like(v) for v in model.trainable_variables]
for step, (bx, by) in enumerate(ds):
    with tf.GradientTape() as tape:
        loss = loss_fn(by, model(bx, training=True)) / accum_steps
    grads = tape.gradient(loss, model.trainable_variables)
    for acc, g in zip(accum_grads, grads):
        acc.assign_add(g)                          # accumulate
    if (step + 1) % accum_steps == 0:              # one update every N steps
        opt.apply_gradients(zip(accum_grads, model.trainable_variables))
        for acc in accum_grads:
            acc.assign(tf.zeros_like(acc))
```

## Q74: What is quantization in TensorFlow Lite?
**A:** Quantization reduces model precision from float32 to int8 or float16. Types: post-training quantization (convert after training, easiest), quantization-aware training (simulate quantization during training, best accuracy). Benefits: 4x smaller model, 2-4x faster on compatible hardware, lower power consumption.
**Code:**
```python
import tensorflow as tf
model = tf.keras.Sequential([tf.keras.layers.Dense(16, input_shape=(4,)),
                             tf.keras.layers.Dense(1)])
model.save('model.keras')

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]     # post-training quant
tflite_model = converter.convert()
with open('model_int8.tflite', 'wb') as f:
    f.write(tflite_model)

converter.target_spec.supported_types = [tf.float16]     # float16 variant
with open('model_fp16.tflite', 'wb') as f:
    f.write(converter.convert())
```

## Q75: What is pruning in TensorFlow?
**A:** Pruning removes unnecessary weights (sets them to zero) to reduce model size. The `tfmot` (TensorFlow Model Optimization Toolkit) provides: weight pruning (remove by magnitude), structured pruning (remove entire neurons/channels). Combined with quantization for significant size reduction with minimal accuracy loss.
**Code:**
```python
import tensorflow as tf
import tensorflow_model_optimization as tfmot   # pip install tensorflow-model-optimization

model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(8,)),
    tf.keras.layers.Dense(1),
])
pruned = tfmot.sparsity.keras.prune_low_magnitude(
    model, tfmot.sparsity.keras.PolynomialDecay(
        initial_sparsity=0.3, final_sparsity=0.7,
        begin_step=0, end_step=1000))
pruned.compile(optimizer='adam', loss='mse')
x = tf.random.normal((200, 8)); y = tf.random.normal((200, 1))
pruned.fit(x, y, epochs=3, verbose=0,
           callbacks=[tfmot.sparsity.keras.UpdatePruningStep()])
```

## Q76: What is the KerasCV library?
**A:** KerasCV is a library for computer vision tasks built on Keras. Provides: model presets (YOLOV8, RetinaNet, Mask R-CNN), data augmentation, preprocessing, and evaluation metrics. Simplifies building: object detection, image segmentation, image classification pipelines with consistent API.
**Code:**
```python
import keras_cv   # pip install keras-cv
import tensorflow as tf
model = keras_cv.models.YOLOV8Detector.from_preset(
    'yolo_v8_xs_backbone_coco',
    bounding_box_format='xywh')                    # ready-to-train detector
model.compile(optimizer='adam')
print(model(tf.keras.Input(shape=(640, 640, 3))).box_predictions.shape)
```

## Q77: What is the KerasNLP library?
**A:** KerasNLP is a library for NLP tasks on Keras. Provides: model presets (BERT, GPT-2, RoBERTa, T5, OPT), tokenizers (WordPiece, BPE, SentencePiece), and preprocessing layers. Supports: text classification, sequence labeling, question answering, causal LM, and masked LM.
**Code:**
```python
import keras_nlp   # pip install keras-nlp
import tensorflow as tf
classifier = keras_nlp.models.BertClassifier.from_preset(
    'bert_tiny_en_uncased', num_classes=3)         # preset-backed classifier
features = classifier.backbone(
    tf.keras.Input(shape=(None,), dtype='int32'))
print(tuple(features.shape))            # (None, None, 128) token embeddings
# presets cover BERT, GPT-2, RoBERTa, T5, OPT, Llama, Gemma, ...
```

## Q78: How do you use BERT with KerasNLP?
**A:** ```python
import keras_nlp
classifier = keras_nlp.models.BertClassifier.from_preset("bert_base_uncased", num_classes=2)
classifier.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
classifier.fit(x_train, y_train, epochs=3)
```
KerasNLP handles tokenization, preprocessing, and model architecture automatically.
**Code:**
```python
import keras_nlp
import tensorflow as tf
classifier = keras_nlp.models.BertClassifier.from_preset(
    'bert_tiny_en_uncased', num_classes=2)
classifier.compile(optimizer=tf.keras.optimizers.Adam(2e-5),
                   loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# strings in, preprocessing handled internally
x = tf.constant(['a great film with a perfect ending',
                 'boring and far too long'])
y = tf.constant([1, 0])
classifier.fit(x, y, epochs=1, verbose=0)
print(classifier.predict(['a great film'], verbose=0).shape)   # (1, 2)
```

## Q79: What is a Transformer model?
**A:** The Transformer (Vaswani et al., 2017) uses self-attention instead of recurrence for sequence processing. Key components: multi-head attention (captures relationships between all positions), feed-forward networks, positional encoding, layer normalization, and residual connections. Foundation of BERT, GPT, T5, and modern NLP.
**Code:**
```python
import tensorflow as tf
x = tf.random.normal((2, 10, 16))     # (batch, seq_len, d_model)
attn = tf.keras.layers.MultiHeadAttention(num_heads=2, key_dim=8)
out = attn(x, x)                                   # self-attention
out = tf.keras.layers.LayerNormalization()(out + x)   # residual + layer norm
ffn = tf.keras.layers.Dense(32, activation='relu')
out = tf.keras.layers.Dense(16)(ffn(out))
out = tf.keras.layers.LayerNormalization()(out + x)   # feed-forward block
print(out.shape)   # (2, 10, 16)
```

## Q80: What is self-attention in Transformers?
**A:** Self-attention computes weighted sums of all elements in a sequence, where weights are based on pairwise compatibility. Each element has: Query (Q), Key (K), Value (V). Attention scores = softmax(Q·K^T/√d_k)·V. Multi-head attention runs multiple attention layers in parallel, capturing different relationship types.
**Code:**
```python
import tensorflow as tf
def scaled_dot_product_attention(q, k, v):
    d_k = tf.cast(tf.shape(k)[-1], tf.float32)
    scores = tf.matmul(q, k, transpose_b=True) / tf.sqrt(d_k)   # Q·K^T/√d_k
    weights = tf.nn.softmax(scores, axis=-1)
    return tf.matmul(weights, v), weights

q = tf.random.normal((1, 3, 8)); k = tf.random.normal((1, 3, 8))
v = tf.random.normal((1, 3, 8))
out, w = scaled_dot_product_attention(q, k, v)
print(out.shape, w.shape)   # (1, 3, 8) (1, 3, 3)

mha = tf.keras.layers.MultiHeadAttention(num_heads=4, key_dim=8)
print(mha(q, k, v).shape)   # heads run attention in parallel: (1, 3, 8)
```

## Q81: What is the difference between TensorFlow 1.x and 2.x?
**A:** TF 2.x: eager execution by default, Keras as high-level API, `tf.function` for graphs, simplified APIs (no more `tf.Session`, `tf.placeholder`), tighter integration with Python, eager debugging, and removal of deprecated APIs. TF 1.x used static graphs — define-then-run paradigm.
**Code:**
```python
import tensorflow as tf
# TF 2.x: eager by default, no tf.Session / tf.placeholder
x = tf.constant([[1., 2.]])
y = tf.linalg.matmul(x, tf.ones((2, 1)))
print(y.numpy())                        # eager result: [[3.]]

@tf.function                            # TF 2.x way to build graphs
def f(a):
    return a * 2
concrete = f.get_concrete_function(tf.TensorSpec((None,), tf.float32))
print(concrete(tf.constant([1., 2., 3.])).numpy())
```

## Q82: What is Graph mode vs Eager mode?
**A:** Eager mode (default in TF 2.x): operations execute immediately, results are concrete tensors, easy debugging. Graph mode: builds a computational graph first (via `tf.function`), then executes the entire graph for better optimization, portability, and deployment. Graph mode is faster for repeated executions.
**Code:**
```python
import tensorflow as tf
def compute(a, b):
    return (a + b) * 2

# Eager: executes immediately, returns a concrete tensor
print(compute(tf.constant(3.), tf.constant(4.)).numpy())   # 14

# Graph: trace once, run the cached graph repeatedly
graph_fn = tf.function(compute)
print(graph_fn(tf.constant(3.), tf.constant(4.)).numpy())  # 14
for _ in range(10):
    graph_fn(tf.constant(1.), tf.constant(2.))   # no re-tracing
```

## Q83: How do you debug TensorFlow models?
**A:** Tools: eager execution (print tensors directly), `tf.print` (works in graphs), TensorBoard (visualize metrics/graphs), `tf.debugging` (asserts, check numeric), `tf.config.run_functions_eagerly(True)` (disable graph for debugging), Python debugger (pdb/ipdb) — works in eager mode.
**Code:**
```python
import tensorflow as tf
@tf.function
def safe_scale(x):
    tf.debugging.assert_all_finite(x, 'input must be finite')   # NaN check
    tf.print('scaling', x)                                       # graph-safe print
    return x * 2

print(safe_scale(tf.constant([1., 2., 3.])).numpy())
tf.config.run_functions_eagerly(True)   # force eager while debugging
print(safe_scale(tf.constant([5.])).numpy())
```

## Q84: How do you handle NaN loss during training?
**A:** Causes: exploding gradients, learning rate too high, inappropriate initialization, division by zero, log(0) in loss. Fixes: gradient clipping, lower learning rate, batch normalization, proper weight initialization, label smoothing, data normalization, check for NaN in predictions. Use `TerminateOnNaN` callback.
**Code:**
```python
import tensorflow as tf
model = tf.keras.Sequential([tf.keras.layers.Dense(64, input_shape=(8,)),
                             tf.keras.layers.Dense(1)])
model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=1e-4,        # a low, safe LR
        clipnorm=1.0),             # clip exploding gradients
    loss='mse')
callbacks = [tf.keras.callbacks.TerminateOnNaN(),   # stop if loss becomes NaN
             tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)]
x = tf.random.normal((200, 8)); y = tf.random.normal((200, 1))
model.fit(x, y, epochs=50, callbacks=callbacks, verbose=0)
```

## Q85: What is weight initialization and why does it matter?
**A:** Weight initialization sets initial values for model parameters. Bad initialization causes: vanishing/exploding gradients, slow convergence. Common methods: Glorot/Xavier (tanh activation), He (ReLU), LeCun (SELU). Keras uses sensible defaults (Glorot uniform for Dense, He normal for Conv2D). Proper initialization is critical for deep networks.
**Code:**
```python
import tensorflow as tf
layer = tf.keras.layers.Dense(
    32, activation='relu',
    kernel_initializer='he_normal',     # suited to ReLU activations
    bias_initializer='zeros')
layer.build((None, 16))
print(layer.kernel.shape)                                  # (16, 32)
print(float(tf.reduce_mean(layer.kernel ** 2)))            # ~1.0 (He scaling)
model = tf.keras.Sequential([layer, tf.keras.layers.Dense(1)])
```

## Q86: What is the difference between `kernel_initializer` and `bias_initializer`?
**A:** `kernel_initializer` sets the initial weight matrix values. `bias_initializer` sets initial bias vector values (default is zeros). Both are layer parameters. Common initializers: 'glorot_uniform', 'he_normal', 'zeros', 'ones', 'random_normal', 'random_uniform', 'orthogonal'.
**Code:**
```python
import tensorflow as tf
layer = tf.keras.layers.Dense(
    8,
    kernel_initializer=tf.keras.initializers.RandomNormal(stddev=0.02),
    bias_initializer=tf.keras.initializers.Zeros())
layer.build((None, 4))
print(layer.kernel.shape)          # (4, 8)   random-normal weights
print(layer.bias.numpy())          # [0. 0. ...]  default zeros bias
```

## Q87: What is the `@tf.function` decorator and AutoGraph?
**A:** `@tf.function` compiles Python functions to TF graphs. AutoGraph converts Python control flow (if/while/for) into TF graph operations. Limitations: Python side effects (print, list append) work differently, dynamic data structures may not trace correctly. Use `tf.print()` and `tf.TensorArray` for graph-compatible alternatives.
**Code:**
```python
import tensorflow as tf
@tf.function
def count_positives(x):
    n = tf.constant(0)
    for v in x:                  # AutoGraph converts the loop to graph ops
        if v > 0:
            n += 1
    return n
print(count_positives(tf.constant([1., -2., 3., 0.])).numpy())   # 2
```

## Q88: How do you handle variable-length sequences in Keras?
**A:** Use `tf.keras.layers.Masking` or `Embedding(mask_zero=True)` to ignore padding. Pad sequences to same length with `tf.keras.preprocessing.sequence.pad_sequences()`. For RNNs, set `mask_zero=True` in Embedding — the RNN will skip masked timesteps.
**Code:**
```python
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
seqs = [[1, 2, 3, 4], [5, 6], [7]]            # variable length
padded = pad_sequences(seqs, maxlen=4, dtype='int32',
                       padding='post', value=0)
print(padded)       # [[1 2 3 4] [5 6 0 0] [7 0 0 0]]

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=10, output_dim=8, mask_zero=True),
    tf.keras.layers.LSTM(4),                  # skips the padded/masked steps
    tf.keras.layers.Dense(1),
])
print(model(padded).shape)                    # (3, 1)
```

## Q89: What is the `add_loss()` method in Keras?
**A:** `add_loss()` allows adding custom losses from within layers or models. Useful for: regularization losses (activation regularization), consistency losses, auxiliary losses. Accumulated losses are added to the model's total loss during `compile()`. Example: `self.add_loss(tf.reduce_mean(self.kernel ** 2))`.
**Code:**
```python
import tensorflow as tf
class DecayLayer(tf.keras.layers.Layer):
    def __init__(self, units):
        super().__init__()
        self.units = units
    def build(self, input_shape):
        self.w = self.add_weight(shape=(input_shape[-1], self.units))
    def call(self, x):
        self.add_loss(1e-3 * tf.reduce_sum(tf.square(self.w)))  # extra loss
        return tf.matmul(x, self.w)

model = tf.keras.Sequential([tf.keras.layers.Input(shape=(8,)),
                             DecayLayer(4), tf.keras.layers.Dense(1)])
model.compile(optimizer='adam', loss='mse')
x = tf.random.normal((64, 8)); y = tf.random.normal((64, 1))
model.fit(x, y, epochs=2, verbose=0)
print(len(model.losses))   # 1 -> the add_loss() term is in the total loss
```

## Q90: What are Keras metrics and how do you track them?
**A:** Metrics track model performance during training. Built-in: accuracy, precision, recall, AUC, MSE, MAE. Track via `model.compile(metrics=[...])`. Available in `model.history.history` after training. Custom metrics extend `tf.keras.metrics.Metric`. For multiple metrics, use list or dict (for multi-output models).
**Code:**
```python
import tensorflow as tf
model = tf.keras.Sequential([tf.keras.layers.Dense(1, activation='sigmoid')])
model.compile(optimizer='adam', loss='binary_crossentropy',
              metrics=['accuracy', tf.keras.metrics.Precision(),
                       tf.keras.metrics.Recall(), tf.keras.metrics.AUC()])
x = tf.random.normal((200, 8))
y = tf.cast(tf.random.uniform((200, 1)) > 0.5, tf.float32)
history = model.fit(x, y, epochs=3, validation_split=0.2, verbose=0)
print(sorted(history.history))   # each epoch's metrics after training
```

## Q91: How do you save and load Keras models?
**A:** Save: `model.save('path.keras')` (Keras v3 format, recommended) or `model.save('path.h5')` (HDF5 legacy). Load: `model = tf.keras.models.load_model('path.keras')`. For weights only: `model.save_weights('path.weights.h5')` and `model.load_weights('path.weights.h5')`. The full model includes architecture, weights, optimizer state, and compile config.
**Code:**
```python
import tensorflow as tf
model = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=(4,))])
model.compile(optimizer='adam', loss='mse')
model.save('model.keras')                        # Keras v3 format (recommended)
reloaded = tf.keras.models.load_model('model.keras')

model.save_weights('weights.weights.h5')         # weights only
reloaded.load_weights('weights.weights.h5')
print(reloaded.predict(tf.random.normal((2, 4)), verbose=0).shape)
```

## Q92: What is `get_config()` and `from_config()` in Keras?
**A:** `get_config()` returns a dictionary of a layer/model's configuration (parameters). `from_config()` reconstructs the layer from the config dict. Implement these for custom layers to enable serialization. Without them, custom layers won't be compatible with `model.save()`/`load_model()`.
**Code:**
```python
import tensorflow as tf
class MyDense(tf.keras.layers.Layer):
    def __init__(self, units, **kwargs):
        super().__init__(**kwargs)
        self.units = units
        self.dense = tf.keras.layers.Dense(units)
    def call(self, x):
        return self.dense(x)
    def get_config(self):                       # serialize the layer config
        config = super().get_config()
        config.update({'units': self.units})
        return config
    @classmethod
    def from_config(cls, config):               # rebuild from the config dict
        return cls(**config)

layer = MyDense(8)
rebuilt = MyDense.from_config(layer.get_config())
print(rebuilt.units)   # 8  (enables save()/load_model() round-trips)
```

## Q93: How do you create a custom training step in Keras?
**A:** Override `train_step()` in a custom model: ```python
class MyModel(tf.keras.Model):
    def train_step(self, data):
        x, y = data
        with tf.GradientTape() as tape:
            preds = self(x, training=True)
            loss = self.compiled_loss(y, preds)
        grads = tape.gradient(loss, self.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.trainable_variables))
        self.compiled_metrics.update_state(y, preds)
        return {m.name: m.result() for m in self.metrics}
```
**Code:**
```python
import tensorflow as tf
class CustomModel(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.dense = tf.keras.layers.Dense(1)
    def train_step(self, data):
        x, y = data
        with tf.GradientTape() as tape:
            y_pred = self(x, training=True)
            loss = self.compiled_loss(y, y_pred)          # uses compile() loss
        grads = tape.gradient(loss, self.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.trainable_variables))
        self.compiled_metrics.update_state(y, y_pred)
        return {m.name: m.result() for m in self.metrics}

model = CustomModel()
model.compile(optimizer='adam', loss='mse', metrics=['mae'])
x = tf.random.normal((100, 4)); y = tf.random.normal((100, 1))
model.fit(x, y, epochs=3, validation_split=0.2, verbose=0)
```

## Q94: What is Pruning (magnitude pruning) and Structured Pruning?
**A:** Magnitude pruning removes individual weights with smallest absolute values — creates sparse models but irregular structure. Structured pruning removes entire neurons, channels, or blocks — creates models that work efficiently with standard hardware. The TF Model Optimization Toolkit (TFMOT) supports both approaches.
**Code:**
```python
import tensorflow as tf
import tensorflow_model_optimization as tfmot   # pip install tensorflow-model-optimization

# Magnitude pruning: zeros out the smallest individual weights
pruned = tfmot.sparsity.keras.prune_low_magnitude(
    tf.keras.layers.Dense(16, input_shape=(8,)),
    tfmot.sparsity.keras.PolynomialDecay(0.3, 0.7,
                                         begin_step=0, end_step=1000))
print(pruned(tf.random.normal((2, 8))).shape)      # (2, 16)
print(len(list(pruned.prunable_weights)))          # 2 (kernel + bias wrapped)

model = tf.keras.Sequential([pruned])
model.compile(optimizer='adam', loss='mse')
x = tf.random.normal((100, 8)); y = tf.random.normal((100, 1))
model.fit(x, y, epochs=2, verbose=0,
          callbacks=[tfmot.sparsity.keras.UpdatePruningStep()])
```

## Q95: What is Knowledge Distillation?
**A:** Knowledge distillation trains a smaller "student" model to mimic a larger "teacher" model. The student learns from the teacher's soft probabilities (logits) rather than hard labels. The loss combines: distillation loss (KL divergence between student and teacher outputs) and student loss (cross-entropy with true labels). Reduces model size while retaining performance.
**Code:**
```python
import tensorflow as tf
teacher = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(8,)),
    tf.keras.layers.Dense(5)])
student = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation='relu', input_shape=(8,)),
    tf.keras.layers.Dense(5)])
temperature, alpha = 4.0, 0.5

def distillation_loss(y_true, y_pred, teacher_logits):
    hard = tf.keras.losses.CategoricalCrossentropy()(y_true, y_pred)
    soft = tf.keras.losses.KLDivergence()(
        tf.nn.softmax(teacher_logits / temperature),
        tf.nn.log_softmax(y_pred / temperature))
    return (1 - alpha) * hard + alpha * temperature ** 2 * soft

x = tf.random.normal((64, 8))
y = tf.one_hot(tf.random.uniform((64,), 0, 5, tf.int32), 5)
with tf.GradientTape() as tape:
    s_logits = student(x, training=True)
    t_logits = teacher(x, training=False)          # teacher is frozen
    loss = distillation_loss(y, tf.nn.softmax(s_logits), t_logits)
grads = tape.gradient(loss, student.trainable_variables)
tf.keras.optimizers.Adam().apply_gradients(
    zip(grads, student.trainable_variables))
```

## Q96: What are the common Pitfalls in TensorFlow/Keras?
**A:** Common issues: not normalizing input data, wrong loss function for the task, learning rate too high/low, insufficient data augmentation, not shuffling training data, overfitting (too many parameters), incompatible shapes, not using `validation_split`/`validation_data`, ignoring class imbalance, and not monitoring for overfitting.
**Code:**
```python
import tensorflow as tf
# Practices that avoid the usual pitfalls: normalize inputs, pick the right
# loss, regularize, shuffle, and hold out a validation split.
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(8,)),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(1, activation='sigmoid'),
])
model.compile(optimizer=tf.keras.optimizers.Adam(1e-3),
              loss='binary_crossentropy',          # correct loss for the task
              metrics=['accuracy'])
x = tf.random.uniform((1000, 8))
y = tf.cast(tf.random.uniform((1000, 1)) > 0.5, tf.float32)
ds = tf.data.Dataset.from_tensor_slices((x, y)).shuffle(1000).batch(64)
val = tf.data.Dataset.from_tensor_slices((x[:200], y[:200])).batch(64)
model.fit(ds, epochs=3, validation_data=val, verbose=0)
```

## Q97: What is the difference between `tf.keras` and standalone Keras?
**A:** `tf.keras` is TensorFlow's implementation of the Keras API (v2 Keras). Standalone Keras (Keras 3) is framework-agnostic, supporting TensorFlow, JAX, and PyTorch backends. Keras 3 allows switching backends via `os.environ["KERAS_BACKEND"]="jax"`. Both share the same API design but Keras 3 is more portable.
**Code:**
```python
import tensorflow as tf
from tensorflow import keras as tf_keras        # Keras inside TF (v2 API)
print(tf.__version__, tf_keras.__version__)

import os
os.environ['KERAS_BACKEND'] = 'jax'             # Keras 3 backend switch
from keras import backend as K
print(K.backend())                              # 'jax' (or 'tensorflow'/'torch')
```

## Q98: How do you benchmark TensorFlow model performance?
**A:** Methods: `model.evaluate()` for standard metrics, TensorFlow profiling (TensorBoard profiling tab), `tf.test.Benchmark` for custom benchmarks, timing individual operations with `tf.timestamp()`, using `%timeit` in notebooks, measuring throughput (samples/sec), and monitoring GPU utilization.
**Code:**
```python
import tensorflow as tf
import time
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(64,)),
    tf.keras.layers.Dense(1)])
model.compile(optimizer='adam', loss='mse')
x = tf.random.normal((10000, 64)); y = tf.random.normal((10000, 1))

start = time.perf_counter()
model.fit(x, y, batch_size=128, epochs=3, verbose=0)
elapsed = time.perf_counter() - start
print(f'{3 * len(x) / elapsed:.0f} samples/sec')   # training throughput

ev = model.evaluate(x[:1000], y[:1000], verbose=0)
print(ev)   # [loss, ...] standard eval metrics
```

## Q99: What is the Hub (TF Hub)?
**A:** TF Hub is a repository of reusable ML modules. Provides pre-trained models for: image classification, text embeddings, object detection, and more. Models are versioned, documented, and ready to use as Keras layers: `hub_layer = hub.KerasLayer("https://tfhub.dev/google/nnlm-en-dim128/2")`. Simplifies transfer learning.
**Code:**
```python
import tensorflow as tf
import tensorflow_hub as hub   # pip install tensorflow-hub
model = tf.keras.Sequential([
    hub.KerasLayer('https://tfhub.dev/google/nnlm-en-dim128/2',
                   trainable=False),              # pre-trained text embedding
    tf.keras.layers.Dense(2, activation='softmax'),
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
print(model(['this sentence is positive',
             'this one is negative']).shape)   # (2, 2), uses the hub layer
```

## Q100: What are the latest developments in TensorFlow (2025-2026)?
**A:** Key developments: 1) Keras 3 with multi-backend (JAX, PyTorch, TF), 2) Improved JIT compilation with XLA, 3) Better large language model support (KerasNLP, model parallelism), 4) TensorFlow Decision Forests for tree-based models, 5) TFLite for on-device LLM inference, 6) TensorFlow Quantum for quantum ML, 7) JAX integration path, 8) Enhanced distributed training performance.
**Code:**
```python
import os
os.environ['KERAS_BACKEND'] = 'jax'   # must be set before importing keras
import tensorflow as tf
import keras
print(tf.__version__, keras.__version__)            # Keras 3 multi-backend
print('keras backend:', keras.backend.backend())    # e.g. jax

# XLA JIT compilation for tf.function graphs on accelerators
@tf.function(jit_compile=True)
def matmul(a, b):
    return tf.linalg.matmul(a, b)
print(matmul(tf.random.normal((32, 32)),
             tf.random.normal((32, 32))).shape)     # (32, 32)
```