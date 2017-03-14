# TivaWifiTemp
Connects a Tiva Launchpad with a CC3100 to the AT&amp;T M2X IoT service. To use, first create an account with AT&T M2X. Next, create two device streams. Past the code found in this directory into Energia. Look for the "Device ID" and "Primary API Key" numbers found on the M2X website and paste them in the code. Then, where "STREAM KEY" is located, replace them with the names of your stream that you want to push values to and pull values from. Finally, replace SSID and password with your network SSID and password. The program is now ready to be interfaced with via Alexa.

This skill is under Certification Review.

The Lamda code is based off of the tutorial code https://www.hackster.io/daquilnp/how-to-publish-an-alexa-skill-from-beginning-to-end-82167c

The specific python code can be found here: https://github.com/daquilnp/alexapi/blob/master/ExamGradeEstimator/exam_grade_estimator.py
