# ThirdEyeServer

###Overview
ThirdEye is a continuous authentication system for Facebook on the Google Chrome web browser. The system comprises of a Chrome [extension] and this server. ```NOTE!``` The server repository is to display its codebase and cannot be used in production because the ThirdEye extension are hardcoded to communicate with our server instance. 

###Description 
The server is responsible for three primary tasks:
- Central storage point for all user collected data.
- Notification generating service.
- A platform for anomaly detection algorithms.

###Technical
####System
The server is written in python's microwebframework [Flask]. By default, it runs on port 5000 and has the following end points (routes):
- /submit : This collects,logs and stores data sent by the ThirdEye extension. A user notification is generated if an anomaly is detected.
- /email : This endpoint receives and stores client's email and generates a user notification for successful installation.
- /uninstall : This endpoint is called at extension uninstallation to generate user notification for uninstallation

####Storage
The server uses MongoDB as storage database. The user database is organized as a unique collection for each client extension. Each Facebook action is stored as an indivdual document.

####Notification
The server uses python's SMTP module to send email notification to users. Connection to mailserver is secured using SSL.

####Design
The server exposes a standard API to allow seamless integration of multiple anomaly detection algorithms. ```detection_system.py``` defines an abstract base class (ABC) which algorithm implementations are expected to override.  The two primary calls are :
- new_entry: This function is called by the server for each individual event/action received.
- alarm: This function is called by a detection algorithm when it wants to send a notification to the user.

###Installation Instructions
####Requirements
The server is cross platform and requires Python 2.7 and MongoDB installed on your system. 

####Steps
- Download the repository and unzip to a desired location
- Navigate and open ```detection_system.py``` and scroll to line 70 - 75.
- Add your SMTP details including mailserver, port, email address, mail server login and mail server password
- Run the server with the following command ```python server.py```

[extension]: <https://github.com/ThirdEyeDetect/ThirdEyeExtension>
[Flask]: <http://flask.pocoo.org/>
