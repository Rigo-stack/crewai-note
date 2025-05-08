```markdown
- **Q: What is the purpose of cost in neural networks?**  
  **A:** Cost measures how wrong our machine's predictions are.

- **Q: Define a scalar, vector, and matrix in the context of neural networks.**  
  **A:** A scalar is a single number (often for biases), a vector is an array of numbers (representing single-layer activations), and a matrix is a two-dimensional table of numbers used for weights between layers.

- **Q: What does the power rule in calculus state?**  
  **A:** The power rule states that the derivative of \( x^n \) is \( n \cdot x^{n-1} \).

- **Q: How does gradient descent function in a neural network?**  
  **A:** Gradient descent uses the gradient of the cost function \( \nabla C \) to update model parameters (weights and biases) in the direction that most decreases cost.

- **Q: What is the structure of a neural network?**  
  **A:** A neural network consists of layers of nodes (neurons) connected by weights and biases, where each node in one layer connects to every node in the next layer.

- **Q: How do we perform feed-forward in a neural network?**  
  **A:** Feed-forward is performed by computing \( z = W^{[l]} \cdot a^{[l-1]} + b^{[l]} \) and then passing \( z \) through a nonlinear activation function \( g(z) \).

- **Q: What is the sigmoid function and its range?**  
  **A:** The sigmoid function is defined as \( g(z) = \frac{1}{1 + e^{-z}} \) and compresses input to the range (0, 1).

- **Q: How does vectorization improve neural network training?**  
  **A:** Vectorization allows processing of \( m \) training samples at once by arranging input data \( X \) as an \( n \times m \) matrix.

- **Q: What are common cost functions used in neural networks?**  
  **A:** Common cost functions include mean squared error (MSE), root mean squared error (RMSE), mean absolute error (MAE), and binary cross-entropy for binary outcomes.

- **Q: What is backpropagation in the context of training a neural network?**  
  **A:** Backpropagation is the algorithm that trains the network by computing the gradients \( \frac{\partial C}{\partial W^{[l]}} \) and \( \frac{\partial C}{\partial b^{[l]}} \) via the chain rule.

- **Q: How do convex and non-convex cost functions differ?**  
  **A:** Convex cost functions have a single global minimum, while non-convex functions can have multiple local minima.

- **Q: What is the significance of the learning rate \( \alpha \) in gradient descent?**  
  **A:** The learning rate \( \alpha \) controls the size of each update step, and it typically varies, often chosen through experimentation.

- **Q: What should be monitored to prevent overfitting while training a neural network?**  
  **A:** Monitor performance on validation data to mitigate the risk of overfitting, which occurs when the model performs well on training data but poorly on unseen data.

- **Q: What steps are involved in building a neural network from scratch?**  
  **A:** Initialize weights and biases randomly, perform feed-forward to compute predictions, compute cost, repeat backpropagation for parameter updates, and monitor the cost until convergence.

- **Q: Why must activation functions be nonlinear?**  
  **A:** Activation functions must be nonlinear to allow the neural network to compute complex functions; if linear, the entire network would behave like a single-layer model.
```

This set of flashcards encapsulates essential concepts and facts pertaining to building a neural network from scratch, facilitating effective studying through active recall techniques.