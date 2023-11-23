# Lab2 - Nim game: Agent using Evolutionary strategy

The objective of this second laboratory is to create an agent able to play the nim game. The agent should be using an evolutionary strategy.

I developed three different approaches to this problem, discussed below. For each strategy, more informations and plots are to be found in their respective Jupyter Notebooks.

The results are the average win-rate against the selected agent (1 being my strategy always wins and 0 my stategy always loses)

More details about the implemetation can be found in the respective folders ```readme.md``` and jupyter notebooks.


| **Strategy**                                | Result vs ```pure_random``` | Result vs ```optimal``` | Folder |
|---------------------------------------------|-----------------------------|-------------------------|---|
| Evolutionary Logistic Classifier __(best)__ | 0.893                       | 0.656                   | |
| Evloutionary Neural Networks Classifier     | 0.830                       | 0.590                   | |
| Evolutionary Rule Weighting                 | 0.663                       | 0.420                   | |