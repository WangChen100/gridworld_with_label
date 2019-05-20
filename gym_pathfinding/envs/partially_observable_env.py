

import numpy as np
import gym

from gym_pathfinding.envs.pathfinding_env import PathFindingEnv
from gym_pathfinding.games.astar import compute_action_planning

GOAL_VALUE = 3


class PartiallyObservablePathFindingEnv(gym.Env):
    """ PartiallyObservableEnv
        -1 = unknown
    """

    def __init__(self, lines, columns, observable_depth, *, grid_type="free", screen_size=(640, 640)):
        self.env = PathFindingEnv(lines, columns, 
            grid_type=grid_type, 
            screen_size=screen_size
        )
        self.observable_depth = observable_depth

        self.observation_space = self.env.observation_space
        self.action_space = self.env.action_space

    def reset(self):
        state = self.env.reset()
        label = action_label(state, self.env.game.player, self.env.game.target)
        return self.partial_state(state), label

    def step(self, action):
        state, reward, done, info = self.env.step(action)
        label = action_label(state, self.env.game.player, self.env.game.target)
        return self.partial_state(state), reward, done, info, label

    def seed(self, seed=None):
        self.env.seed(seed=seed)

    def render(self, mode='human'):
        grid = self.env.game.get_state()
        grid = self.partial_state(grid)

        if (mode == 'human'):
            self.env.viewer.draw(grid)
        elif (mode == 'array'):
            return grid

    def close(self):
        self.env.close()

    def partial_state(self, state):
        return partial_grid(state, self.env.game.player, self.observable_depth)

    
def partial_grid(grid, center, observable_depth):
    """return the centered partial state, place -1 to non-visible cells"""

    i, j = center
    offset = observable_depth

    mask = np.ones_like(grid, dtype=bool)
    mask[max(0, i - offset): i + offset + 1, max(0, j - offset): j + offset + 1] = False

    _grid = np.array(grid, copy=True)
    _grid[mask] = -1
    _grid = stack_map(_grid)  # stack goal map with partial observable map
    return _grid


def create_partially_observable_pathfinding_env(id, name, lines, columns, observable_depth, *, grid_type="free"):

    def constructor(self):
        PartiallyObservablePathFindingEnv.__init__(self, lines, columns, observable_depth, grid_type=grid_type)
    
    env_class = type(name, (PartiallyObservablePathFindingEnv,), {
        "id" : id,
        "__init__": constructor
    })
    return env_class


# Create classes 

sizes = list(range(9, 20, 2)) + [25, 35, 55]
envs = [
    create_partially_observable_pathfinding_env(
        id="partially-observable-pathfinding-{type}-{n}x{n}-d{obs}-v0".format(
            type=grid_type, n=size, obs=obs_depth
        ),
        name="PartiallyObservablePathFinding{type}{n}x{n}d{obs}Env".format(
            type=grid_type.capitalize(), n=size, obs=obs_depth
        ),
        grid_type=grid_type,
        lines=size, 
        columns=size, 
        observable_depth=obs_depth
    ) 
    for grid_type in ["free", "obstacle", "maze"]
    for obs_depth in range(2, 10 + 1)
    for size in sizes 
]

for env_class in envs:
    globals()[env_class.__name__] = env_class


def get_env_classes():
    return envs


def action_label(gridmap, start, goal):
    path, action_planning = compute_action_planning(gridmap, start, goal)
    return action_planning[0]


def stack_map(grid_map,):
    # Goal grid contains something only if the goal is visible
    where_is_goal = grid_map == GOAL_VALUE

    def create_goal_grid(shape, goal_position):
        goal_grid = np.zeros(shape, dtype=np.int8)
        goal_grid[goal_position] = 10
        return goal_grid

    goal_map = create_goal_grid(grid_map.shape, where_is_goal)
    # Stack partial and goal grid
    image = np.stack([grid_map, goal_map], axis=2)
    return image
