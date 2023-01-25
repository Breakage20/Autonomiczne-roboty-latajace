# Autonomiczne-roboty-latajace

Autorzy:
Błażej Gawędzki
Piotr Michałek
Mikołaj Piaszczyński

## To build dockerfile use 
```
bash build.sh
```
## In order to create container with neccesary config use
```
bash create_container.sh
```
## To open new docker window use
```
bash open_new.sh
```
### Start simple simulation
```
ros2 launch tello_gazebo simple_launch.py
```

### Liftoff drone
```
bash src/tello_ros/tello_gazebo/scripts/two_drones_rc.bash 
```
