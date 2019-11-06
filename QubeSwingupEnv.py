import numpy as np
from gym_brt.envs.rendering import QubeRenderer

# from bonsai import qube_swingup_policy

qube_swingup_policy = lambda x: np.clip(np.random.randn() * 0.1, -3, 3)


def next_state(state, action, dt=0.004):
    theta, alpha, theta_dot, alpha_dot = state

    # Physical constants from system
    Rm, kt, km = 8.4, 0.042, 0.042  # Motor
    mr, Lr, Dr = 0.095, 0.085, 0.00027  # Rotary arm
    mp, Lp, Dp = 0.024, 0.129, 0.00005  # Pendulum arm
    Jr = mr * Lr ** 2 / 12
    Jp = mp * Lp ** 2 / 12
    g = 9.81

    # Calculate the derivative of the state
    # fmt: off
    theta_dot_dot = float((-Lp*Lr*mp*(-8.0*Dp*alpha_dot + Lp**2*mp*theta_dot**2*np.sin(2.0*alpha) + 4.0*Lp*g*mp*np.sin(alpha))*np.cos(alpha) + (4.0*Jp + Lp**2*mp)*(4.0*Dr*theta_dot + Lp**2*alpha_dot*mp*theta_dot*np.sin(2.0*alpha) + 2.0*Lp*Lr*alpha_dot**2*mp*np.sin(alpha) - 4.0*(-(km * (action - km * theta_dot)) / Rm)))/(4.0*Lp**2*Lr**2*mp**2*np.cos(alpha)**2 - (4.0*Jp + Lp**2*mp)*(4.0*Jr + Lp**2*mp*np.sin(alpha)**2 + 4.0*Lr**2*mp)))
    alpha_dot_dot = float((2.0*Lp*Lr*mp*(4.0*Dr*theta_dot + Lp**2*alpha_dot*mp*theta_dot*np.sin(2.0*alpha) + 2.0*Lp*Lr*alpha_dot**2*mp*np.sin(alpha) - 4.0*(-(km * (action - km * theta_dot)) / Rm))*np.cos(alpha) - 0.5*(4.0*Jr + Lp**2*mp*np.sin(alpha)**2 + 4.0*Lr**2*mp)*(-8.0*Dp*alpha_dot + Lp**2*mp*theta_dot**2*np.sin(2.0*alpha) + 4.0*Lp*g*mp*np.sin(alpha)))/(4.0*Lp**2*Lr**2*mp**2*np.cos(alpha)**2 - (4.0*Jp + Lp**2*mp)*(4.0*Jr + Lp**2*mp*np.sin(alpha)**2 + 4.0*Lr**2*mp)))
    # fmt: on

    # Euler integration: x[k+1] = x[k] + x_dot[k] * dt
    theta += theta_dot * dt
    alpha += alpha_dot * dt
    theta_dot += theta_dot_dot * dt
    alpha_dot += alpha_dot_dot * dt

    # Normalize between -pi and pi
    theta = ((theta + np.pi) % (2 * np.pi)) - np.pi
    alpha = ((alpha + np.pi) % (2 * np.pi)) - np.pi

    return theta, alpha, theta_dot, alpha_dot


class QubeSwingupEnv:
    def __init__(self):
        self.state = [0, 0, 0, 0]
        self._viewer = QubeRenderer(0.0, 0.0, 250)

    def reward(self):
        theta = self.state[0]
        alpha = self.state[1]
        reward = 1 - (0.8 * np.abs(alpha) + 0.2 * np.abs(theta)) / np.pi
        return reward

    def terminal(self):
        theta = self.state[0]
        terminal = False
        terminal |= abs(theta) > (90 * np.pi / 180)
        return terminal

    def reset(self):
        # Start the pendulum stationary at the top (stable point)
        self.state = [0, 0, 0, 0] + np.random.randn(4) * 0.01
        reward = 0
        terminal = False
        return self.state, reward, terminal

    def step(self, action):
        self.state = next_state(self.state, action)
        reward = self.reward()
        terminal = self.terminal()
        return self.state, reward, terminal

    def render(self):
        theta = self.state[0]
        alpha = self.state[1]
        self._viewer.render(theta, alpha)


def main():
    num_episodes = 1200
    num_steps = 2500  # 10 seconds if frequency is 250Hz/period is 0.004s
    env = QubeSwingupEnv()

    for episode in range(num_episodes):
        state, reward, terminal = env.reset()

        for step in range(num_steps):
            action = qube_swingup_policy(state)
            state, reward, terminal = env.step(action)
            print(state)
            env.render()
            if terminal:
                break


if __name__ == "__main__":
    main()
