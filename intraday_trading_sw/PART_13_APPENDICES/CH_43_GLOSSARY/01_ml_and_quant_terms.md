# 01 — ML and Quant Terms Glossary

## Purpose
Define the modeling and quantitative terminology used in Parts 04, 05, and 16.

## Data & features
- **Feature**: a numeric input to a model (CH_09).
- **Feature engineering**: constructing informative inputs.
- **Look-ahead bias / leakage**: using future information in a feature.
- **Target/label**: the value a model is trained to predict (CH_16/00).
- **Normalization/scaling**: transforming features to comparable ranges.
- **Imputation**: filling missing values (per policy, CH_09/04).

## Model & validation
- **Overfitting**: fitting noise; great in-sample, poor out-of-sample.
- **Underfitting**: too simple to capture real signal.
- **Train / validation / test**: time-ordered splits (CH_19/00).
- **Walk-forward**: rolling retrain-and-test evaluation (CH_19/01).
- **Cross-validation**: resampling evaluation — random CV forbidden for time
  series (CH_19/00).
- **Calibration**: how well predicted probabilities match observed frequencies.
- **Brier score**: mean squared error of probabilities.
- **AUC / ROC**: ranking quality of a classifier.
- **Precision / recall**: per-class correctness measures.
- **Bootstrap / permutation test**: resampling significance methods (CH_18/02).

## Performance
- **Sharpe ratio**: return per unit of volatility (CH_18/01).
- **Sortino ratio**: return per unit of downside deviation.
- **Calmar ratio**: annualized return / max drawdown.
- **Max drawdown**: worst peak-to-trough decline.
- **VaR / CVaR**: tail-risk measures (CH_18/01).
- **Expectancy**: average net profit per trade (CH_18/00).

## Model types
- **Logistic regression**: linear probabilistic classifier (CH_15/01).
- **Decision tree / Random Forest / Gradient Boosting**: tree ensembles (CH_15/03).
- **Reinforcement learning**: learns a policy from rewards (CH_15/04).
- **Regime**: market condition; regime models/gates (CH_10/01, CH_13/04).
- **Drift**: when live data/model behavior deviates from training (CH_16/03).
