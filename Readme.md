# Sourcebots Robot

This is the source code for a robot I built as part of a team at the Southampton university Source Bots Computer Science and Electronics Labs.

# Info

This is the code for a robot that I built as part of a team of 4 over the course of 5 days that contained very long hours and very little sleep.
The software was completely written by me apart from one function in the utils section that I "borrowed" from stackoverflow because I was too tired to figure out the intersection point of two circles (the function is called "get_intersections").

It uses the sbot and j5 api to control the motors, sensors and parse data from the camera to read the location of AprilTags (funky QR code looking things) but everything else is handled by this code. (sbot docs - https://docs.sourcebots.co.uk/)

The code this robot ran on made it through to the grand finals and ended up coming 4th out of the 10 starting teams, however it did win the Staff Pick/Best design and software Award (The only non-point based award, the other awards were for 1st, 2nd and 3rd).

The main issue with this code is that it wasn't tested enough, this was partially my fault but also due to how little testing time we had in the actual arena (approximately an hour in total prior to the first match), and a testimony to this is how the constant tweaks I made very quickly inbetween rounds brought it up from dead last in it's first two matches to first in it's third, fifth, quarter and semi final rounds.

# The score sheet:

| League rounds                        | Quarter Finals | Semi Finals | Grand Finals |
| ------------------------------------ | -------------- | ----------- | ------------ |
| 4th, 4th, **1st**, 2nd, **1st**, 3rd | **1st**        | **1st**     | **4th**      |

Each game had 4 contestants.

The league rounds contributed towards a teams league score, of which the top two teams skipped straight through to the Finals.

The Quarter, Semi and Grand finals were knockout rounds, with the bottom two teams in each match being eliminated, and the Grand finals being your teams final placement.

(This might be slightly wrong but I'm pretty sure it's fairly accurate)

# Requirements

sbot - `pip install sbot`

# License

If you would like to use this code you must meet the following requirements:

-   Not be currently attending an **sbot/Sourcebot** event - these events are for fun and you should be coding your own robot, duplicating someone else's code is not good sportsmanship.

-   Attribute myself and link this repo in your ReadME if the code will be in a github repository and leave the message commented at the top of the main.py file/paste it into your main.py file if you are just using part of the program.

-   Please email anything you make using this code to me (alfie.ranstead@outlook.com) so that I can see what you've used it for and possibly add it to the bottom of this ReadMe document.
