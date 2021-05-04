# Central Management Web Application

This is a simple management web portal for the raspberry-pi surveillance clients based
on [django-admin](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/).

## Table of contents

* [Functionality](#functionality)
    * [APIs](#apis-description)
* [Requirements](#requirements)

## Functionality

Assuming that each client unit has the ability to distinguish people entering a property from people leaving it; This
management website provides basic functionality to track and manage a number of client units, add/remove/change pictures
of new people to be tracked, and provide overall statistics of the intermittent logs send from face-detection units
owned by each user.

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

## Requirements

To run this project you would need `python>=3.8`. To install the dependancies you can run
`pip install -r requirements.txt`.
