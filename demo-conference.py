import gym
import pygame
import argparse
import numpy as np

from gym_brt.envs import QubeSwingupEnv
from gym_brt.control import pd_control_policy
from rl_controller import rl_controller


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
BUTTON = {"A": 0, "B": 1, "X": 2, "Y": 3}

STATES = {"manual": 0, "cheat": 1, "rl": 2}
LED = {
    "manual": [1, 0, 0],  # Red
    "cheat": [1, 1, 0],  # Yellow
    "rl": [0, 0, 1],  # Blue
}


class QubeSwingupLEDEnv(QubeSwingupEnv):
    """A swingup environment that supports changing the LEDs for the 3 states"""

    def __init__(self, **kwargs):
        super(QubeSwingupEnv, self).__init__(**kwargs)
        self.led_state = LED["manual"]

    def set_led_state(self, s):
        self.led_state = LED[s]

    def _led(self):
        is_upright = np.abs(self._alpha) < (10 * np.pi / 180)
        if is_upright:
            return [0, 1, 0]
        else:
            return self.led_state


def run(use_simulator=False):
    # Connect to the xbox controller ===========================================
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

    # Open the Qube Environment ================================================
    with QubeSwingupLEDEnv(use_simulator=use_simulator) as env:
        state = env.reset()
        state, reward, done, info = env.step(np.array([0], dtype=np.float64))
        action = 0.0
        axis = 0.0

        # Start off in the manual setting
        game_state = STATES["manual"]

        while True:

            # Get the actions from the xbox controller =========================
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == AXIS["left-thumb-x"]:
                        axis = joystick.get_axis(AXIS["left-thumb-x"])
                    elif event.axis == AXIS["right-thumb-x"]:
                        axis = joystick.get_axis(AXIS["right-thumb-x"])

                if event.type == pygame.JOYBUTTONDOWN:
                    if joystick.get_button(BUTTON["A"]):
                        if game_state == STATES["manual"]:
                            game_state = STATES["cheat"]
                            env.set_led_state("cheat")

                        elif game_state == STATES["cheat"]:
                            game_state = STATES["manual"]
                            env.set_led_state("manual")

                        elif game_state == STATES["rl"]:
                            game_state = STATES["cheat"]
                            env.set_led_state("cheat")

                    elif joystick.get_button(BUTTON["B"]):
                        if game_state == STATES["manual"]:
                            game_state = STATES["rl"]
                            env.set_led_state("rl")

                        elif game_state == STATES["cheat"]:
                            game_state = STATES["rl"]
                            env.set_led_state("rl")

                        elif game_state == STATES["rl"]:
                            game_state = STATES["manual"]
                            env.set_led_state("manual")

            # Do an action depending on your state =============================
            if game_state == STATES["manual"]:
                action = -3.0 * axis
            elif game_state == STATES["cheat"]:
                action = -3.0 * axis
                if abs(state[1]) < (20 * np.pi / 180):
                    action = pd_control_policy(state)
            elif game_state == STATES["rl"]:
                action = rl_controller(state)

            # Run the action in the environment
            state, reward, done, info = env.step(action)
            if use_simulator:
                env.render()


def main():
    # Parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--use_simulator", action="store_true")
    args, _ = parser.parse_known_args()
    run(use_simulator=args.use_simulator)


if __name__ == "__main__":
    main()
