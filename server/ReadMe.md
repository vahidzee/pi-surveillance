# Central Management Web Application

This is a simple management web portal for the raspberry-pi surveillance clients based
on [django-admin](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/).

## Table of contents

* [Functionality](#functionality)
    * [Web Application](#web-application)
    * [APIs](#apis-description)
* [Requirements](#requirements)

## Functionality

Assuming that each client unit has the ability to distinguish people entering a property from people leaving it; This
management website provides basic functionality to track and manage a number of client units, add/remove/change pictures
of new people to be tracked, and provide overall statistics of the intermittent logs send from face-detection units
owned by each user.

### Web Application

Through the provided web application user interface, users can sign up and manage their face-detector devices all in a
single platform. After a face-detector client is connected to the internet, it will automatically contact the central
management system announcing its livelihood. The owner can then register his/her device by entering the
unique `device_id` which is provided for each device. After than the claimed device will automatically start sending
updates on the passerby movements and potentially newly observed faces.

After creating an account (by logging on) and signing in to the platform, three main menus are noticeable:

1. **Devices**: Through this menu users can register new face-detector devices, provide and edit custom names for
   registered devices (to help with tracking their location & etc.), and follow overall statistics such as _last update_
   or _number of people inside_ which can be beneficial for many things such as social distancing controlling.

2. **Faces**: This menu provides the necessary functionality to add and manage the observed faces. Users can add custom
   images of people to be tracked by face-detector devices. If the provided image, is of more than one people, the
   picture is automatically processed and cropped into sub images each holding only one face inside. Then each image is
   compared with the old set of images in the database to prevent the repetitive registry of different images of the
   same people.

   In addition to the faces that users manually submit, this menu lists all the new faces that user-owned face-detectors
   will observe overtime. It is possible to add an arbitrary name for each face to help with easier tracking.

   Finally, an overall statistic of where the user was last observed is shown to depict each person's most recent
   location.

### APIs Description

All correspondence is done with JSON HTTP Requests. The following is a list of utilized API endpoints and a short
description of their functionalities:

* **hello**: Upon its connection to internet, each face-detection device employs this API endpoint to announce its
  presence to the central management system while sending its unique `device_id`. In return the server responds with a
  temporary
  `access_token`. Using a valid token, clients can interact with other API endpoints seamlessly. Due to security reasons
  each token's validity will be automatically deprecated upon changes of client's initial IP address, or after a day
  since its creation. Devices should renounce their presence through **hello** once their `access_token` has been
  invalidated.

  It should be mentioned that until the device is not claimed by a user through the UI of the management system, No
  access token is provided to the newly connected device and the error message _Device is yet to be claimed by a user_
  will be returned.

  After the device has successfully acquired a valid access token, it will update its local stack of `face_embeddings`
  by employing the **fetch** API endpoint.

## Requirements

To run this project you would need `python>=3.8`. To install the dependancies you can run
`pip install -r requirements.txt`.
