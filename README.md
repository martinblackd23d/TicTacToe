# TicTacToe
Neural network to evaluate TicTacToe positions

The entire code was written by me, in Python. As a result, it is really slow, and while scaling is theoretically possible, it is highly impractical. Consequently, it is incredibely inaccurate. It mainly serves as a proof of concept, before I start learing dedicated machine learning libraries, or try to build a neural network in a more efficient language

First I built a game tree to create a database of all valid positions and whether they are winning or not.

For simplicity, I only trained the AI to play as the player who goes first. Additionally, I excluded every losing position, because perfect strategy doesn't make sense there. I initially planned to evaluate losing positions based on probability of winning, depending on the opponents moves, but I ulitmately didn't implement it.

In every position, I calculated the list of optimal moves, based on the optimal strategy found on [wikipedia.](https://en.wikipedia.org/wiki/Tic-tac-toe#Strategy)
I then trained the neural network to evaluate these individual positions.

## Structure of neural network
Simple feedforward neural network

9 input nodes, with 3 possible inputs: X, O, empty

9 output nodes, the final move played is the largest number in the output

1 hidden layer with 9 nodes

Activation function: I tried linear, binary step, sigmoid, ReLU and Leaky ReLU activation functions, while performance didn't change significantly, sigmoid slightly outperformed the others

Later in development, bias was also added to be changed along with the weigths

The loss function was the percentage of positions, where the neural networks single largest output was part of the optimal moves in that position.

The learning rate was adjusted several times, with the different networks having different rates within the same generation. This was meant to ensure that a particularly unlucky generation still doesn't lose it's progress. This was a theoretical possibility because of the limited number of nets trained simultaniously.

I considered reserving a portion of the database for evaluation, but due to the already limited size of the dataset, and considering that it included every possible position anyway, I thought overfitting wouldn't be an issue.
For now, it does not include backpropagation

## Results
10 nets trained simultaneously

10 generations

out of 2300 positions, randomly initialized networks on average got around 1000 correct

over the course of the training, the nets' results converged to around 1300 correct

## Future improvements
Rewriting entire code in a more efficient language.

Increasing number of neurons and/or layers

Increasing number of nets trained and generations

Include backpropagation for faster training
