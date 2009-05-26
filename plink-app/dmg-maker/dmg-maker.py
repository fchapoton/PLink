#! /usr/bin/env python
"""
Creates a nice disk image, with background and /Applications symlink
for the app.  Uses YourSway's 'create-dmg' a GPL program available
from http://www.yoursway.com/free/#createdmg, slightly modified to
make the final mounted disk image size less that 300m !
"""
import os, sys, re
from math import ceil

name = "PLink"
dist_dir = "../dist"

command_str = """\
./create-dmg --window-size 500 240  --icon-size 128 \
--background "background.png"  --volname "%s" \
--icon "Applications" 400 95 \
--icon "%s" 50 95 \
--dmg-size %s \
%s.dmg  %s"""

def main():
    # Make sure the dmg isn't currently mounted, or this won't work.  
    mount_name = "/Volumes/" + name
    if os.path.exists(mount_name):
        print("Trying to eject " + mount_name)
        os.system("hdiutil detach " + mount_name)
    # Remove old dmg if there is one
    if os.path.exists(name + ".dmg"):
        os.remove(name + ".dmg")
    # Add symlink to /Applications if not there:
    if not os.path.exists("../dist/Applications"):
        os.symlink("/Applications/", dist_dir)
    # figure out the needed size:
    size, units = re.match("([\d.]+)([KMG])", os.popen("du -sh " + dist_dir).read()).groups()
    new_size = "%d" % ceil(1.2 * float(size)) + units
# Run the main script:
    os.system( command_str % (name, name, size, name, dist_dir) )

if __name__ == "__main__":
    main()



