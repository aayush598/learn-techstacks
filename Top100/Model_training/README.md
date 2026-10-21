# Model Training Interview Questions and Answers

## Q1: What is model training in machine learning?
**A:** Model training is the process of teaching a machine learning model to make predictions or decisions by exposing it to labeled or unlabeled data. During training, the model learns patterns and relationships in the data by adjusting its internal parameters to minimize a loss function.
**Code:**
```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=1000, n_features=20, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)              # training minimizes a loss function
print(model.score(X_test, y_test))
```

## Q2: What is the difference between supervised and unsupervised learning?
**A:** Supervised learning uses labeled data where input-output pairs are provided, and the model learns to map inputs to outputs. Unsupervised learning uses unlabeled data where the model discovers hidden patterns, groupings, or structures without explicit guidance.
**Code:**
```python
from sklearn.linear_model import LogisticRegression  # supervised
from sklearn.cluster import KMeans                  # unsupervised

# Supervised: labels y are available
clf = LogisticRegression().fit(X_train, y_train)

# Unsupervised: only X, no labels
kmeans = KMeans(n_clusters=3).fit(X_train)
print(kmeans.labels_)
```

## Q3: What is the training loop?
**A:** The training loop is the iterative process of: 1) Forward pass (compute predictions), 2) Calculate loss, 3) Backward pass (compute gradients), 4) Update model parameters using an optimizer. This repeats for each batch over multiple epochs.
**Code:**
```python
import torch

for epoch in range(10):
    for xb, yb in dataloader:
        pred = model(xb)                # 1) forward pass
        loss = criterion(pred, yb)      # 2) compute loss
        optimizer.zero_grad()
        loss.backward()                 # 3) backward pass (gradients)
        optimizer.step()                # 4) update parameters
```

## Q4: What are hyperparameters in model training?
**A:** Hyperparameters are configuration settings set before training begins that control the training process. Examples include learning rate, batch size, number of epochs, optimizer choice, number of layers, hidden units, dropout rate, and regularization strength.
**Code:**
```python
config = {
    "learning_rate": 1e-3,
    "batch_size": 32,
    "epochs": 50,
    "hidden_units": 128,
    "dropout": 0.3,
    "weight_decay": 1e-4,
}
model = MLP(hidden_units=config["hidden_units"], dropout=config["dropout"])
optimizer = torch.optim.Adam(model.parameters(), lr=config["learning_rate"], weight_decay=config["weight_decay"])
```

## Q5: What is the difference between parameters and hyperparameters?
**A:** Parameters are learned from data during training (weights, biases). Hyperparameters are set before training and control how training happens. Parameters are updated by the optimizer; hyperparameters are tuned by the practitioner.
**Code:**
```python
import torch.nn as nn

linear = nn.Linear(4, 2)
print(linear.weight)            # parameters: learned during training
print(linear.bias)              # parameters

lr, batch_size, epochs = 1e-3, 32, 50   # hyperparameters: chosen before training
```

## Q6: What is a loss function?
**A:** A loss function quantifies the difference between the model's predictions and the true values. It measures how well the model is performing. Common loss functions include mean squared error (regression), cross-entropy (classification), and Huber loss (robust regression).
**Code:**
```python
import torch.nn as nn

mse = nn.MSELoss()                     # regression
ce = nn.CrossEntropyLoss()             # classification
huber = nn.HuberLoss()                 # robust regression

pred, target = model(xb), yb
print("MSE:", mse(pred, target).item())
```

## Q7: What is gradient descent?
**A:** Gradient descent is an optimization algorithm that iteratively updates model parameters in the direction of the negative gradient of the loss function. The goal is to find parameter values that minimize the loss. The learning rate controls the step size.
**Code:**
```python
import torch

w = torch.tensor(2.0, requires_grad=True)
for _ in range(100):
    loss = (w - 5.0) ** 2               # minimize (w-5)^2
    loss.backward()
    with torch.no_grad():
        w -= 0.1 * w.grad               # step opposite the gradient
        w.grad = None
print(w.item())                         # -> ~5.0
```

## Q8: What are the variants of gradient descent?
**A:** The main variants are: Batch GD (uses entire dataset), Stochastic GD (SGD, uses one sample), and Mini-batch GD (uses a subset/batch). Mini-batch GD is most common as it balances computational efficiency with convergence stability.
**Code:**
```python
from torch.utils.data import DataLoader

# Mini-batch GD: iterate over batches of the dataset
loader = DataLoader(dataset, batch_size=64, shuffle=True)
for xb, yb in loader:
    loss = criterion(model(xb), yb)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

## Q9: What is the learning rate and why is it important?
**A:** The learning rate controls how much the model's parameters are adjusted during each update. Too high: training may diverge or oscillate. Too low: training is slow or may get stuck in local minima. Learning rate scheduling (decay, warmup, cyclical) can help.
**Code:**
```python
import torch.optim.lr_scheduler as S

optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
scheduler = S.StepLR(optimizer, step_size=10, gamma=0.1)  # decay by 0.1 every 10 epochs

for epoch in range(30):
    train_one_epoch()
    scheduler.step()
    print(optimizer.param_groups[0]['lr'])
```

## Q10: What are epochs and batches?
**A:** An epoch is one complete pass through the entire training dataset. A batch is a subset of the dataset processed before updating parameters. Iterations per epoch = total samples / batch size. Multiple epochs are typically needed for convergence.
**Code:**
```python
n_samples, batch_size = 1000, 100
iters_per_epoch = n_samples // batch_size          # 10 iterations == 1 epoch

for epoch in range(5):                             # 5 full passes over data
    for iteration in range(iters_per_epoch):
        xb = dataset_X[iteration * batch_size:(iteration + 1) * batch_size]
        yb = dataset_y[iteration * batch_size:(iteration + 1) * batch_size]
        optimizer.zero_grad()
        loss = criterion(model(xb), yb)
        loss.backward()
        optimizer.step()
```

## Q11: What is overfitting?
**A:** Overfitting occurs when a model learns the training data too well, including noise and irrelevant patterns, resulting in poor generalization to unseen data. Symptoms include high training accuracy but low validation/test accuracy.
**Code:**
```python
train_acc = evaluate(model, train_loader)   # e.g., 0.99
val_acc = evaluate(model, val_loader)       # e.g., 0.72
print(f"train={train_acc:.3f} val={val_acc:.3f}")   # large gap => overfitting
```

## Q12: How do you prevent overfitting?
**A:** Techniques include: regularization (L1, L2), dropout, early stopping, data augmentation, reducing model complexity, cross-validation, batch normalization, label smoothing, and using more training data.
**Code:**
```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(128, 256),
    nn.BatchNorm1d(256),          # batch normalization
    nn.ReLU(),
    nn.Dropout(0.5),              # dropout
    nn.Linear(256, 10),
)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)  # L2 regularization
```

## Q13: What is underfitting?
**A:** Underfitting occurs when a model is too simple to capture the underlying patterns in the data, resulting in poor performance on both training and validation sets. Solutions include increasing model complexity, training longer, or improving feature engineering.
**Code:**
```python
model = nn.Sequential(
    nn.Linear(20, 64), nn.ReLU(),          # increase model complexity
    nn.Linear(64, 64), nn.ReLU(),
    nn.Linear(64, 1),
)
# train longer with more epochs
for epoch in range(200):
    train_one_epoch()
```

## Q14: What is the bias-variance tradeoff?
**A:** Bias is error from overly simplistic assumptions (underfitting). Variance is error from excessive sensitivity to training data (overfitting). The tradeoff means reducing one often increases the other. The goal is to find the optimal balance for best generalization.
**Code:**
```python
import matplotlib.pyplot as plt

# low complexity -> high bias; high complexity -> high variance
complexities = [1, 8, 64, 512, 4096]
train_err, val_err = [], []
for c in complexities:
    model = MLP(hidden_units=c)
    train_err.append(train_loss(model)); val_err.append(val_loss(model))

plt.plot(complexities, train_err, label="train")
plt.plot(complexities, val_err, label="validation")
plt.xscale("log"); plt.legend(); plt.show()   # pick complexity with min val error
```

## Q15: What is cross-validation?
**A:** Cross-validation is a technique for assessing model performance by partitioning data into complementary subsets. k-fold cross-validation splits data into k folds, trains on k-1 folds and validates on the remaining fold, repeating k times. This provides robust performance estimates.
**Code:**
```python
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

scores = cross_val_score(RandomForestClassifier(), X, y, cv=5)  # 5-fold CV
print(scores.mean(), scores.std())
```

## Q16: What is the training-validation-test split?
**A:** Data is split into three sets: training (used to learn parameters), validation (used for hyperparameter tuning and model selection), and test (used for final, unbiased performance evaluation). Common splits are 70-15-15 or 80-10-10.
**Code:**
```python
from sklearn.model_selection import train_test_split

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3)      # 70/30
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5)  # 15/15
print(X_train.shape, X_val.shape, X_test.shape)
```

## Q17: What is batch normalization?
**A:** Batch normalization normalizes layer inputs by subtracting the batch mean and dividing by the batch standard deviation. It stabilizes training, allows higher learning rates, reduces internal covariate shift, and provides some regularization.
**Code:**
```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(128, 256),
    nn.BatchNorm1d(256),        # normalize layer inputs to mean 0, std 1
    nn.ReLU(),
    nn.Linear(256, 10),
)
```

## Q18: What is dropout?
**A:** Dropout is a regularization technique where randomly selected neurons are "dropped out" (set to zero) during training with probability p. This prevents co-adaptation of neurons and forces the network to learn more robust features.
**Code:**
```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(128, 256), nn.ReLU(),
    nn.Dropout(p=0.5),          # each neuron zeroed with probability 0.5
    nn.Linear(256, 10),
)
model.train()   # dropout active during training
```

## Q19: What is early stopping?
**A:** Early stopping halts training when validation performance stops improving for a specified number of epochs (patience). It prevents overfitting by stopping before the model memorizes training data noise.
**Code:**
```python
best_val, patience, bad_epochs = float("inf"), 5, 0
for epoch in range(100):
    train_one_epoch()
    val_loss = validate(model)
    if val_loss < best_val:
        best_val = val_loss
        bad_epochs = 0
        torch.save(model.state_dict(), "best.pt")
    else:
        bad_epochs += 1
        if bad_epochs >= patience:      # no improvement for `patience` epochs
            model.load_state_dict(torch.load("best.pt"))
            break
```

## Q20: What optimizers are commonly used for training neural networks?
**A:** Common optimizers include SGD (with momentum), Adam, AdamW, RMSprop, Adagrad, Adadelta, and Lion. Adam is popular for its adaptive learning rates and momentum, while AdamW improves on Adam by decoupling weight decay.
**Code:**
```python
import torch

sgd = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
adam = torch.optim.Adam(model.parameters(), lr=1e-3)
adamw = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.01)
rmsprop = torch.optim.RMSprop(model.parameters(), lr=1e-3)
adagrad = torch.optim.Adagrad(model.parameters(), lr=1e-2)
```

## Q21: How does the Adam optimizer work?
**A:** Adam combines momentum (adaptive gradient direction) with RMSprop (adaptive learning rate per parameter). It maintains moving averages of gradients (first moment) and squared gradients (second moment), with bias correction for initialization.
**Code:**
```python
# Adam update core: biased-corrected first/second moment estimates
m = beta1 * m + (1 - beta1) * g          # first moment (mean of gradients)
v = beta2 * v + (1 - beta2) * g ** 2     # second moment (mean of squared gradients)
m_hat = m / (1 - beta1 ** t)             # bias correction
v_hat = v / (1 - beta2 ** t)
param -= lr * m_hat / (v_hat.sqrt() + eps)

optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)  # ready-made
```

## Q22: What is weight decay?
**A:** Weight decay is a regularization technique that adds a penalty term to the loss function proportional to the magnitude of weights (usually L2 norm). It prevents weights from growing too large and helps control overfitting.
**Code:**
```python
import torch

# AdamW: decoupled weight decay applied directly to weights
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.01)

# Equivalent L2 penalty added to the loss
loss = task_loss + 0.5 * 0.01 * sum(p.pow(2).sum() for p in model.parameters())
```

## Q23: What is gradient clipping?
**A:** Gradient clipping limits the magnitude of gradients during backpropagation to prevent exploding gradients. If the gradient norm exceeds a threshold, it is scaled down. This is especially important for RNNs and deep networks.
**Code:**
```python
import torch

optimizer.zero_grad()
loss.backward()
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)  # cap gradient norm
optimizer.step()
```

## Q24: What is the vanishing gradient problem?
**A:** Vanishing gradients occur when gradients become extremely small as they backpropagate through many layers, causing early layers to learn very slowly or not at all. Solutions include ReLU activations, batch normalization, residual connections, and proper weight initialization.
**Code:**
```python
import torch.nn as nn

block = nn.Sequential(
    nn.Linear(256, 256), nn.BatchNorm1d(256), nn.ReLU(),   # ReLU + BN
    nn.Linear(256, 256),
)

# Residual connection (identity shortcut) preserves gradient flow
x = block(x) + x
```

## Q25: What is the exploding gradient problem?
**A:** Exploding gradients occur when gradients become extremely large, causing unstable training and numerical overflow. Solutions include gradient clipping, proper weight initialization, and using optimizers with adaptive learning rates.
**Code:**
```python
optimizer.zero_grad()
loss.backward()
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.5)  # prevent explosion
optimizer.step()
```

## Q26: What activation functions are commonly used?
**A:** Common activations include ReLU (most popular for hidden layers), sigmoid (for binary classification output), tanh (for RNNs), Leaky ReLU (fixes dying ReLU), GELU (used in transformers), Swish/SiLU, and softmax (for multi-class output).
**Code:**
```python
import torch.nn.functional as F

x = torch.randn(16, 8)
relu = F.relu(x)
sigmoid = torch.sigmoid(x)
tanh = torch.tanh(x)
leaky = F.leaky_relu(x, 0.1)
gelu = F.gelu(x)
swish = F.silu(x)
softmax = F.softmax(x, dim=-1)
```

## Q27: Why is ReLU widely used?
**A:** ReLU (Rectified Linear Unit) is computationally efficient (simple max(0, x)), helps mitigate vanishing gradients in positive regions, promotes sparse activation, and empirically works well in deep networks. Drawback: dying ReLU problem for negative inputs.
**Code:**
```python
import torch

x = torch.tensor([-1.0, 0.0, 2.0])
print(torch.relu(x))          # tensor([0., 0., 2.])  = max(0, x)
```

## Q28: What is the dying ReLU problem?
**A:** The dying ReLU problem occurs when neurons get stuck outputting 0 for all inputs (because the gradient is 0 for negative inputs, so they never recover). Solutions include Leaky ReLU, PReLU, ELU, or using smaller learning rates.
**Code:**
```python
import torch.nn as nn

# Leaky ReLU keeps a small gradient for negative inputs -> neurons recover
leaky = nn.LeakyReLU(negative_slope=0.01)
print(leaky(torch.tensor([-2.0])))   # tensor([-0.02])
```

## Q29: What is transfer learning?
**A:** Transfer learning leverages a pre-trained model (trained on a large, general dataset) as a starting point for a new but related task. It involves fine-tuning some or all layers on the target dataset, requiring less data and training time.
**Code:**
```python
import torchvision.models as models
import torch.nn as nn

model = models.resnet18(weights="IMAGENET1K_V1")       # pre-trained base
model.fc = nn.Linear(model.fc.in_features, 10)          # replace head for new task
```

## Q30: How does fine-tuning work?
**A:** Fine-tuning takes a pre-trained model and continues training on a new dataset. Common strategies: freeze early layers (general features) and retrain later layers (task-specific features), or train all layers with a lower learning rate.
**Code:**
```python
model = models.resnet18(weights="IMAGENET1K_V1")
model.fc = nn.Linear(512, 10)

for name, param in model.named_parameters():
    param.requires_grad = name in {"fc.weight", "fc.bias"}  # freeze early layers

optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)   # low LR for fine-tuning
```

## Q31: What is data augmentation?
**A:** Data augmentation artificially expands the training dataset by applying transformations to existing data: rotations, flips, crops, color shifts (images), back-translation (text), pitch shifting (audio), and synthetic data generation.
**Code:**
```python
from torchvision import transforms

augment = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2),
    transforms.ToTensor(),
])
train_loader = DataLoader(ImageDataset(transform=augment), batch_size=32, shuffle=True)
```

## Q32: What is curriculum learning?
**A:** Curriculum learning organizes training data from easy to hard examples, gradually increasing difficulty. This mimics how humans learn and can lead to faster convergence and better generalization compared to random data ordering.
**Code:**
```python
# Sort examples by difficulty, then train on increasingly hard slices
examples.sort(key=lambda ex: ex.difficulty)
for epoch in range(10):
    # show more of the dataset as training progresses (easy -> hard)
    subset = examples[: len(examples) * (epoch + 1) // 10]
    train_one_epoch(subset)
```

## Q33: What is learning rate scheduling?
**A:** Learning rate scheduling adjusts the learning rate during training. Strategies include: step decay (reduce at fixed intervals), exponential decay, cosine annealing, cyclic LR (oscillating), warmup (gradually increase initially), and ReduceLROnPlateau (reduce when plateaued).
**Code:**
```python
import torch.optim.lr_scheduler as S

# ReduceLROnPlateau: lower LR when validation loss stops improving
scheduler = S.ReduceLROnPlateau(optimizer, mode="min", patience=3, factor=0.5)

for epoch in range(50):
    train_one_epoch()
    val_loss = validate()
    scheduler.step(val_loss)   # reduces LR if val_loss plateaus
```

## Q34: What is the one-cycle learning rate policy?
**A:** The one-cycle policy by Leslie Smith starts with a low learning rate, linearly increases to a maximum, then decreases. Combined with momentum cycling opposite, this allows training with much higher max learning rates, often reaching better minima faster.
**Code:**
```python
import torch.optim.lr_scheduler as S

scheduler = S.OneCycleLR(
    optimizer,
    max_lr=0.01,                  # peak learning rate
    total_steps=200,
    pct_start=0.3,                # warmup for first 30% of steps
    anneal_strategy="cos",
)
for step in range(200):
    train_step()
    scheduler.step()
```

## Q35: What is the difference between batch gradient descent and stochastic gradient descent?
**A:** Batch GD computes gradients on the full dataset (accurate but slow, memory-intensive). SGD computes gradients on single samples (fast updates but noisy, oscillating). Mini-batch GD is the practical middle ground.
**Code:**
```python
# Batch GD: one update per full pass over the dataset
loss = criterion(model(X), y).mean()
loss.backward(); optimizer.step(); optimizer.zero_grad()

# SGD: one update per sample (noisy)
for x_i, y_i in zip(X, y):
    loss = criterion(model(x_i), y_i)
    loss.backward(); optimizer.step(); optimizer.zero_grad()

# Mini-batch GD: middle ground
for xb, yb in DataLoader(dataset, batch_size=64):
    loss = criterion(model(xb), yb).mean()
    loss.backward(); optimizer.step(); optimizer.zero_grad()
```

## Q36: What is momentum in optimization?
**A:** Momentum accumulates a moving average of past gradients to accelerate convergence in consistent directions and dampen oscillations. It helps navigate ravines and flat regions. The momentum coefficient (typically 0.9) controls how much past gradients influence the update.
**Code:**
```python
# velocity update: v = momentum * v + lr * grad; parameters -= v
v = momentum * v + lr * g

optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
```

## Q37: How do you choose the batch size?
**A:** Batch size affects training speed, memory usage, and convergence quality. Smaller batches provide noisy gradients that can help escape sharp minima (better generalization). Larger batches provide more accurate gradients but may converge to sharper minima. Typical range: 16-512.
**Code:**
```python
from torch.utils.data import DataLoader

# Trade-off: small (noisy, generalizes) vs large (accurate, sharper minima)
loader_small = DataLoader(dataset, batch_size=16)
loader_large = DataLoader(dataset, batch_size=256)
for xb, yb in loader_small:      # more, noisier updates per epoch
    optimizer.zero_grad()
    loss = criterion(model(xb), yb)
    loss.backward()
    optimizer.step()
```

## Q38: What is gradient accumulation?
**A:** Gradient accumulation simulates larger batch sizes by accumulating gradients over multiple forward/backward passes before performing one optimizer step. This enables training with effective batch sizes larger than GPU memory permits.
**Code:**
```python
acc_steps = 4                      # simulate batch_size * 4
optimizer.zero_grad()
for i, (xb, yb) in enumerate(dataloader):
    loss = criterion(model(xb), yb) / acc_steps
    loss.backward()                # accumulate gradients
    if (i + 1) % acc_steps == 0:
        optimizer.step()           # one optimizer step per acc_steps batches
        optimizer.zero_grad()
```

## Q39: What is mixed precision training?
**A:** Mixed precision training uses float16 (half precision) for most operations while keeping critical computations (loss scaling, gradient updates) in float32. This reduces memory usage and speeds up training on GPUs with Tensor Cores (NVIDIA).
**Code:**
```python
scaler = torch.cuda.amp.GradScaler()          # keeps gradient updates in fp32
for xb, yb in dataloader:
    with torch.cuda.amp.autocast():           # fp16 for ops in this block
        loss = criterion(model(xb), yb)
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

## Q40: What is distributed training?
**A:** Distributed training uses multiple GPUs or machines to train models faster. Strategies include data parallelism (each device has a copy of the model and processes different data batches) and model parallelism (different devices handle different model parts).
**Code:**
```python
import torch.distributed as dist

dist.init_process_group("nccl")                       # one process per GPU
model = nn.parallel.DistributedDataParallel(model)    # data parallelism
for xb, yb in dataloader:
    loss = model(xb, yb)["loss"]
    loss.backward()
    optimizer.step()
```

## Q41: What is data parallelism?
**A:** Data parallelism splits the training batch across multiple devices. Each device has a complete copy of the model, processes its data subset, computes gradients, and synchronizes gradient updates. Frameworks: DDP (PyTorch), Horovod, TF distributed strategies.
**Code:**
```python
import torch.distributed as dist

dist.init_process_group("nccl")                      # one GPU per process
model = nn.parallel.DistributedDataParallel(model)   # replicate model, shard batch

# Each rank sees its own shard of the batch and gradients are all-reduced
for xb, yb in dataloader:
    loss = criterion(model(xb), yb)
    loss.backward()
    optimizer.step()
```

## Q42: What is model parallelism?
**A:** Model parallelism splits the model architecture across multiple devices, with each device handling specific layers or operations. This is necessary when the model is too large to fit on a single device (e.g., large language models with hundreds of billions of parameters).
**Code:**
```python
dev0, dev1 = "cuda:0", "cuda:1"

# Split the model across devices
emb_layers = nn.ModuleList([...]).to(dev0)
head_layers = nn.ModuleList([...]).to(dev1)

def forward(x):
    x = x.to(dev0)
    for layer in emb_layers:
        x = layer(x)
    x = x.to(dev1)
    for layer in head_layers:
        x = layer(x)
    return x
```

## Q43: What is pipeline parallelism?
**A:** Pipeline parallelism combines model parallelism with data parallelism. Different layers are placed on different devices, and micro-batches are pipelined through the devices. This reduces idle time compared to naive model parallelism.
**Code:**
```python
# Stages on different GPUs; micro-batches flow through the pipeline
stages = [stage0.to("cuda:0"), stage1.to("cuda:1"), stage2.to("cuda:2")]

for micro_batch in split(big_batch, num_micro_batches):
    x = micro_batch
    for stage in stages:
        x = stage(x)          # pipelined forward through stage devices
```

## Q44: What is tensor parallelism?
**A:** Tensor parallelism splits individual tensor operations (like matrix multiplication) across multiple devices. This is finer-grained than model parallelism and is used in large transformer models (e.g., Megatron-LM) where even a single layer computation is split.
**Code:**
```python
# Split the weight matrix columns across devices for one matmul
W0, W1 = W.chunk(2, dim=-1)                       # W: [d, 2k] -> [d,k] each
y = torch.cat([x @ W0.to("cuda:0"), x @ W1.to("cuda:1")], dim=-1)
```

## Q45: What is the role of a validation set?
**A:** The validation set is used during development to tune hyperparameters, compare models, and detect overfitting. It provides an unbiased evaluation while the model is being iteratively improved. Performance on the validation set guides model selection.
**Code:**
```python
from sklearn.model_selection import train_test_split

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)
best = None
for lr in [1e-4, 1e-3, 1e-2]:                    # tune hyperparameters
    model = LogisticRegression(C=1/lr).fit(X_train, y_train)
    val_acc = model.score(X_val, y_val)          # validate on held-out val set
    if best is None or val_acc > best[1]:
        best = (lr, val_acc)
print("best lr:", best)
```

## Q46: What is the test set and why should it be kept separate?
**A:** The test set is used only once at the very end to provide an unbiased final performance estimate. It must never be used for training decisions or hyperparameter tuning, as that would leak information and overestimate generalization performance.
**Code:**
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# ... tune everything on train/validation during development ...

test_acc = best_model.score(X_test, y_test)   # final evaluation only
print(f"test accuracy: {test_acc:.3f}")
```

## Q47: How do you handle imbalanced datasets?
**A:** Techniques include: resampling (oversample minority class, undersample majority), class weights (higher weight for minority classes in the loss function), synthetic data generation (SMOTE), anomaly detection approaches, and specialized loss functions (focal loss).
**Code:**
```python
import torch.nn as nn

# Class weights: upweight the minority class in the loss
class_weights = torch.tensor([1.0, 5.0])
criterion = nn.CrossEntropyLoss(weight=class_weights)

loss = criterion(logits, y)
```

## Q48: What is SMOTE?
**A:** SMOTE (Synthetic Minority Over-sampling Technique) creates synthetic samples for the minority class by interpolating between existing minority samples and their nearest neighbors. This balances class distribution without simple duplication.
**Code:**
```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_res, y_res = smote.fit_resample(X, y)      # interpoles minority samples
print(X_res.shape, y_res.shape)
```

## Q49: What is focal loss?
**A:** Focal loss modifies cross-entropy loss to down-weight well-classified examples and focus training on hard, misclassified examples. It's particularly effective for class imbalance and object detection tasks where background dominates.
**Code:**
```python
import torch.nn.functional as F

def focal_loss(logits, target, gamma=2.0, alpha=0.25):
    ce = F.cross_entropy(logits, target, reduction="none")
    pt = torch.exp(-ce)                          # probability of true class
    return (alpha * (1 - pt) ** gamma * ce).mean()

loss = focal_loss(logits, y)
```

## Q50: What is the difference between training loss and validation loss?
**A:** Training loss measures error on the training data (should decrease over time). Validation loss measures error on unseen data. A diverging gap (training loss decreasing while validation loss increases) indicates overfitting.
**Code:**
```python
train_losses.append(run_epoch(train_loader))   # keeps decreasing
val_losses.append(run_epoch(val_loader))       # diverges when overfitting

if val_losses[-1] > val_losses[-2] and len(val_losses) > 2:
    print("overfitting detected: val loss rising")
```

## Q51: What are learning curves?
**A:** Learning curves plot training and validation metrics (loss, accuracy) over epochs. They help diagnose training problems: underfitting (both high), overfitting (diverging gap), good fit (both low with small gap), and convergence (plateauing).
**Code:**
```python
import matplotlib.pyplot as plt

plt.plot(range(len(train_losses)), train_losses, label="train")
plt.plot(range(len(val_losses)), val_losses, label="validation")
plt.xlabel("epoch"); plt.ylabel("loss"); plt.legend()
plt.show()          # diverging curves => overfitting; both high => underfitting
```

## Q52: How do you debug a model that is not learning?
**A:** Start with: check data pipeline (correct labels, preprocessing), overfit a single batch (model should memorize), reduce learning rate, simplify the model, check gradient statistics (vanishing/exploding), verify loss function is appropriate, and inspect input/output shapes.
**Code:**
```python
# 1) Overfit a single batch: the model should memorize it
xb, yb = next(iter(dataloader))
for _ in range(500):
    optimizer.zero_grad()
    loss = criterion(model(xb), yb)
    loss.backward()
    optimizer.step()
print("single-batch loss:", loss.item())   # should drop to ~0

# 2) Inspect gradient norms to catch vanishing/exploding
for name, param in model.named_parameters():
    if param.grad is not None:
        print(name, param.grad.norm().item())
```

## Q53: What is a learning rate finder?
**A:** A learning rate finder (LR range test) runs training with a learning rate that gradually increases from very small to very large, tracking the loss. The optimal learning rate is typically where the loss decreases most steeply, before diverging.
**Code:**
```python
import torch

lrs, losses = [], []
lr = 1e-7
for step in range(200):
    for g in optimizer.param_groups:
        g["lr"] = lr
    loss = train_step().item()
    lrs.append(lr); losses.append(loss)
    lr *= 1.1                              # exponentially increase LR
# optimal LR ≈ where loss falls fastest before shooting up
```

## Q54: What is cyclical learning rate?
**A:** Cyclical learning rate (CLR) oscillates the learning rate between a minimum and maximum bound during training. This helps escape sharp minima and saddle points, often leading to better generalization without needing to find the exact best learning rate.
**Code:**
```python
import torch.optim.lr_scheduler as S

scheduler = S.CyclicLR(
    optimizer,
    base_lr=1e-4,        # minimum bound
    max_lr=1e-2,         # maximum bound
    step_size_up=10,     # steps to reach max_lr
)
for epoch in range(50):
    train_one_epoch()
    scheduler.step()     # LR oscillates between base_lr and max_lr
```

## Q55: What is weight initialization and why is it important?
**A:** Weight initialization sets initial parameter values before training. Proper initialization prevents vanishing/exploding gradients and helps faster convergence. Common methods: Xavier/Glorot (for tanh/sigmoid), He/Kaiming (for ReLU), and orthogonal initialization.
**Code:**
```python
import torch.nn as nn

def init_weights(m):
    if isinstance(m, nn.Linear):
        nn.init.xavier_uniform_(m.weight)     # for tanh/sigmoid nets
        nn.init.zeros_(m.bias)

model.apply(init_weights)
```

## Q56: What is Xavier initialization?
**A:** Xavier (Glorot) initialization sets weights from a distribution with variance 2/(fan_in + fan_out), where fan_in and fan_out are the number of input and output connections. It maintains gradient variance through layers for tanh/sigmoid activations.
**Code:**
```python
import torch.nn as nn

layer = nn.Linear(128, 256)
nn.init.xavier_uniform_(layer.weight)   # U(-sqrt(6/(fan_in+fan_out)), +sqrt(6/(fan_in+fan_out)))
nn.init.zeros_(layer.bias)
```

## Q57: What is He initialization?
**A:** He (Kaiming) initialization sets weights from a distribution with variance 2/fan_in. It's designed for ReLU activations, accounting for the fact that ReLU zeros out half the outputs, effectively doubling the variance of surviving signals.
**Code:**
```python
import torch.nn as nn

layer = nn.Linear(128, 256)
nn.init.kaiming_normal_(layer.weight, mode="fan_in", nonlinearity="relu")
nn.init.zeros_(layer.bias)
```

## Q58: What is the cold start problem in training?
**A:** Cold start refers to the initial phase of training when parameters are random, gradients are noisy, and loss decreases slowly. Gradual warmup (starting with a very small learning rate and increasing) helps stabilize this phase.
**Code:**
```python
# Linear warmup: start with a tiny LR and ramp up over ~1000 steps
for step in range(2000):
    lr = 1e-3 * min(step / 1000, 1.0)
    for g in optimizer.param_groups:
        g["lr"] = lr
    train_step()
```

## Q59: What is the warmup strategy?
**A:** Warmup gradually increases the learning rate from near zero to the target rate over a specified number of steps or epochs. This prevents early training instability and is especially important for large batch training and transformer models.
**Code:**
```python
import torch.optim.lr_scheduler as S

# Linear warmup over 2000 steps, then cosine decay to ~0
warmup = S.LinearLR(optimizer, start_factor=0.01, end_factor=1.0, total_iters=2000)
decay = S.CosineAnnealingLR(optimizer, T_max=10000)
scheduler = S.SequentialLR(optimizer, schedulers=[warmup, decay], milestones=[2000])

for step in range(12000):
    train_step()
    scheduler.step()
```

## Q60: How do you handle missing data during training?
**A:** Strategies include: remove samples with missing values (if few), impute with mean/median/mode, use models that handle missing values (tree-based), create indicator features, use interpolation (time series), or learn to predict missing values.
**Code:**
```python
import pandas as pd
from sklearn.impute import SimpleImputer

df = pd.DataFrame({"age": [25, None, 30, 28], "income": [50, 60, None, 70]})

# Impute missing values with the column median
imputer = SimpleImputer(strategy="median")
X_filled = imputer.fit_transform(df)
print(X_filled)
```

## Q61: What is feature scaling and why is it needed?
**A:** Feature scaling normalizes the range of input features. Methods: standardization (zero mean, unit variance), min-max scaling (to [0,1]), robust scaling (using median/IQR). Needed because features with larger ranges can dominate gradient updates.
**Code:**
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()         # zero mean, unit variance
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)   # fit ONLY on training data
```

## Q62: What is the difference between normalization and standardization?
**A:** Normalization (min-max scaling) rescales to a fixed range [0,1] using min and max. Standardization centers at 0 with standard deviation 1 using mean and std. Standardization is less affected by outliers and is preferred for many algorithms.
**Code:**
```python
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

X_minmax = MinMaxScaler().fit_transform(X)     # range [0,1]
X_std = StandardScaler().fit_transform(X)      # mean 0, std 1
X_robust = RobustScaler().fit_transform(X)     # median and IQR (outlier-resistant)
```

## Q63: What is one-hot encoding?
**A:** One-hot encoding converts categorical variables into binary vectors. Each category becomes a binary column where exactly one element is 1 (hot) and others are 0. This avoids implying ordinal relationships between categories.
**Code:**
```python
import pandas as pd

df = pd.DataFrame({"color": ["red", "green", "blue", "red"]})
encoded = pd.get_dummies(df["color"], prefix="color")
print(encoded)             # one binary column per category
```

## Q64: What is label encoding vs one-hot encoding?
**A:** Label encoding assigns each category a unique integer (1, 2, 3...). It implies ordinal relationships and is unsuitable for nominal categories. One-hot encoding avoids this but increases dimensionality. Label encoding is appropriate for ordinal categories.
**Code:**
```python
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

colors = [["red"], ["green"], ["blue"]]

le = LabelEncoder()                       # assigns 0,1,2 (implies order!)
print(le.fit_transform(["red", "green", "blue"]))

oh = OneHotEncoder(sparse_output=False)   # one column per category
print(oh.fit_transform(colors))
```

## Q65: How do you choose the number of epochs?
**A:** Use early stopping based on validation loss. Set a maximum (e.g., 1000) with patience (e.g., 10) where training stops if validation loss doesn't improve. Monitor learning curves to ensure training has converged.
**Code:**
```python
best_val = float("inf")
patience, bad_epochs = 10, 0
for epoch in range(1000):                 # maximum epochs
    train_one_epoch()
    current_val = validate(model)
    if current_val < best_val - 1e-4:
        best_val, bad_epochs = current_val, 0
        torch.save(model.state_dict(), "best.pt")
    else:
        bad_epochs += 1
        if bad_epochs >= patience:        # stop after 10 no-improvement epochs
            model.load_state_dict(torch.load("best.pt"))
            break
```

## Q66: What is the model capacity?
**A:** Model capacity refers to the complexity of the model, typically measured by the number of parameters, depth, or width. Higher capacity can learn more complex patterns but risks overfitting. Lower capacity may underfit. Capacity should match data complexity and size.
**Code:**
```python
import torch.nn as nn

# Lower capacity: fewer parameters
small = nn.Sequential(nn.Linear(20, 8), nn.ReLU(), nn.Linear(8, 1))
# Higher capacity: many more parameters
large = nn.Sequential(nn.Linear(20, 512), nn.ReLU(), nn.Linear(512, 512), nn.ReLU(), nn.Linear(512, 1))

print(sum(p.numel() for p in small.parameters()))   # e.g. 185
print(sum(p.numel() for p in large.parameters()))   # e.g. ~273k
```

## Q67: What is the universal approximation theorem?
**A:** The universal approximation theorem states that a feedforward neural network with a single hidden layer containing sufficient neurons can approximate any continuous function to arbitrary accuracy, given appropriate activation functions (non-linear, e.g., sigmoid).
**Code:**
```python
import torch.nn as nn

# Single hidden layer with many neurons approximates any continuous function
model = nn.Sequential(
    nn.Linear(1, 256),      # hidden layer
    nn.Sigmoid(),           # non-linear activation
    nn.Linear(256, 1),
)
y_pred = model(x)           # arbitrarily close to the true f(x) as width grows
```

## Q68: How do you train large language models?
**A:** LLM training involves: massive datasets (trillions of tokens), distributed training across thousands of GPUs, mixed precision (bf16/fp16), gradient checkpointing, tensor/pipeline parallelism, 3D parallelism (DP+PP+TP), ZeRO optimization, and careful learning rate scheduling with warmup.
**Code:**
```python
# Mixed precision bf16 + gradient checkpointing + cosine schedule with warmup
with torch.autocast("cuda", dtype=torch.bfloat16):
    loss = model(input_ids, labels=labels).loss

scheduler = torch.optim.lr_scheduler.OneCycleLR(
    optimizer, max_lr=3e-4, total_steps=total_steps, pct_start=0.03
)

# Distributed with ZeRO/FSDP under TorchTitan/DeepSpeed for 3D parallelism
model = fsdp_wrap(model)
```

## Q69: What is the pretraining-finetuning paradigm?
**A:** First, a model is pre-trained on a large, general corpus using self-supervised objectives (next token prediction, masked language modeling). Then it's fine-tuned on a smaller, task-specific dataset. This transfers general knowledge to specific tasks efficiently.
**Code:**
```python
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments

# Phase 1: pretrain on a large general corpus (self-supervised)
model = AutoModelForCausalLM.from_pretrained("gpt2")

# Phase 2: fine-tune on a small task-specific dataset
trainer = Trainer(
    model=model,
    args=TrainingArguments(output_dir="./ft", per_device_train_batch_size=4),
    train_dataset=tiny_task_dataset,
)
trainer.train()
```

## Q70: What are self-supervised learning objectives?
**A:** Self-supervised learning creates supervisory signals from unlabeled data. Common objectives: masked language modeling (MLM, BERT), next token prediction (GPT), contrastive learning (SimCLR), and rotation prediction (images).
**Code:**
```python
# Masked language modeling: predict the masked tokens from context
def mlm_loss(model, input_ids, mask_token_id):
    masked = input_ids.clone()
    mask = (torch.rand_like(input_ids.float()) < 0.15) & (input_ids != mask_token_id)
    masked[mask] = mask_token_id
    return F.cross_entropy(model(masked).logits.view(-1, vocab_size), input_ids.view(-1),
                           ignore_index=mask_token_id)
```

## Q71: What is contrastive learning?
**A:** Contrastive learning trains models to pull similar (positive) pairs together and push dissimilar (negative) pairs apart in embedding space. It's widely used for self-supervised representation learning in vision (SimCLR, MoCo) and NLP.
**Code:**
```python
import torch.nn.functional as F

# InfoNCE: positives on the diagonal, negatives are all other rows/cols
def nt_xent(z, temperature=0.1):
    z = F.normalize(z, dim=-1)
    sim = z @ z.T / temperature
    labels = torch.arange(z.size(0))
    return F.cross_entropy(sim, labels)

loss = nt_xent(torch.cat([z1, z2], dim=0))  # z1, z2: embeddings of two views
```

## Q72: What is knowledge distillation?
**A:** Knowledge distillation trains a smaller "student" model to mimic a larger "teacher" model. The student learns from the teacher's soft predictions (logits) rather than hard labels, capturing the teacher's knowledge more effectively.
**Code:**
```python
import torch.nn.functional as F

T = 4.0  # temperature
soft_targets = F.softmax(teacher_logits / T, dim=-1)
student_soft = F.log_softmax(student_logits / T, dim=-1)

kd_loss = F.kl_div(student_soft, soft_targets, reduction="batchmean") * T ** 2
task_loss = F.cross_entropy(student_logits, labels)
loss = alpha * kd_loss + (1 - alpha) * task_loss
```

## Q73: What is the temperature parameter in distillation?
**A:** Temperature softens the probability distribution from the teacher model. Higher temperature produces softer distributions (more information about relative probabilities of classes), enabling the student to learn nuanced relationships beyond just the correct class.
**Code:**
```python
import torch.nn.functional as F

logits = torch.tensor([2.0, 1.0, 0.1])

p_hard = F.softmax(logits, dim=-1)          # sharp, near one-hot
p_soft = F.softmax(logits / 3.0, dim=-1)    # higher T -> softer distribution
print(p_hard)
print(p_soft)
```

## Q74: What is quantization in model training?
**A:** Quantization reduces the precision of model weights and activations from float32 to lower bit widths (int8, float16, bfloat16). This reduces memory footprint and speeds up inference, often with minimal accuracy loss.
**Code:**
```python
import torch

w = torch.randn(64, 64)
scale = w.abs().max() / 127.0
w_int8 = torch.clamp(torch.round(w / scale).to(torch.int8), -128, 127)  # fp32 -> int8
w_deq = w_int8.float() * scale                                            # dequantized
print("max abs error:", (w - w_deq).abs().max().item())
```

## Q75: What is QAT (Quantization-Aware Training)?
**A:** QAT simulates quantization effects during training by inserting fake quantization nodes in the computation graph. The model learns to adapt to lower precision, resulting in better accuracy post-quantization compared to post-training quantization.
**Code:**
```python
import torch

def fake_quantize(w, scale):
    # Round to nearest int, keep gradients flowing via straight-through estimator
    return (torch.clamp(torch.round(w / scale), -128, 127) * scale - w).detach() + w

# Used inside the forward pass during training QAT
for name, p in model.named_parameters():
    if p.dim() >= 2:
        p.data = fake_quantize(p.data.detach(), scale)   # simulated int8 weights
```

## Q76: What is pruning in neural networks?
**A:** Pruning removes unnecessary weights or neurons from a trained network to reduce model size and computational cost without significant accuracy loss. Methods include magnitude-based pruning (remove small weights), structured pruning (remove entire channels/neurons).
**Code:**
```python
import torch.nn.utils.prune as prune

# Magnitude pruning: remove the smallest 50% of weights in a layer
prune.l1_unstructured(net.fc, name="weight", amount=0.5)
print(net.fc.weight)              # many weights are now 0 (pruned)
print(prune.is_pruned(net.fc))
```

## Q77: What is the lottery ticket hypothesis?
**A:** The lottery ticket hypothesis suggests that dense neural networks contain sparse subnetworks ("winning tickets") that, when trained in isolation, can achieve comparable accuracy to the original network much faster. These subnetworks are identified through iterative pruning.
**Code:**
```python
# 1) Initialize and record starting weights, 2) train, 3) prune, 4) rewind to start
init_state = {k: v.clone() for k, v in model.state_dict().items()}

for round_ in range(5):
    train(model)                                # train dense weights
    prune_amount = 1 - (0.8 ** (round_ + 1))    # progressively prune
    for name, module in model.named_modules():
        if hasattr(module, "weight") and hasattr(module, "weight_mask"):
            prune.l1_unstructured(module, name="weight", amount=0.2)
    model.load_state_dict(init_state)           # rewind remaining weights
```

## Q78: How do you train models on streaming data?
**A:** Online learning processes data incrementally as it arrives, updating the model continuously. Techniques include stochastic gradient descent (online variant), incremental learning, and adaptive learning rates. Challenges include concept drift and catastrophic forgetting.
**Code:**
```python
from sklearn.linear_model import SGDRegressor

model = SGDRegressor(learning_rate="adaptive", eta0=0.01)  # online learning
for X_batch, y_batch in data_stream():          # data arrives incrementally
    model.partial_fit(X_batch, y_batch)         # update without retraining
```

## Q79: What is catastrophic forgetting?
**A:** Catastrophic forgetting occurs when a neural network forgets previously learned information upon learning new information. This is a key challenge in continual/lifelong learning. Solutions include replay buffers, elastic weight consolidation (EWC), and progressive networks.
**Code:**
```python
# Replay buffer: mix old-task samples into new-task batches to avoid forgetting
replay_batch = sample_from_buffer(np.ones(64, dtype=int))
for x_new, y_new in new_loader:
    xb = torch.cat([x_new, replay_batch])
    yb = torch.cat([y_new, replay_labels])
    loss = criterion(model(xb), yb)
    loss.backward(); optimizer.step()
```

## Q80: What is elastic weight consolidation (EWC)?
**A:** EWC prevents catastrophic forgetting by adding a penalty to the loss function for changing important parameters. Parameter importance is estimated from the Fisher information matrix, allowing the model to learn new tasks while preserving knowledge of old tasks.
**Code:**
```python
# EWC penalty: penalize moving away from old optimal parameters, scaled by Fisher
def ewc_penalty(model, fisher, opt_params, prev_params, lam=100):
    penalty = 0.0
    for name, p in model.named_parameters():
        f = fisher[name]
        penalty += (f * (p - prev_params[name]) ** 2).sum()
    return lam * penalty

total_loss = new_task_loss + ewc_penalty(model, fisher, opt, prev_theta)
```

## Q81: What is reproducibility in model training?
**A:** Reproducibility means training runs produce identical results given the same code, data, and configuration. It requires: fixing random seeds, deterministic algorithms, controlling nondeterministic operations (GPU ops), consistent data ordering, and logging all hyperparameters.
**Code:**
```python
import random
import numpy as np
import torch

random.seed(42)
np.random.seed(42)
torch.manual_seed(42)
torch.cuda.manual_seed_all(42)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
```

## Q82: How do you set random seeds for reproducibility?
**A:** Set seeds for Python's random, numpy, and the deep learning framework (PyTorch/TensorFlow):
**Code:**
```python
import random, numpy as np, torch
random.seed(42); np.random.seed(42); torch.manual_seed(42)
torch.cuda.manual_seed_all(42); torch.backends.cudnn.deterministic = True
```

## Q83: What is experiment tracking?
**A:** Experiment tracking logs and organizes training runs with their parameters, metrics, artifacts (model checkpoints), and environment details. Tools include MLflow, Weights & Biases, TensorBoard, Neptune, and Comet ML.
**Code:**
```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("lr", lr)
    mlflow.log_param("batch_size", batch_size)
    for epoch in range(epochs):
        mlflow.log_metric("train_loss", train_loss, step=epoch)
        mlflow.log_metric("val_loss", val_loss, step=epoch)
    mlflow.log_artifact("best_model.pt")
```

## Q84: What is a model checkpoint?
**A:** A checkpoint saves the model's state (parameters, optimizer state, epoch number, metrics) at a point during training. Checkpoints enable resuming training from interruptions, evaluating intermediate models, and rolling back to the best model.
**Code:**
```python
# Save
torch.save({
    "epoch": epoch,
    "model_state_dict": model.state_dict(),
    "optimizer_state_dict": optimizer.state_dict(),
    "val_loss": val_loss,
}, "checkpoint.pt")

# Resume
ckpt = torch.load("checkpoint.pt")
model.load_state_dict(ckpt["model_state_dict"])
optimizer.load_state_dict(ckpt["optimizer_state_dict"])
start_epoch = ckpt["epoch"] + 1
```

## Q85: How do you save the best model during training?
**A:** Monitor a validation metric (e.g., validation loss) and save the model whenever it improves. Use a ModelCheckpoint callback that saves only when the monitored metric is better than all previous values (save_best_only=True).
**Code:**
```python
import tensorflow as tf

checkpoint = tf.keras.callbacks.ModelCheckpoint(
    "best_model.weights.h5",
    monitor="val_loss",
    save_best_only=True,     # save only when val_loss improves
    save_weights_only=True,
    mode="min",
)
model.fit(X, y, validation_split=0.2, epochs=50, callbacks=[checkpoint])
```

## Q86: What is the Plateau detection in training?
**A:** Plateau detection monitors a metric and triggers actions (like reducing learning rate) when improvement stalls for a defined number of epochs. Implemented via ReduceLROnPlateau callbacks, it helps escape flat regions in the loss landscape.
**Code:**
```python
import torch.optim.lr_scheduler as S

scheduler = S.ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=5)
for epoch in range(100):
    train_one_epoch()
    current = validate(model)
    scheduler.step(current)     # reduces LR when val_loss plateaus for 5 epochs
```

## Q87: What is gradient checkpointing?
**A:** Gradient checkpointing trades compute for memory by not storing intermediate activations during forward pass. Instead, they are recomputed during backward pass. This enables training larger models on limited GPU memory at the cost of ~20-30% more compute.
**Code:**
```python
from torch.utils.checkpoint import checkpoint

def forward(self, x):
    for block in self.blocks:
        # Don't store activations; recompute them during backward
        x = checkpoint(block, x)
    return x
```

## Q88: What is the ZeRO optimizer?
**A:** ZeRO (Zero Redundancy Optimizer) by Microsoft partitions optimizer states, gradients, and parameters across GPUs, eliminating memory redundancy in data-parallel training. ZeRO-1 (optimizer states), ZeRO-2 (+ gradients), ZeRO-3 (+ parameters). Enables training huge models.
**Code:**
```python
import deepspeed

# ZeRO-3 shards optimizer states, gradients, and parameters across GPUs
ds_config = {
    "train_batch_size": 1024,
    "zero_optimization": {"stage": 3, "offload_param": {"device": "cpu"}},
    "fp16": {"enabled": True},
}
model, optimizer, _, _ = deepspeed.initialize(model=model, config=ds_config)
```

## Q89: What is model parallelism in transformers?
**A:** Transformer model parallelism typically uses tensor parallelism (splitting attention and FFN computations across GPUs) and pipeline parallelism (placing different transformer layers on different GPUs). Hybrid approaches combine both for optimal throughput.
**Code:**
```python
# Megatron-style tensor parallelism: split QKV/FFN weights across ranks
import torch.distributed as dist

def split_heads(x, world_size):
    x = x.chunk(world_size, dim=-1)   # each rank owns part of the head dim
    return dist.all_gather(x)         # aggregate across the TP group

y = tensor_parallel_attention(q, k, v)   # attention computed cooperatively
```

## Q90: What is training stability and how do you ensure it?
**A:** Training stability means the loss decreases monotonically without divergence or oscillations. Ensure by: proper learning rate (with warmup), gradient clipping, batch normalization, residual connections, proper initialization, and maintaining reasonable learning rate/batch size ratios.
**Code:**
```python
# Stability kit: clip gradients, warmup LR, monotonic loss check
optimizer.zero_grad()
loss.backward()
torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
optimizer.step()

assert loss_history[-1] <= loss_history[-2] * 1.5, "loss spiked"
```

## Q91: How do you train with limited GPU memory?
**A:** Techniques: gradient accumulation, mixed precision training, gradient checkpointing, reduced batch size, model parallelism, memory-efficient optimizers (Adafactor), activation offloading to CPU, and using memory-efficient attention (Flash Attention).
**Code:**
```python
# Combine gradient accumulation + AMP + activation checkpointing
accumulate = 4
optimizer.zero_grad()
for i, (xb, yb) in enumerate(loader):
    with torch.cuda.amp.autocast():
        loss = criterion(model(xb), yb) / accumulate
    loss.backward()
    if (i + 1) % accumulate == 0:
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        optimizer.zero_grad()
```

## Q92: What is Flash Attention?
**A:** Flash Attention is an efficient attention algorithm that computes exact attention without materializing the full N×N attention matrix. It uses tiling to reduce GPU memory reads/writes, providing 2-4x speedup and significant memory savings for transformer training.
**Code:**
```python
import torch.nn.functional as F

# PyTorch's fused scaled_dot_product_attention (FlashAttention when applicable)
attn = F.scaled_dot_product_attention(q, k, v, is_causal=True)

print(attn.shape)   # [B, H, L, D] — no NxN materialized matrix
```

## Q93: What are LoRA and QLoRA?
**A:** LoRA (Low-Rank Adaptation) adds small trainable rank-decomposition matrices to frozen pre-trained weights, enabling efficient fine-tuning with minimal parameters. QLoRA adds 4-bit quantization of the base model, further reducing memory requirements.
**Code:**
```python
from peft import LoraConfig, get_peft_model
import torch

config = LoraConfig(r=8, lora_alpha=16, target_modules=["q_proj", "v_proj"])
model = get_peft_model(model, config)      # freeze base, train only LoRA matrices
print(trainable_parameters(model))         # < 1% of full model
```

## Q94: What is PEFT (Parameter-Efficient Fine-Tuning)?
**A:** PEFT methods adapt pre-trained models by updating only a small number of (extra) parameters while keeping most pre-trained weights frozen. Methods include LoRA, Adapters, Prefix Tuning, and Prompt Tuning. PEFT reduces memory and storage requirements.
**Code:**
```python
from transformers import Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model

peft_config = LoraConfig(r=8, lora_alpha=32, task_type="CAUSAL_LM")
model = get_peft_model(base_model, peft_config)     # only LoRA params trainable

trainer = Trainer(model=model, args=training_args, train_dataset=dataset)
trainer.train()
trainer.save_model("lora_adapter")                  # tiny adapter checkpoint
```

## Q95: How do you choose an optimizer?
**A:** Start with Adam or AdamW for most deep learning tasks. For NLP/transformers, AdamW is preferred. For computer vision, SGD with momentum can still work well. For LLM fine-tuning, AdamW with 8-bit (bitsandbytes) or Adafactor for memory efficiency.
**Code:**
```python
import torch

# Default recommendation
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=0.01)

# Memory-efficient Adafactor for large models / long contexts
from transformers import Adafactor
opt_adafactor = Adafactor(model.parameters(), scale_parameter=True, relative_step=True)
```

## Q96: What is the learning rate range test (LRRT)?
**A:** The LRRT by Leslie Smith runs training for a few epochs with linearly increasing learning rate, plotting loss vs learning rate. It identifies the optimal learning rate range (where loss decreases fastest) and maximum LR (where loss diverges).
**Code:**
```python
import torch

# LR range test: exponentially ramp LR, record loss at each step
lr_low, lr_high = 1e-6, 1.0
losses, lrs = [], []
lr = lr_low
optimizer = torch.optim.SGD(model.parameters(), lr=lr)
for step in range(100):
    optimizer.zero_grad()
    loss = criterion(model(xb), yb)
    loss.backward(); optimizer.step()
    lrs.append(optimizer.param_groups[0]["lr"]); losses.append(loss.item())
    lr *= (lr_high / lr_low) ** (1 / 100)
    optimizer.param_groups[0]["lr"] = lr
# choose the LR where loss descends most steeply before it shoots up
```

## Q97: How do you train a model from scratch vs fine-tuning?
**A:** Training from scratch requires more data, compute, and time. Fine-tuning starts from a pre-trained model, requiring less data and resources. From scratch allows full control over architecture; fine-tuning benefits from learned representations. Choose based on data availability and task similarity.
**Code:**
```python
import torch.nn as nn

# From scratch: randomized initialization
net_scratch = MyNetwork()                     # weights initialized at random

# Fine-tuning: start from pretrained weights and continue on new data
import torchvision.models as models
net_ft = models.resnet18(weights="IMAGENET1K_V1")
net_ft.fc = nn.Linear(512, 10)                # swap head, keep learned features
```

## Q98: What is the no free lunch theorem in ML?
**A:** The no free lunch theorem states that no single machine learning algorithm is universally better than any other across all possible problems. Performance depends on the specific problem, data distribution, and evaluation metric. Algorithm selection requires experimentation.
**Code:**
```python
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

# Compare algorithms on YOUR data; no universal winner exists
for clf in [LogisticRegression(), RandomForestClassifier(), SVC()]:
    scores = cross_val_score(clf, X, y, cv=5)
    print(type(clf).__name__, scores.mean())
```

## Q99: What are the signs of a well-trained model?
**A:** Signs include: low and stable training/validation loss, small gap between training and validation metrics, good performance on held-out test data, sensible predictions, robustness to input perturbations, and calibration (confidence matches accuracy).
**Code:**
```python
train_loss, val_loss = history["train_loss"][-1], history["val_loss"][-1]
gap = val_loss - train_loss

well_trained = train_loss < 0.1 and gap < 0.02 and test_acc > 0.9
print(f"train={train_loss:.3f} val={val_loss:.3f} test_acc={test_acc:.3f}")
print("well-trained:", well_trained)
```

## Q100: What is the future of model training?
**A:** Future directions include: efficient training techniques (sparse training, mixture of experts), training with synthetic data, self-supervised and foundation models, hardware-software co-design, automated ML (AutoML), federated learning (privacy-preserving), and sustainable AI (energy-efficient training).
**Code:**
```python
# Federated learning: train locally on devices, aggregate only the updates
import torch.distributed as dist

def federated_round(clients, server_model):
    updates = []
    for client in clients:
        w = train_on_client(client, server_model.state_dict())   # private data stays local
        updates.append(w)
    agg = {k: torch.stack([u[k] for u in updates]).mean(0) for k in updates[0]}
    server_model.load_state_dict(agg)                            # federated averaging
    return server_model
```
