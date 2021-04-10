# Suave-Detector v1.1

hey there! This program was made for the 2021 SkillsUSA programming contest. Stinks-Detector creates backups of your hard drive and can compare backups to find differences within you're hardrive! It even uses basic mulit-threading (wow!). Check out my buddy ViperSniper's project for the contest here: https://github.com/vipersniper0501/Mirage. His program looks at any changes made within a few seconds, so its best use would be **after** installing a virus. My program though, creates a .csv file that can be used to check for changes between a couple of days, allowing for __long term backups__. Very suave inded.

Also, keep in mind this is not an Anti-Virus. It just detects file changes by looking at hashes, timestamps, sizes. Nothing more or less.

# Dependencies
The following modules are used:
pathlib
os
sys
PyQt6
threading
datetime
hashlib

**Also this runs on Python 3.8 btw**


# FAQ

_Why does my computer flag it as a "Unsafe" file?_
Its cause windows doesn't register it in it's program database, and it tries to not let you screw your computer into having its kernel rewritten in brainfuck.
Right click the file and select ___unblock file__ and press apply. Should let it work.

_Why does this kind of suck?_
Cause I'm a freshman and I learned like half of the stuff in there within days.
Still gonna make it work better.

_wtf does it freeze after I click ok_
IDK how to implement more than 2 threads, and I kinda like did multi-threading as an after-thought. The program for making backups uses only 2 threads, while the program for comparing them uses nil. It probably isn't long though, _considering it makes a hash of your entire root drive_. Gonna add an option to do a certain folder soon though.
