# vehicle control by eyes

## Intallation

1- Install Dlib and Cmake [link]([https://cmake.org/install/](https://www.geeksforgeeks.org/how-to-install-dlib-library-for-python-in-windows-10/)).

2- run ```python main.py``` to start the program.

## How it work

The code is build by using opencv and Dlib library, it recognize the face then take the eyes point as ROI to apply sepacific filters on it.

After applying filters it script take the region of iris and set a command based on this region.

#### Commands:
1- ST -> stop

2- R -> right

3- L -> left

4- FW -> forward

5- BW -> back
