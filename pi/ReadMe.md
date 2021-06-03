# Pi Client

This is an implementation of the surveillance functionalities in python3 for Raspberry Pi.

## Table of contents

* [Functionality](#functionality)
    * [`SmartCamera` Class](#smartcamera-class)
    * [`Client` Class](#client-class)
    * [`Manager` Class](#manager-class)
* [Requirements](#requirements)

## Functionality  

The client is able to record a picture when it senses motion with the PIR sensors. The picture is then scanned for 
faces. Faces that are unknown will be sent to the serverto be stored for security. 

### `SmartCamera` Class

This class saves the embeddings and IDs of faces known to the server. Upon the triggeringof the motion sensors, A 
picture will be taken and each detected face will be reported tothe server. If any of the detected faces were unknown, 
they will introduced to the server.
 
### `Client` Class

This class handles all communications with the server. At the beginning, this class initiates a session with the server.
A unique ID is needed for each device to communicate with the sever. Here, the CPU serial number was extracted as the 
unique ID. If the server doesn't recognise this ID as a registered ID, a session won't be initiated until the device is 
registered by the admin. In this case, the unique ID will be displayed on the LCD to assist the admin in the 
registration process. After the successful initialization of a session, a token (i.e. a session key) will be returned to
the client. This token expires after some time so the client re-establishes the session automatically. With this token, 
the client can now fetch the known faces, introduce new faces, and send logs to the server.

### `Manager` Class

This class is responsible for handling the IO inputs and coordinating between the camera and the client. At any given 
time, The total number of people and the name of the last passing person is displayed on the LCD by the manger.

## Requirements

To run this project you would need `python3`. To install the dependencies you can run
`pip3 install -r requirements.txt`.

If you wish to try out the project (development-test) follow the steps bellow:

1. Install dependencies:

```shell
pip3 install -r requirements.txt
```

2. Run the codee:

```shell
python3 main.py
```
Please note that in the above code, the right PIR sensor was connected to pin `23` and the left PIR sensor was connected
to pin `24`. If your circuit has a different pinout setup, change the `pir_r` and `pir_l` variables in `main.py` 
accordingly.

The LCD driver code was taken from [this gist](https://gist.github.com/DenisFromHR/cc863375a6e19dce359d).