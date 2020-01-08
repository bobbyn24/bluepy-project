# ubc-mentorship
Python script that interfaces with the TI CC2650 SensorTag microcontroller, specifically its inertial measurement unit (IMU) which contains 3 sensors (gyroscope, accelerometer, magnetometer). The Bluetooth Low Energy (BLE) wireless personal area network protocol is used to communicate data (with the help of [the Python bluepy library](http://ianharvey.github.io/bluepy-doc/ "Bluepy Documentation")) to a Raspberry Pi 3 computer. The data is then used to create 3D simulation of the SensorTag's rotation, which is strapped to the subject's abdomen.

![Position on abdomen](sensortag-position.png)

Created as a part of the Sensory Information Technologies for Sleep Monitoring Research Project at the Advanced Materials and Process Engineering Laboratory.

*Thank You To:*  
Professor John Madden  
Ezequiel Hernandez  
Professor Edmond Cretu
