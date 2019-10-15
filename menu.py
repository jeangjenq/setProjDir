'''

########################################################################################################################

setProjDir v2.4
Created by Jeang Jenq Loh
Last updated: 27 April 2019

menu.py
Create nodes menu with icon
Add commands for version check, convert path to absolute, select nodes with file
Add paths onScriptLoad

########################################################################################################################
Potential future release:
Automatically avoid file knobs with TCL/Python
'''

import nuke
import setProjDir
import webbrowser
import re

#Create toolbar with icon
JJmenu = nuke.menu('Nodes').addMenu('jj_tools', icon='icon_JJ.png')

#directory for setProjDir
projDirMenu = JJmenu.addMenu('Set Project Directory')
projDirMenu.addCommand('Version v2.4', "webbrowser.open('http://www.nukepedia.com/python/misc/setprojdir')")
projDirMenu.addCommand('Convert file path to absolute', 'setProjDir.absFilePathsSel()')
projDirMenu.addCommand('Select nodes with File Knob', 'setProjDir.SelNodeWithFile()')
projDirMenu.addCommand('Custom Path', 'setProjDir.setProjDir(0)', index=3)

def addRelPathCommandMenu():
    # import re
    projectPath = nuke.menu('Nodes').findItem('jj_tools/Set Project Directory').addMenu('Project Path')
    projectPath.clearMenu()
    for i in range(5)[::-1]:
        projectPath.addCommand(re.escape(nuke.script_directory().rsplit('/', i)[0]), 'setProjDir.setProjDir(%s)' % str(i+1))

def rmRelPathCommandMenu(): # Doesn't work at the moment
    projectPath = nuke.menu('Nodes').findItem('jj_tools/Set Project Directory/Project Path')
    if projectPath is not None:
        projectPath.clearMenu()


#Add relative project directory to File menu when a script is open
nuke.addOnScriptLoad(addRelPathCommandMenu, nodeClass='Root')
#nuke.addOnScriptClose(rmRelPathCommandMenu, nodeClass='Root')
# can't affect or change menu items with a '/' for some reason, looking into it
