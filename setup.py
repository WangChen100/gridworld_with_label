from setuptools import setup

setup(name='gridworld',
      description='GridWorld who inherits from Gym environnement is made for interactive pathfinding.',
      version='0.0.1',
      install_requires=['gym>=0.9.7', 'cython', 'numpy', 'scipy', 'pygame'],
      packages=['gridworld', 'gridworld.envs', 'gridworld.games'],
      author='Chen Wang',
      url='https://github.com/WangChen100/gridworld_with_label'
)
