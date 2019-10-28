import gym
import pygame
import argparse
import numpy as np

from gym_brt.envs import QubeSwingupEnv


# All of these are in the range (-1.0, +1.0)
# Thumbs directions are top and right are positive directions
# Triggers are -1.0 when unpressed, +1.0 when fully pressed
AXIS = {
    "left-thumb-x": 0,
    "left-thumb-y": 1,
    "left-trigger": 2,
    "right-thumb-x": 3,
    "right-thumb-y": 4,
    "right-trigger": 5,
}


def run(frequency=250, use_simulator=False, max_time=5): # max time is in seconds until reset
    pygame.init()
    pygame.joystick.init()
    clock = pygame.time.Clock()

    joysticks = []
    # for all the connected joysticks
    for i in range(0, pygame.joystick.get_count()):
        # create an Joystick object in our list
        joysticks.append(pygame.joystick.Joystick(i))
        # initialize them all (-1 means loop forever)
        joysticks[-1].init()
        # print a statement telling what the name of the controller is
        print("Detected joystick '", joysticks[-1].get_name(), "'")
    joystick = joysticks[-1]

    with QubeSwingupEnv(frequency=frequency, use_simulator=use_simulator) as env:
        state = env.reset()
        state, reward, done, info = env.step(np.array([0], dtype=np.float64))
        action = 0.0

        while True:
            # Get the action from the xbox controller
            for event in pygame.event.get():
                if event.axis == AXIS["left-thumb-x"]:
                    axis = joystick.get_axis(AXIS["left-thumb-x"])
                    action = -3.0 * axis

            # Run the action in the environment
            state, reward, done, info = env.step(action)
            if use_simulator:
                env.render()


def main():
    # Parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--frequency",
        "--sample-frequency",
        default="250",
        type=float,
        help="The frequency of samples on the Quanser hardware.",
    )
    parser.add_argument(
        "-mt",
        "--max_time",
        default="5",
        type=float,
        help="The maximum amount of time to wait before doing a reset.",
    )
    parser.add_argument("-s", "--use_simulator", action="store_true")
    args, _ = parser.parse_known_args()

    run(frequency=args.frequency, use_simulator=args.use_simulator, max_time=args.max_time)



if __name__ == '__main__':
    main()