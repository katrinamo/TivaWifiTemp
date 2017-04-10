# TivaWifiTemp
Connects a Tiva Launchpad with a CC3100 to the AT&amp;T M2X IoT service. Asking an Alexa with this skill for the local temperature pings the Launchpad, which returns the temperature using the board sensor. Alexa then responds to the user with the temperature. Users may then instruct Alexa to send a different temperature to the board. As of this version (v0.1), the board merely lights up and LED to acknowledge the different temperature.

## Set Up
# Cloud Service Set Up
To use, first [create an account with AT&T M2X.](https://m2x.att.com/) It has a fairly straightforward API that is easy to manipulate. Any other cloud service can be substituted but be aware that this tutorial uses the AT&T M2X service. 

Next, create two device streams. Past the code found in this directory into Energia. Look for the "Device ID" and "Primary API Key" numbers found on the M2X website and paste them in the code. Then, where "STREAM KEY" is located, replace them with the names of your stream that you want to push values to and pull values from. Finally, replace SSID and password with your network SSID and password. The program is now ready to be interfaced with via Alexa.

This skill is under Certification Review.

The Lamda code is based off of the tutorial code https://www.hackster.io/daquilnp/how-to-publish-an-alexa-skill-from-beginning-to-end-82167c

The specific python code can be found here: https://github.com/daquilnp/alexapi/blob/master/ExamGradeEstimator/exam_grade_estimator.py
