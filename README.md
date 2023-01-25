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

Finalny projekt różni się od początkowego brakiem generowania mapy przestrzeni w której porusza się dron. Kolejną różnicą jest dynamiczna estymacja pozycji znacznika AruCo, zamiast odczytu poznanej wcześniej pozycji.

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
### Start simulation - numer znacznika AruCo podawany jest jako argument w ostatniej komendzie
```
ros2 launch tello_custom start_launch.py 
bash src/tello_ros/tello_gazebo/scripts/two_drones_rc.bash 
python3 src/tello_ros/custom_package/scripts/follower.py
ros2 topic pub /marker_id std_msgs/msg/Int32 data:\ 0\ ```

### Start real drone - numer znacznika AruCo podawany jest jako argument w ostatniej komendzie
```
ros2 launch tello_custom drone.py 
ros2 service call /tello_action tello_msgs/TelloAction "{cmd: 'takeoff'}"
python3 src/tello_ros/custom_package/scripts/follower.py
ros2 topic pub /marker_id std_msgs/msg/Int32 data:\ 0\ ```
