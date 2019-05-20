from setuptools import setup

setup(name='gridworld',
      description='GridWorld who inherits from Gym environnement is made for interactive pathfinding.',
      version='0.0.1',
      install_requires=['gym>=0.9.7', 'cython', 'numpy', 'scipy', 'pygame'],
      packages=['gym_pathfinding', 'gym_pathfinding.envs', 'gym_pathfinding.games'],

      author='Chen Wang',
      url='https://github.com/DidiBear/gym-pathfinding'
)
