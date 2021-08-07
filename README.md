# StetsonHomeAutomation
Home automation (lights, audio, etc) for the Stetson household.

:warning: Abandonware! :warning:

This repo contains the half-finished abandonware attempt at creating a touch-sensitive panel for interacting with various smart home devices in the house.
This was largely abandoned due to issues with the hardware at the house with which this interfaces. 

### Design and Issues
This was designed to run on a raspberry pi with an attached touch screen. This design was successful, but the screen's housing that I purchased was too small by a centimeter, so the screen never fit, and I just never got a new housing. So the unit was sitting on a table with exposed electronics for kids and cats to mess with.

In its current state, it is capable of turning my lights on/off and setting their colors. It is also capable of switching the inputs and outputs on my Onkyo audio receiver with the help of an attached Arduino that has an infrared LED attached to it. You'll see some COM port signals being exchanged between the pi and arduino in some code modules.

One of the features was a plugin system for adding games to one of the panels, allowing people near one of the devices to have a little fun while sitting around. I added a Magic 8-ball app, but never finished the plugin architecture and left code in the `__init__.py`, so ... another thing abandoned.

The kivy UI did work quite handsomely on the PC, but stuttered quite a bit on the RPi which was disappointing. Kivy did present a bit of a barrier since it had so many dependencies that needed to be installed in order to iterate on the code, and no two PCs in my house had the same modules installed. The smartest idea would have been to set up a docker container with python3 and all required modules, including kivy, ready to go on any machine, but I never graduated to that point.

### Future

I hestitate to drop this repo from my github in case I ever come back to it in my free time, especially now that Kivy has matured.  My guess is that, if I ever did pick this up, I'd likely use PyQt since I am so familiar with it and it is supported on so many platforms, but kivy does have its appeal particularly in the realm of mobile.

I also hesitate to leave this in my github repo for fear that it will reflect poorly on my ability to write code, but decided that I'll reconcile that fear with this
*STATEMENT TO POTENTIAL EMPLOYERS*:

This code is in an infantile stage and does not represent my best work. While somewhat functional, it is by no means my best attempt to make something usable, readable, pretty, or representative of my skill.

Ok, be well, all.
