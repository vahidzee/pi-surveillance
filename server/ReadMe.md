# Central Management Web Application

This is a simple management web portal for the raspberry-pi surveillance clients based
on [django-admin](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/).

## Table of contents

* [Functionality](#functionality)
* [Requirements](#requirements)

## Functionality

Assuming that each client unit has the ability to distinguish people entering a property from people leaving it; This
management website provides basic functionality to track and manage a number of client units, add/remove/change pictures
of new people to be tracked, and provide overall statistics of the intermittent logs send from face-detection units
owned by each user.

## Requirements

To run this project you would need `python>=3.8`. To install the dependancies you can run
`pip install -r requirements.txt`.
