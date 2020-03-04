# demo-conference.py tutorial

This is a tutorial on how to use the `demo-conference.py` to demonstrate the Qube to an audience.
Make sure to read `setup.md` prior to this tutorial.


## Modes
There are four modes for the demo:
- Fully manual
- 'Cheat' mode
- Combined classical control
- Reinforcement Learning mode

#### Fully manual (red/`B` button)
This is controlled only by the Xbox controller.

Simply move one of the two joysticks left or right (only one joystick can be activated at any time--this is for people that may be right/left handed).

#### 'Cheat' (yellow/`Y` button)
This is the same as manual mode, but whenever the pendulum arm (the red rod on the Qube) is within +/- 20 degrees of upright, it turns off the Xbox controller and uses a 'PID' (or proportional, integral, derivative) controller to balance the Qube. 

The PID controller uses differential equations to solve the control problem. https://en.wikipedia.org/wiki/PID_controller

#### Combined classical control (green/`A` button)
This does not give any control to the user. Combined classical control uses two separate algorithms to do the combined swingup and balance tasks. 

The first is the same as in cheat. Within +/- 20 degrees of the pendulum arm being upright, the PID controller is turned on to do the 'balance' portion.

Outside of that range, the system switches to an 'energy' controller. This essentially tries to increase the energy of the system to a reference energy. This reference energy is the maximum potential energy (ie the potential energy when the pendulum is inverted) and no kinetic energy.

#### Reinforcement Learning (blue/`X` button)
This mode is a controller trained on a simulation using approximately 2 hours of training.

Some interesting things to note:
- Due to the reward function encouraging doing the swingup quickly, this is **much** faster than the energy controller in the swingup portion of the task. Making the energy controller do this is essentially impossible as the control is just built off of the idea: 'increase energy'.
- Unlike the combined controller this is a single algorithm that does both the swingup and balance. To do this classically you must use **both** the PID and energy controllers.
- The algorithm to train this toy problem is very general! It can be used on any problem as long as you can think of nice rewards and have a simulator.
