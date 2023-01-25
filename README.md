# Autonomiczne-roboty-latajace

Autorzy:

Błażej Gawędzki 140348,

Piotr Michałek 140281,

Mikołaj Piaszczyński 140359

Temat: **Budowa mapy otoczenia przy użyciu znaczników AruCo**

Podczas prac nad projektem zostały zrealizowane takie zagadnienia jak:
- zbudowanie zbudowanie work space'a dla drona DJI Ryze Tello w ROS2
- umieszczenie znaczników AruCo w symulacji Gazeboo
- zbudowanie node'a do odczytu wartości ze znaczników AruCo
- wizualizacja TF-ów znaczników oraz drona.
- odczyt pozycji i orientacji znaczników względem drona
- lot drona do znacznika na podstawie odczytu pozycji i orientacji znacznika
- zadawanie prędkości liniowych i obrotowych za pomocą regulatora PID
- odnajdywanie obiektów i śledzenie ich zgodnie z poleceniami operatora

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
