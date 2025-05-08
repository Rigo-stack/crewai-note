```markdown
# Recurrent Neural Networks (RNNs), Clearly Explained!!!

## Overview
- **Definition:** Neural Networks (NN) that work with different amounts of sequential data.
- **Sequential Data:** Data where the order or sequence of elements matters, meaning each data point is dependent on preceding ones.

## Recurrent Neural Networks (RNN)
- **Functionality:** RNNs are designed to handle varying amounts of input values.
- **Components:**
  - Weights
  - Biases
  - Activation Functions
  - Feedback Loops

### Key Features
- **Activation Functions:** Introduce non-linearity to the model.
- **Feedback Loops:** Allow processing of sequential data by passing information from past time steps to present.
- **Output Paths:** Can either go to output or feedback loop.

### Unrolling the Network
- **Unrolling:** Making copies of the neural network for each input value.
- **Weights & Biases:** Shared across all unrolled inputs.

### Training Challenges
- **Vanishing/Exploding Gradient Problem:** Difficulty in training as gradients become extremely small (vanishing) or large (exploding) with unrolling.
- **Gradient Descent:** Optimization algorithm that minimizes a loss function (e.g., sum of squared residuals).

---

## Long Short-Term Memory (LSTM), Clearly Explained

### Overview
- **Definition:** A type of RNN designed to avoid the exploding/vanishing gradient problem.

### Prediction Paths
- **Long-Term Memory Path**
- **Short-Term Memory Path**

### Activation Functions
- **Sigmoid Function:** Outputs between 0 and 1.
- **Tanh Function:** Outputs between -1 and 1.

### Memory States
- **Cell State (Long-Term Memory):** No direct weights or biases interfere, allowing stable flow through units.
- **Hidden State (Short-Term Memory):** Directly connected to modifiable weights.

### Gates in LSTMs
- **Forget Gate:** Decides whether to retain or discard memory.
- **Input Gate:** Controls information passed to the memory cell.
- **Output Gate:** Determines data passed as output.

### Summary
- **Advantages:** Different paths for memory help unroll LSTMs more effectively vs. vanilla RNNs.

---

## Neural Networks Part 5: ArgMax and SoftMax

### ArgMax
- **Functionality:** Sets the highest value to 1 and others to 0, making interpretation easy.
- **Limitations:** Cannot optimize weights/biases (only outputs 0 or 1); poor derivative for backpropagation.

### SoftMax
- **Definition:** Transforms real number vectors into a probability distribution, ensuring total probability equals 1.
- **Properties:** Preserves ranking and outputs range from 0 to 1.

---

## Neural Networks Part 6: Cross Entropy

### Overview
- **Purpose:** Evaluates neural network fit to data.
- **Common Use:** Loss function for multi-class and binary classification.
- **Total Error Calculation:** Adding results of individual cross-entropy computations.
  
### Key Definitions
- **Residuals:** Difference between observed and predicted.

### Loss Comparison
- **Cross Entropy:** Higher loss as probability approaches zero.
- **Sum of Squared Residuals:** Symmetrically treats errors.

---

## Word Embedding and Word2Vec, Clearly Explained!!!

### Basic Concept
- Convert words into numbers by assigning random numbers or using a neural network.

### Methods
1. **Continuous Bag of Words:** Uses surrounding words to predict the middle word.
2. **Skip Gram:** Utilizes the middle word to predict surrounding words.

### Activation Function
- **Identity Activation:** Outputs the input directly, no transformation.

### Optimization
- **Negative Sampling:** Randomly selects words to skip during training to speed up optimization.

---

## Sequence-to-Sequence (seq2seq) Encoder-Decoder Neural Networks, Clearly Explained!!!

### Overview
- **Purpose:** Transform one sequence into another (e.g., translating languages).

### Structure
- **Components:**
  - Encoder (with LSTM layers)
  - Decoder (with LSTM layers)
- **Context Vector:** Contains the encoded representation of the input sequence.

### Functionality
- **End and Start Tokens:** Utilize EOS and SOS for processing efficiency.
- **Training Method:** Harnessing *Teacher Forcing* instead of using predicted tokens.

### Summary
- Encoder-Decoder architecture helps manage variable lengths of input and output sequences effectively with trained weights and biases.

---

## Resources
- [Video 1](https://www.youtube.com/watch?v=AsNTP8Kwu80&t=2s)
- [Video 2](https://www.youtube.com/watch?v=YCzL96nL7j0)
- [Video 3](https://www.youtube.com/watch?v=viZrOnJclY0)
- [Video 4](https://www.youtube.com/watch?v=KpKog-L9veg)
- [Video 5](https://www.youtube.com/watch?v=6ArSys5qHAU)
- [Video 6](https://www.youtube.com/watch?v=L8HKweZIOmg&t=223s)
- [GitHub Repository](https://github.com/bentrevett/pytorch-seq2seq/tree/rewrite)
```