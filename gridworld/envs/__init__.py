from gym.envs.registration import register
import gridworld.envs.pathfinding_env
import gridworld.envs.partially_observable_env


for env_class in pathfinding_env.get_env_classes():
    register(
        id=env_class.id,
        entry_point='gridworld.envs.pathfinding_env:{name}'.format(name=env_class.__name__)
    )

for env_class in partially_observable_env.get_env_classes():
    register(
        id=env_class.id,
        entry_point='gridworld.envs.partially_observable_env:{name}'.format(name=env_class.__name__)
    )
