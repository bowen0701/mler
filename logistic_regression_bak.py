from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np


def sigmoid(x):
    """Compute the sigmoid of x.

    Args:
      x: A scalar or numpy array of any size.

    Returns:
      s: sigmoid(x).
    """
    s = 1 / (1 + np.exp(-x))    
    return s

def sigmoid_derivative(s):
    """Compute the gradient of the sigmoid function.
    
    Args:
      s: A scalar or numpy array. Sigmoid function.

    Returns:
      ds: Computed gradient.
    """
    ds = s * (1 - s)    
    return ds


def initialize_weights(dim):
    """Initialize weights.

    This function creates a vector of zeros of shape (dim, 1) for w and b to 0.
    
    Args:
      dim: A integer. Size of the w vector (or number of parameters.)
    
    Returns:
      w: A Numpy array. Initialized vector of shape (dim, 1)
      b: A integer. Initialized scalar (corresponds to the bias)
    """
    w = np.zeros(dim).reshape(dim, 1)
    b = 0
    assert(w.shape == (dim, 1))
    assert(isinstance(b, float) or isinstance(b, int))
    return w, b


def propagate(w, b, X, Y):
    """Forward & backward propagation.

    Implement the cost function and its gradient for the propagation.

    Args:
      w: A Numpy array. Weights of size (num_px * num_px * 3, 1)
      b: A float. Bias.
      X: A Numpy array. Data of size (num_px * num_px * 3, number of examples).
      Y: A Numpy array. True "label" vector (containing 0 or 1) 
         of size (1, number of examples).

    Returns:
      cost: A float. Negative log-likelihood cost for logistic regression.
      dw: A Numpy array. Gradient of the loss w.r.t. w, thus same shape as w.
      db: A float. Gradient of the loss w.r.t b, thus same shape as b.
    """
    m = X.shape[1]
    
    # Forward propagation from X to cost.
    # Compute activation.
    A = sigmoid(np.dot(w.T, X) + b)
    # Compute cost.
    cost = - 1 / m * np.sum(Y * np.log(A) + (1 - Y) * np.log(1 - A))
    
    # Backward propagation to find gradient.
    dw = 1 / m * np.dot(X, (A - Y).T)
    db = 1 / m * np.sum(A - Y)

    assert(dw.shape == w.shape)
    assert(db.dtype == float)

    cost = np.squeeze(cost)
    assert(cost.shape == ())

    grads = {"dw": dw,
             "db": db} 

    return grads, cost


def optimize(w, b, X, Y, num_iterations, learning_rate, print_cost=False):
    """Optimization function.

    This function optimizes w and b by running a gradient descent algorithm.
    That is, write down two steps and iterate through them:
      1. Calculate the cost and the gradient for the current parameters. 
        Use propagate().
      2. Update the parameters using gradient descent rule for w and b.
    
    Args:
      w: A Numpy array. Weights of size (num_px * num_px * 3, 1).
      b: A scalar. Bias.
      X: A Numpy array. Data of shape (num_px * num_px * 3, number of examples).
      Y: A Numpy array. True "label" vector (containing 0 if non-cat, 1 if cat), 
        of shape (1, number of examples)
      num_iterations: A integer. Number of iterations of the optimization loop.
      learning_rate: A scalr. Learning rate of the gradient descent update rule.
      print_cost: A Boolean. Print the loss every 100 steps. Default: False.
    
    Returns:
      params: A dictionary containing the weights w and bias b.
      grads: A dictionary containing the gradients of the weights and bias 
        with respect to the cost function
      costs: A list of all the costs computed during the optimization, 
        this will be used to plot the learning curve.
    """   
    costs = []

    for i in range(num_iterations):
        # Cost and gradient calculation (≈ 1-4 lines of code)
        grads, cost = propagate(w, b, X, Y)
        
        # Retrieve derivatives from grads
        dw = grads.get('dw')
        db = grads.get('db')
        
        # Update rule.
        w -= learning_rate * dw
        b -= learning_rate * db
        
        # Record the costs
        if i % 100 == 0:
            costs.append(cost)
        # Print the cost every 100 training examples
        if print_cost and i % 100 == 0:
            print("Cost after iteration %i: %f" %(i, cost))
    
    params = {"w": w,
              "b": b}
    
    grads = {"dw": dw,
             "db": db}
    
    return params, grads, costs


def predict(w, b, X):
    """Prediction.

    Predict whether the label is 0 or 1 using learned logistic regression 
    parameters (w, b)
    
    Args:
      w: A Numpy array. Learned weights of size (num_px * num_px * 3, 1).
      b: A scalar. Learned bias.
      X: A Numpy array. New data of size (num_px * num_px * 3, number of examples).
    
    Returns:
      Y_prediction: A Numpy array containing all predictions (0/1) 
        for the examples in X.
    """
    m = X.shape[1]
    Y_prediction = np.zeros((1, m))
    w = w.reshape(X.shape[0], 1)
    
    # Compute vector "A" predicting the probabilities of a label 1 
    # being present in the picture.
    A = sigmoid(np.dot(w.T, X) + b)
    
    for i in range(A.shape[1]):
        # Convert probabilities a[0,i] to actual predictions p[0,i]
        if A[0, i] > 0.5:
            Y_prediction[0, i] = 1
        else:
            Y_prediction[0, i] = 0
    
    assert(Y_prediction.shape == (1, m))
    
    return Y_prediction


def accuracy(Y_prediction, Y):
    acc = 1 - np.mean(np.abs(Y_prediction_train - Y_train))
    return acc


def logistic_regression(X_train, Y_train, X_test, Y_test, 
                        num_iterations=2000, learning_rate=0.5, print_cost=False):
    """Wrap-up function for logistic regression.

    Builds the logistic regression model by calling the function 
    you've implemented previously.
    
    Args:
      X_train: A Numpy. Training set of shape (num_px * num_px * 3, m_train).
      Y_train: A Numpy array. Training labels of shape (1, m_train).
      X_test: A Numpy array. Test set of shape (num_px * num_px * 3, m_test).
      Y_test: A Numpy array. Test labels of shape (1, m_test).
      num_iterations: An integer. Hyperparameter for the number of iterations 
        to optimize the parameters
      learning_rate: A scalar. Hyperparameter for the learning rate used 
        in the update rule of optimize()
      print_cost: A Boolean. Print the cost every 100 iterations. Default: True.
    
    Returns:
      d: A dictionary containing information about the model.
    """    
    # initialize parameters with zeros (≈ 1 line of code)
    w, b = initialize_with_zeros(X_train.shape[0])

    # Gradient descent.
    parameters, grads, costs = optimize(
        w, b, X_train, Y_train, 
        num_iterations=num_iterations, learning_rate=learning_rate, 
        print_cost=print_cost)
    
    # Retrieve parameters w and b from dictionary "parameters"
    w = parameters.get('w')
    b = parameters.get('b')
    
    # Predict test/train set examples (≈ 2 lines of code)
    Y_prediction_test = predict(w, b, X_test)
    Y_prediction_train = predict(w, b, X_train)

    # Print train/test Errors
    print("Train accuracy: {} %"
          .format(accuracy(Y_prediction_train, Y_train) * 100))
    print("Test accuracy: {} %"
          .format(accuracy(Y_prediction_test, Y_test) * 100))
    
    d = {"costs": costs,
         "Y_prediction_test": Y_prediction_test, 
         "Y_prediction_train" : Y_prediction_train, 
         "w" : w, 
         "b" : b,
         "learning_rate" : learning_rate,
         "num_iterations": num_iterations}
    return d