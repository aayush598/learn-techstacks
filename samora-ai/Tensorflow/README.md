# TensorFlow / Keras Interview Questions and Answers

## Q1: What is TensorFlow?
**A:** TensorFlow is an open-source machine learning framework developed by Google for building, training, and deploying ML models. It supports deep learning, numerical computation using data flow graphs, and runs on CPU, GPU, and TPU. TensorFlow provides both high-level APIs (Keras) and low-level operations for maximum flexibility.

## Q2: What is Keras and how does it relate to TensorFlow?
**A:** Keras is a high-level neural networks API that provides a user-friendly interface for building and training models. Since TensorFlow 2.0, Keras is the official high-level API (`tf.keras`). It offers: Sequential API (linear stack of layers), Functional API (complex topologies), and Model subclassing (custom logic).

## Q3: What is a Tensor in TensorFlow?
**A:** A tensor is a multi-dimensional array — the fundamental data unit in TensorFlow. Rank 0 (scalar), Rank 1 (vector), Rank 2 (matrix), Rank 3+ (higher-dimensional). Tensors have: `dtype` (data type like float32, int32), `shape` (size of each dimension), and `device` (where allocated). Unlike NumPy arrays, tensors can run on GPUs and are immutable.

## Q4: What is eager execution in TensorFlow?
**A:** Eager execution (default in TF 2.x) evaluates operations immediately when called, returning concrete values without building a computational graph first. This makes debugging easier and code more pythonic. You can mix eager execution with `tf.function` for performance — use `@tf.function` decorator to compile functions into graphs.

## Q5: What is `tf.function` and how does it work?
**A:** `@tf.function` decorator compiles a Python function into a TensorFlow graph for performance optimization. On first call, it traces the function and creates a graph. Subsequent calls execute the cached graph. Benefits: graph optimizations (constant folding, op fusion), XLA compilation, and execution on accelerators. Not all Python code is supported — only TF operations.

## Q6: What is the difference between `tf.constant`, `tf.Variable`, and `tf.Tensor`?
**A:** `tf.Tensor` is the base type — immutable, created from operations. `tf.constant` is a tensor with a fixed value, immutable, and can be stored in the graph definition. `tf.Variable` is mutable — used for model parameters (weights, biases). Variables must be explicitly initialized and their values persist across `tf.function` calls.

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

## Q8: What is the Functional API in Keras?
**A:** The Functional API allows building complex models with non-linear topologies: multi-input, multi-output, shared layers, and residual connections. Instead of stacking layers sequentially, you define layers as callable functions: `x = Dense(64, activation='relu')(input)`. Useful for branch networks, siamese networks, and models with skip connections.

## Q9: What is Model subclassing in Keras?
**A:** Model subclassing involves extending `tf.keras.Model` and implementing the `call()` method. Gives full control over forward pass logic, including loops, conditionals, and custom operations. Example: `class MyModel(tf.keras.Model): def __init__(self): super().__init__(); self.dense = Dense(10); def call(self, x): return self.dense(x)`.

## Q10: What are the advantages and disadvantages of each Keras API?
**A:** Sequential: simplest, good for linear stacks, limited flexibility. Functional: moderate complexity, supports branching/sharing, good for most projects. Subclassing: most flexible, supports custom logic, harder to debug, not serializable by default. Recommendation: use Sequential for simple models, Functional for multi-branch, subclass for research.

## Q11: What is the `compile` step in Keras?
**A:** `model.compile()` configures the model for training. Parameters: `optimizer` (adam, sgd, rmsprop), `loss` (mse, categorical_crossentropy, binary_crossentropy), `metrics` (accuracy, precision, recall, AUC). This is where you define the learning process before calling `fit()`. You can also compile with custom losses and metrics.

## Q12: What optimizers are available in TensorFlow?
**A:** Common optimizers: `SGD` (with/without momentum), `Adam` (adaptive moment estimation, generally recommended), `RMSprop`, `Adagrad`, `Adadelta`, `AdamW` (Adam with weight decay), `Nadam` (Adam with Nesterov). Adam is the default choice for most deep learning tasks due to adaptive learning rates and good convergence.

## Q13: What is the difference between `SGD` and `Adam`?
**A:** SGD (Stochastic Gradient Descent) uses a single learning rate, requires manual scheduling, can get stuck in local minima, but generalizes better in some cases. Adam uses adaptive learning rates per parameter, momentum, bias correction, converges faster, and requires less tuning. Adam is safer for starting projects; SGD + momentum with LR scheduling may give better final performance.

## Q14: What loss functions does Keras provide?
**A:** Regression: `MeanSquaredError` (MSE), `MeanAbsoluteError` (MAE), `Huber` (robust to outliers). Classification: `CategoricalCrossentropy` (multi-class, one-hot labels), `SparseCategoricalCrossentropy` (multi-class, integer labels), `BinaryCrossentropy` (binary). Others: `KLDivergence`, `CosineSimilarity`, `Hinge`, `Poisson`.

## Q15: What is the difference between `categorical_crossentropy` and `sparse_categorical_crossentropy`?
**A:** `categorical_crossentropy` expects labels as one-hot encoded vectors (e.g., [0, 1, 0]). `sparse_categorical_crossentropy` expects labels as integers (e.g., 1) and computes the same loss without requiring one-hot encoding. Sparse version is more memory efficient for large numbers of classes.

## Q16: What is the `fit()` method and what are its key parameters?
**A:** `model.fit()` trains the model. Key params: `x` (training data), `y` (labels), `batch_size` (samples per gradient update), `epochs` (passes over data), `validation_data`/`validation_split` (eval set), `callbacks` (list of callback objects), `shuffle` (shuffle per epoch), `class_weight` (handle imbalance), `verbose` (0/1/2).

## Q17: What is the difference between an epoch, batch, and iteration?
**A:** Epoch: one complete pass through the entire training dataset. Batch: a subset of training samples processed before updating weights. Iteration: one batch processed (number of iterations per epoch = total samples / batch size). Example: 1000 samples, batch size 100 = 10 iterations per epoch.

## Q18: What is a callback in Keras?
**A:** Callbacks are objects that perform actions at various stages of training (start/end of epoch, batch, training). Built-in: `ModelCheckpoint` (save weights), `EarlyStopping` (stop when metric stops improving), `ReduceLROnPlateau` (reduce LR on plateau), `TensorBoard` (logging), `CSVLogger`, `LearningRateScheduler`. Custom callbacks can extend `tf.keras.callbacks.Callback`.

## Q19: What is EarlyStopping and how do you configure it?
**A:** `EarlyStopping` stops training when a monitored metric stops improving. Params: `monitor` (e.g., 'val_loss'), `patience` (epochs with no improvement before stopping), `min_delta` (minimum change considered improvement), `restore_best_weights` (revert to best epoch), `mode` ('auto', 'min', 'max'). Prevents overfitting and saves time.

## Q20: What is ModelCheckpoint?
**A:** `ModelCheckpoint` saves model weights during training. Params: `filepath` (path to save), `monitor` (metric to track), `save_best_only` (only save when metric improves), `save_weights_only` (vs. full model), `mode` ('min'/'max'). Ensures you don't lose progress and can recover the best model.

## Q21: What is the difference between model.save() and model.save_weights()?
**A:** `model.save()` saves the entire model: architecture, weights, training config, optimizer state. Creates a SavedModel directory (or .h5 file). `model.save_weights()` saves only the weight values (smaller file). To reconstruct a model from weights, you need the architecture code or a separate config. Full save is preferred for deployment.

## Q22: What is the SavedModel format?
**A:** SavedModel is TensorFlow's standard serialization format. It contains: `saved_model.pb` (graph definition, signature), `variables/` (weight values), `assets/` (external files). It's self-contained, language-neutral, and supports serving via TensorFlow Serving. Use `tf.saved_model.save()` or `model.export()` (Keras 3).

## Q23: What is TensorFlow Serving?
**A:** TensorFlow Serving is a production-serving system for ML models. It handles: model versioning, automatic A/B testing, batching requests, gRPC and REST APIs, and model reloading without downtime. Deploy SavedModel format. Can be extended with custom ops and pre/post-processing pipelines.

## Q24: What is TensorFlow Lite?
**A:** TensorFlow Lite (TFLite) is a lightweight solution for deploying models on mobile, embedded, and edge devices. It converts TF models to `.tflite` format, optimizes for latency and size (quantization, pruning), and runs on Android, iOS, microcontrollers, and Linux. Minimal binary size and hardware acceleration via GPU/Neural Networks API.

## Q25: What is TensorFlow.js?
**A:** TensorFlow.js enables ML model training and inference in the browser and Node.js. Supports: loading pre-trained models (TF Hub, Keras), transfer learning in the browser, and training from scratch. Uses WebGL/WebGPU for GPU acceleration. Use cases: client-side image classification, pose estimation, sentiment analysis.

## Q26: What is the difference between `tf.data.Dataset` and NumPy arrays for model input?
**A:** `tf.data.Dataset` provides: efficient data pipelining (parallel loading, prefetching, caching), on-the-fly preprocessing, shuffling, batching, and infinite data generation. It integrates with TF's execution pipelines. NumPy arrays must be loaded entirely in memory. For large datasets, use `tf.data` for performance and memory efficiency.

## Q27: How do you create a tf.data pipeline?
**A:** ```python
dataset = tf.data.Dataset.from_tensor_slices((x, y))
dataset = dataset.shuffle(1000).batch(32).prefetch(tf.data.AUTOTUNE)
dataset = dataset.map(preprocess_fn, num_parallel_calls=tf.data.AUTOTUNE)
```
Key methods: `map` (apply function), `filter` (select samples), `batch` (group), `shuffle` (randomize), `prefetch` (overlap preparation and execution), `cache` (cache in memory/disk), `repeat` (loop indefinitely).

## Q28: What is prefetch in tf.data?
**A:** `dataset.prefetch(tf.data.AUTOTUNE)` overlaps data preprocessing and model execution. While the model trains on batch N, the CPU prepares batch N+1. This reduces idle time and improves throughput. `AUTOTUNE` lets TF dynamically tune the buffer size. Prefetch is typically the last transformation in a pipeline.

## Q29: What is a convolutional layer (Conv2D)?
**A:** `Conv2D` is a layer that applies convolution filters to input images. Parameters: `filters` (number of output channels), `kernel_size` (filter size, e.g., 3x3), `strides`, `padding` ('valid' or 'same'), `activation`, `dilation_rate`. Convolution preserves spatial structure, learns local patterns, and uses parameter sharing (same filter across image).

## Q30: What is pooling in CNNs?
**A:** Pooling reduces spatial dimensions and provides translation invariance. `MaxPooling2D` takes the maximum value in each window — preserves sharp features. `AveragePooling2D` takes the average — smoother. `GlobalAveragePooling2D` reduces each feature map to a single value — used before classification layers. Pooling reduces parameters and computation.

## Q31: What is the difference between 'valid' and 'same' padding?
**A:** 'valid' padding: no padding, output size shrinks (e.g., 32x32 input + 3x3 filter = 30x30 output). 'same' padding: pad with zeros so output size equals input size (rounded up). 'same' is typically used to preserve spatial dimensions, especially in deep networks with many conv layers.

## Q32: What is batch normalization?
**A:** `BatchNormalization` normalizes layer outputs by mean and variance across the batch, then applies learnable scale (gamma) and shift (beta). Benefits: faster convergence (allows higher learning rates), reduces internal covariate shift, provides regularization, reduces sensitivity to initialization. Applied before or after activation depending on convention.

## Q33: What is dropout?
**A:** `Dropout` randomly sets a fraction of input units to 0 at each training step. Prevents co-adaptation of neurons and acts as regularization. Rate (0.2–0.5) controls fraction dropped. During inference, dropout is disabled and outputs are scaled. `Dropout` is effective in fully-connected layers; spatial dropout is used for conv layers.

## Q34: What is a recurrent layer (LSTM, GRU)?
**A:** Recurrent layers process sequential data (text, time series, audio). `LSTM` (Long Short-Term Memory) uses input/forget/output gates and cell state to capture long-range dependencies. `GRU` (Gated Recurrent Unit) is simpler (two gates, no cell state). Both handle vanishing gradient problems in vanilla RNNs.

## Q35: What is the difference between LSTM and GRU?
**A:** LSTM has three gates (input, forget, output) and a separate cell state — more expressive, more parameters, can capture longer dependencies. GRU has two gates (reset, update) and no cell state — simpler, faster, fewer parameters. GRU often performs similarly to LSTM with less computation. Use LSTM for very long sequences.

## Q36: What is an embedding layer?
**A:** `Embedding` layer maps discrete tokens (words, categories) to dense vector representations. Input: integer indices. Output: dense vectors. Parameters: `input_dim` (vocabulary size), `output_dim` (embedding size). Embeddings are learned during training. Pre-trained embeddings (Word2Vec, GloVe) can be loaded. Useful for: NLP, recommendation systems, categorical features.

## Q37: What is transfer learning?
**A:** Transfer learning uses a pre-trained model (trained on a large dataset like ImageNet) as a starting point for a new task. Approaches: feature extraction (freeze pre-trained layers, train new classifier on top) and fine-tuning (unfreeze some layers and train with a low learning rate). Saves time, requires less data, often performs better.

## Q38: How do you implement transfer learning with Keras?
**A:** ```python
base_model = tf.keras.applications.ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Freeze base
model = tf.keras.Sequential([base_model, GlobalAveragePooling2D(), Dense(10, activation='softmax')])
model.compile(optimizer='adam', loss='categorical_crossentropy')
```
After initial training, optionally unfreeze layers and fine-tune with a lower learning rate.

## Q39: What are common pre-trained models in Keras?
**A:** `tf.keras.applications` includes: ResNet50/101/152, VGG16/19, InceptionV3, Xception, MobileNetV2/V3 (lightweight), EfficientNetB0-B7 (state-of-the-art efficiency), DenseNet121/169/201, NASNetLarge/Mobile. Each has different trade-offs between accuracy, speed, and size.

## Q40: What is data augmentation in Keras?
**A:** `tf.keras.layers.Random*` and `tf.keras.preprocessing.image.ImageDataGenerator` generate training variations to improve generalization. Augmentations: rotation, zoom, flip, shift, brightness, contrast, shear. In TF 2.x, use Keras preprocessing layers: `RandomFlip`, `RandomRotation`, `RandomZoom`, `RandomContrast`, `Rescaling`. Applied on-the-fly during training.

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

## Q42: What is the Adam optimizer and how does it work?
**A:** Adam (Adaptive Moment Estimation) combines: 1) Momentum — accumulates past gradients (like SGD with momentum), 2) RMSprop — adaptive learning rates per parameter. It maintains exponentially decaying averages of past gradients (m) and squared gradients (v), with bias correction. Default LR: 0.001. Robust to sparse gradients, works well out of the box.

## Q43: What is gradient clipping?
**A:** Gradient clipping prevents exploding gradients by capping gradient values. Methods: clip by value (`clipvalue=1.0` — clip each gradient component to [-1, 1]) and clip by norm (`clipnorm=1.0` — scale down if gradient norm exceeds 1). Essential for RNNs, transformers, and deep networks. Configure in optimizer: `Adam(clipnorm=1.0)`.

## Q44: What is the learning rate and how do you schedule it?
**A:** Learning rate controls step size during gradient descent. Scheduling strategies: step decay (reduce by factor every N epochs), exponential decay (`ExponentialDecay`), cosine decay (`CosineDecay`), ReduceLROnPlateau (reduce when metric plateaus), warmup (gradually increase from small to target LR). Keras provides `LearningRateScheduler` and `ReduceLROnPlateau` callbacks.

## Q45: What is overfitting and how do you prevent it?
**A:** Overfitting occurs when a model learns training data too well (including noise) but fails to generalize. Prevention: more training data, data augmentation, simpler architectures, regularization (L1/L2), dropout, batch normalization, early stopping, cross-validation, and reducing model capacity.

## Q46: What is the difference between L1 and L2 regularization?
**A:** L1 (Lasso) adds absolute weight values to the loss — encourages sparsity (some weights become exactly zero), useful for feature selection. L2 (Ridge) adds squared weight values — encourages small weights but not zero, keeps all features. L2 is more common in deep learning. Apply via `kernel_regularizer=tf.keras.regularizers.l2(0.01)`.

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

## Q48: What is `tf.GradientTape`?
**A:** `tf.GradientTape` records operations for automatic differentiation. Inside the `with` block, all trainable operations are recorded. `tape.gradient(loss, variables)` computes gradients. Supports: nested tapes (higher-order gradients), persistent tapes (multiple gradient calls), and watching non-trainable variables.

## Q49: How do you use GPUs with TensorFlow?
**A:** TF automatically uses available GPUs. Control GPU usage: `os.environ['CUDA_VISIBLE_DEVICES']='0'` to restrict visible GPUs. `tf.config.list_physical_devices('GPU')` to list. `tf.config.experimental.set_memory_growth(device, True)` for dynamic memory allocation. `tf.distribute.MirroredStrategy` for multi-GPU training.

## Q50: What is distributed training in TensorFlow?
**A:** `tf.distribute.Strategy` abstracts distributed training. Strategies: `MirroredStrategy` (sync SGD, single-host multi-GPU), `MultiWorkerMirroredStrategy` (multi-host), `TPUStrategy` (TPU pods), `ParameterServerStrategy` (async, parameter servers). MirroredStrategy copies model to each GPU, computes gradients in parallel, synchronizes via all-reduce.

## Q51: What is mixed precision training?
**A:** Mixed precision uses float16 (half precision) for most operations while keeping float32 for critical parts (loss scaling, weight updates). Benefits: ~2x speedup on compatible GPUs (Tesla V100, A100, RTX series), 50% less memory. Enable with: `tf.keras.mixed_precision.set_global_policy('mixed_float16')` and add loss scaling.

## Q52: What is the `tf.keras.metrics` module?
**A:** Provides metric classes for evaluation: `Accuracy`, `Precision`, `Recall`, `AUC`, `MeanSquaredError`, `MeanAbsoluteError`, `TopKCategoricalAccuracy`, etc. Metrics can be updated per batch and queried at epoch end. For custom metrics, extend `tf.keras.metrics.Metric` and implement `update_state()`, `result()`, `reset_state()`.

## Q53: How do you create a custom layer in Keras?
**A:** Extend `tf.keras.layers.Layer`: implement `__init__` (define sublayers), `build()` (create weights, called on first use with input shape), `call()` (forward pass logic). Optionally implement `get_config()` for serialization. Example: define a custom activation or a specialized computation layer.

## Q54: What is the `call()` method in Keras layers?
**A:** `call()` defines the forward pass computation. Parameters: `inputs` (tensor), `training` (bool — to distinguish train vs inference behavior, e.g., for dropout/batchnorm), `mask` (for masking sequences). The method must return one tensor or a list of tensors.

## Q55: How do you create a custom loss function in Keras?
**A:** Define a function that takes `y_true` and `y_pred` and returns a scalar loss: `def custom_loss(y_true, y_pred): return tf.reduce_mean(tf.square(y_true - y_pred))`. Pass to `compile(loss=custom_loss)`. For stateful losses, subclass `tf.keras.losses.Loss` with `call()` method.

## Q56: What are callbacks and how do you create a custom callback?
**A:** Custom callbacks extend `tf.keras.callbacks.Callback` and override methods: `on_epoch_begin/end`, `on_batch_begin/end`, `on_train_begin/end`, etc. Access `self.model` for the model, `self.model.history` for metrics, `self.params` for training parameters. Useful for custom logging, model manipulation, or external integrations.

## Q57: What is the TensorBoard callback?
**A:** `TensorBoard` callback logs metrics, histograms, graph, and embeddings for visualization in TensorBoard. Enable: `callbacks=[TensorBoard(log_dir='./logs')]`. View with: `tensorboard --logdir ./logs`. Visualizes: training metrics, model graph, layer histograms, image summaries, embeddings, and profiling data.

## Q58: What are Keras applications?
**A:** `tf.keras.applications` provides pre-trained model architectures with pre-trained weights. Common models: ResNet, VGG, Inception, MobileNet, EfficientNet, DenseNet. Each provides: `preprocess_input()` (proper input scaling), `decode_predictions()` (class label decoding), and configurable `include_top` (with/without classifier head).

## Q59: What is the Functional API use case for multi-input models?
**A:** Multi-input models take multiple independent inputs that are combined later: ```python
input_a = Input(shape=(32,))
input_b = Input(shape=(64,))
merged = Concatenate()([Dense(16)(input_a), Dense(32)(input_b)])
output = Dense(1, activation='sigmoid')(merged)
model = Model(inputs=[input_a, input_b], outputs=output)
```
Used for: multi-modal data, ensemble-like architectures, siamese networks.

## Q60: What is a siamese network in Keras?
**A:** A siamese network uses shared weights between two subnetworks to compare inputs. Built with Functional API: same Dense layers applied to two inputs via shared layers. Output is a similarity score (e.g., cosine distance). Used for: face verification, signature comparison, similarity learning, one-shot learning.

## Q61: How do you handle imbalanced datasets?
**A:** Approaches: 1) `class_weight` in `model.fit()` — higher weight for minority classes, 2) Oversampling (duplicate minority), 3) Undersampling (reduce majority), 4) SMOTE (synthetic samples), 5) Focal Loss (focus on hard examples), 6) Weighted loss function, 7) Stratified splitting for validation.

## Q62: What is focal loss?
**A:** Focal Loss down-weights easy examples and focuses on hard, misclassified examples. It adds a modulating factor `(1 - p_t)^γ` to the cross-entropy loss. When γ=0, focal loss = cross-entropy. Higher γ (e.g., 2) focuses more on hard examples. Commonly used in object detection (RetinaNet) and severe class imbalance.

## Q63: How do you perform hyperparameter tuning in TensorFlow?
**A:** Methods: 1) Grid search (exhaustive combinations), 2) Random search (random combinations — more efficient), 3) Bayesian optimization (Keras Tuner), 4) Early stopping-based methods (Hyperband). Keras Tuner provides: `RandomSearch`, `Hyperband`, `BayesianOptimization` with intuitive API for defining search spaces.

## Q64: What is the Keras Tuner?
**A:** Keras Tuner is a library for hyperparameter tuning. Define a model-building function with `hp.Choice`, `hp.Int`, `hp.Float` for searchable parameters. Run: `tuner = RandomSearch(build_model, objective='val_accuracy', max_trials=100)` then `tuner.search(x_train, y_train)`. Supports: search algorithms, distribution strategies, and callback integration.

## Q65: What is the difference between `model.fit()` and `model.fit_generator()`?
**A:** `model.fit()` accepts data as arrays or `tf.data.Dataset`. `model.fit_generator()` (deprecated in TF 2.1+) accepted Python generators for data loading. In TF 2.x, always use `model.fit()` with `tf.data.Dataset` or arrays. The unified API handles both cases efficiently.

## Q66: How does TensorFlow handle model serialization for serving?
**A:** `model.save('path')` creates a SavedModel. TensorFlow Serving loads SavedModels and exposes gRPC/REST endpoints. For mobile: convert to TFLite. For JS: convert to TFJS format. For cloud: deploy to Vertex AI, Sagemaker, or custom containers with TF Serving.

## Q67: What is ONNX and can TensorFlow export to it?
**A:** ONNX (Open Neural Network Exchange) is an open format for ML models. TF models can be converted to ONNX via `tf2onnx` library. Benefits: interoperability with PyTorch, ONNX Runtime optimization, deployment on edge devices. However, some TF ops may not have ONNX equivalents, requiring workarounds.

## Q68: What is TensorFlow Extended (TFX)?
**A:** TFX is a production ML pipeline platform. Components: ExampleGen (data ingestion), StatisticsGen (data analysis), SchemaGen (schema inference), Transform (feature engineering), Trainer (model training), Tuner (hyperparameter tuning), Evaluator (model validation), Pusher (deployment). Uses Apache Beam for distributed pipeline execution.

## Q69: What is TensorFlow Data Validation (TFDV)?
**A:** TFDV analyzes and validates data to detect anomalies. Features: schema inference, statistics computation, data drift detection, skew detection (train vs serving), and anomaly visualization. Helps catch data quality issues before they affect model performance in production.

## Q70: What is TensorFlow Model Analysis (TFMA)?
**A:** TFMA evaluates models on large datasets and provides detailed slicing and fairness analysis. Computes metrics across slices (e.g., accuracy by age group, gender). Detects model bias and fairness issues. Integrates with TFX for continuous evaluation.

## Q71: What are Keras callbacks for model checkpointing?
**A:** `ModelCheckpoint` saves weights during training. `BackupAndRestore` enables recovery from interruptions. `EarlyStopping` halts training when no improvement. `ReduceLROnPlateau` adapts learning rate. `TerminateOnNaN` stops on NaN loss. `CSVLogger` logs metrics to CSV. `ProgbarLogger` displays progress.

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

## Q73: What is gradient accumulation?
**A:** Gradient accumulation simulates larger batch sizes by accumulating gradients over multiple forward passes before updating weights. Used when GPU memory limits batch size. Pseudocode: loop N batches, sum gradients, then apply optimizer step. Not built into standard Keras — requires custom training loop.

## Q74: What is quantization in TensorFlow Lite?
**A:** Quantization reduces model precision from float32 to int8 or float16. Types: post-training quantization (convert after training, easiest), quantization-aware training (simulate quantization during training, best accuracy). Benefits: 4x smaller model, 2-4x faster on compatible hardware, lower power consumption.

## Q75: What is pruning in TensorFlow?
**A:** Pruning removes unnecessary weights (sets them to zero) to reduce model size. The `tfmot` (TensorFlow Model Optimization Toolkit) provides: weight pruning (remove by magnitude), structured pruning (remove entire neurons/channels). Combined with quantization for significant size reduction with minimal accuracy loss.

## Q76: What is the KerasCV library?
**A:** KerasCV is a library for computer vision tasks built on Keras. Provides: model presets (YOLOV8, RetinaNet, Mask R-CNN), data augmentation, preprocessing, and evaluation metrics. Simplifies building: object detection, image segmentation, image classification pipelines with consistent API.

## Q77: What is the KerasNLP library?
**A:** KerasNLP is a library for NLP tasks on Keras. Provides: model presets (BERT, GPT-2, RoBERTa, T5, OPT), tokenizers (WordPiece, BPE, SentencePiece), and preprocessing layers. Supports: text classification, sequence labeling, question answering, causal LM, and masked LM.

## Q78: How do you use BERT with KerasNLP?
**A:** ```python
import keras_nlp
classifier = keras_nlp.models.BertClassifier.from_preset("bert_base_uncased", num_classes=2)
classifier.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
classifier.fit(x_train, y_train, epochs=3)
```
KerasNLP handles tokenization, preprocessing, and model architecture automatically.

## Q79: What is a Transformer model?
**A:** The Transformer (Vaswani et al., 2017) uses self-attention instead of recurrence for sequence processing. Key components: multi-head attention (captures relationships between all positions), feed-forward networks, positional encoding, layer normalization, and residual connections. Foundation of BERT, GPT, T5, and modern NLP.

## Q80: What is self-attention in Transformers?
**A:** Self-attention computes weighted sums of all elements in a sequence, where weights are based on pairwise compatibility. Each element has: Query (Q), Key (K), Value (V). Attention scores = softmax(Q·K^T/√d_k)·V. Multi-head attention runs multiple attention layers in parallel, capturing different relationship types.

## Q81: What is the difference between TensorFlow 1.x and 2.x?
**A:** TF 2.x: eager execution by default, Keras as high-level API, `tf.function` for graphs, simplified APIs (no more `tf.Session`, `tf.placeholder`), tighter integration with Python, eager debugging, and removal of deprecated APIs. TF 1.x used static graphs — define-then-run paradigm.

## Q82: What is Graph mode vs Eager mode?
**A:** Eager mode (default in TF 2.x): operations execute immediately, results are concrete tensors, easy debugging. Graph mode: builds a computational graph first (via `tf.function`), then executes the entire graph for better optimization, portability, and deployment. Graph mode is faster for repeated executions.

## Q83: How do you debug TensorFlow models?
**A:** Tools: eager execution (print tensors directly), `tf.print` (works in graphs), TensorBoard (visualize metrics/graphs), `tf.debugging` (asserts, check numeric), `tf.config.run_functions_eagerly(True)` (disable graph for debugging), Python debugger (pdb/ipdb) — works in eager mode.

## Q84: How do you handle NaN loss during training?
**A:** Causes: exploding gradients, learning rate too high, inappropriate initialization, division by zero, log(0) in loss. Fixes: gradient clipping, lower learning rate, batch normalization, proper weight initialization, label smoothing, data normalization, check for NaN in predictions. Use `TerminateOnNaN` callback.

## Q85: What is weight initialization and why does it matter?
**A:** Weight initialization sets initial values for model parameters. Bad initialization causes: vanishing/exploding gradients, slow convergence. Common methods: Glorot/Xavier (tanh activation), He (ReLU), LeCun (SELU). Keras uses sensible defaults (Glorot uniform for Dense, He normal for Conv2D). Proper initialization is critical for deep networks.

## Q86: What is the difference between `kernel_initializer` and `bias_initializer`?
**A:** `kernel_initializer` sets the initial weight matrix values. `bias_initializer` sets initial bias vector values (default is zeros). Both are layer parameters. Common initializers: 'glorot_uniform', 'he_normal', 'zeros', 'ones', 'random_normal', 'random_uniform', 'orthogonal'.

## Q87: What is the `@tf.function` decorator and AutoGraph?
**A:** `@tf.function` compiles Python functions to TF graphs. AutoGraph converts Python control flow (if/while/for) into TF graph operations. Limitations: Python side effects (print, list append) work differently, dynamic data structures may not trace correctly. Use `tf.print()` and `tf.TensorArray` for graph-compatible alternatives.

## Q88: How do you handle variable-length sequences in Keras?
**A:** Use `tf.keras.layers.Masking` or `Embedding(mask_zero=True)` to ignore padding. Pad sequences to same length with `tf.keras.preprocessing.sequence.pad_sequences()`. For RNNs, set `mask_zero=True` in Embedding — the RNN will skip masked timesteps.

## Q89: What is the `add_loss()` method in Keras?
**A:** `add_loss()` allows adding custom losses from within layers or models. Useful for: regularization losses (activation regularization), consistency losses, auxiliary losses. Accumulated losses are added to the model's total loss during `compile()`. Example: `self.add_loss(tf.reduce_mean(self.kernel ** 2))`.

## Q90: What are Keras metrics and how do you track them?
**A:** Metrics track model performance during training. Built-in: accuracy, precision, recall, AUC, MSE, MAE. Track via `model.compile(metrics=[...])`. Available in `model.history.history` after training. Custom metrics extend `tf.keras.metrics.Metric`. For multiple metrics, use list or dict (for multi-output models).

## Q91: How do you save and load Keras models?
**A:** Save: `model.save('path.keras')` (Keras v3 format, recommended) or `model.save('path.h5')` (HDF5 legacy). Load: `model = tf.keras.models.load_model('path.keras')`. For weights only: `model.save_weights('path.weights.h5')` and `model.load_weights('path.weights.h5')`. The full model includes architecture, weights, optimizer state, and compile config.

## Q92: What is `get_config()` and `from_config()` in Keras?
**A:** `get_config()` returns a dictionary of a layer/model's configuration (parameters). `from_config()` reconstructs the layer from the config dict. Implement these for custom layers to enable serialization. Without them, custom layers won't be compatible with `model.save()`/`load_model()`.

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

## Q94: What is Pruning (magnitude pruning) and Structured Pruning?
**A:** Magnitude pruning removes individual weights with smallest absolute values — creates sparse models but irregular structure. Structured pruning removes entire neurons, channels, or blocks — creates models that work efficiently with standard hardware. The TF Model Optimization Toolkit (TFMOT) supports both approaches.

## Q95: What is Knowledge Distillation?
**A:** Knowledge distillation trains a smaller "student" model to mimic a larger "teacher" model. The student learns from the teacher's soft probabilities (logits) rather than hard labels. The loss combines: distillation loss (KL divergence between student and teacher outputs) and student loss (cross-entropy with true labels). Reduces model size while retaining performance.

## Q96: What are the common Pitfalls in TensorFlow/Keras?
**A:** Common issues: not normalizing input data, wrong loss function for the task, learning rate too high/low, insufficient data augmentation, not shuffling training data, overfitting (too many parameters), incompatible shapes, not using `validation_split`/`validation_data`, ignoring class imbalance, and not monitoring for overfitting.

## Q97: What is the difference between `tf.keras` and standalone Keras?
**A:** `tf.keras` is TensorFlow's implementation of the Keras API (v2 Keras). Standalone Keras (Keras 3) is framework-agnostic, supporting TensorFlow, JAX, and PyTorch backends. Keras 3 allows switching backends via `os.environ["KERAS_BACKEND"]="jax"`. Both share the same API design but Keras 3 is more portable.

## Q98: How do you benchmark TensorFlow model performance?
**A:** Methods: `model.evaluate()` for standard metrics, TensorFlow profiling (TensorBoard profiling tab), `tf.test.Benchmark` for custom benchmarks, timing individual operations with `tf.timestamp()`, using `%timeit` in notebooks, measuring throughput (samples/sec), and monitoring GPU utilization.

## Q99: What is the Hub (TF Hub)?
**A:** TF Hub is a repository of reusable ML modules. Provides pre-trained models for: image classification, text embeddings, object detection, and more. Models are versioned, documented, and ready to use as Keras layers: `hub_layer = hub.KerasLayer("https://tfhub.dev/google/nnlm-en-dim128/2")`. Simplifies transfer learning.

## Q100: What are the latest developments in TensorFlow (2025-2026)?
**A:** Key developments: 1) Keras 3 with multi-backend (JAX, PyTorch, TF), 2) Improved JIT compilation with XLA, 3) Better large language model support (KerasNLP, model parallelism), 4) TensorFlow Decision Forests for tree-based models, 5) TFLite for on-device LLM inference, 6) TensorFlow Quantum for quantum ML, 7) JAX integration path, 8) Enhanced distributed training performance.
