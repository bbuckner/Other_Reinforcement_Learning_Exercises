This project utilizes a Deep Q-Learning RL Architecture to teach an agent to reach a desired quantum state with 3 qbits.

Action Space:<br>
![](images/action_space.PNG)

State Space:<br>
List of 8 amplitude probabilities representing distribution of outcomes for 3 qbits.<br>
The indexes represent the probability of getting outcomes 000, 001, 010, 011, 100, 101, 110, and 111 respectively.<br>
For example, the following distribution would be represented by [0, 0, 0.514, 0, 0, 0, 0, 0.486]:<br>
![](images/example_state.PNG)<br>


