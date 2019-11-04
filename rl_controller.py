import numpy as np
import argparse
from rl_weights import w0, b0, w1, b1, wout, bout


def rl_controller(x):
    x = np.asarray(x)
    h0 = np.tanh(x @ w0 + b0)
    h1 = np.tanh(h0 @ w1 + b1)
    return h1 @ wout + bout


def test_rl_controller(use_simulator):
    from gym_brt.envs import QubeSwingupEnv

    with QubeSwingupEnv(use_simulator=use_simulator, frequency=250) as env:
        while True:
            state = env.reset()
            state, _, done, _ = env.step(np.array([0]))

            while not done:
                action = rl_controller(state)
                state, _, done, _ = env.step(action)
                if use_simulator:
                    env.render()


if __name__ == "__main__":
    # Parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--use_simulator", action="store_true")
    args, _ = parser.parse_known_args()
    test_rl_controller(args.use_simulator)
