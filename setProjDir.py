import nuke
import nukescripts
import os
import re

def absFilePaths(nodes):
    for n in nodes:
        nPath = str(nuke.filename(n))
        n['file'].setValue(nPath)

def nodeWithFile():
    fileKnobNodes = [i for i in nuke.allNodes(recurseGroups=True) if nukescripts.searchreplace.__NodeHasFileKnob(i)]
    return fileKnobNodes

def searchReplaceProjDir():
    fileKnobNodes = nodeWithFile()
    searchstr = str(nuke.root().knob('project_directory').evaluate() + "/")
    replacestr = ''
    for f in fileKnobNodes:
        v = str(nuke.filename(f))
        repl = re.sub(searchstr, replacestr, v)
        f['file'].setValue(repl)

def setProjDir(var):
    if var == 0:
        try:
            filepath = os.path.dirname(nuke.getFilename('Set Project Directory'))
        except (TypeError, ValueError):
            nuke.message('Project directory not set!')
    elif var == 1:
        filepath = '[join [lrange [split [file dirname [knob root.name]] "/"] 0 end-0] "/"]'
    elif var == 2:
        filepath = '[join [lrange [split [file dirname [knob root.name]] "/"] 0 end-1] "/"]'
    elif var == 3:
        filepath = '[join [lrange [split [file dirname [knob root.name]] "/"] 0 end-2] "/"]'
    elif var == 4:
        filepath = '[join [lrange [split [file dirname [knob root.name]] "/"] 0 end-3] "/"]'
    else:
        filepath = '[join [lrange [split [file dirname [knob root.name]] "/"] 0 end-4] "/"]'

    try:
        absFilePaths(nodeWithFile())
    except:
        pass
    nuke.root().knob("project_directory").setValue(filepath)
    searchReplaceProjDir()

def absFilePathsSel():
    try:
        absFilePaths(nuke.selectedNodes())
    except NameError:
        nuke.message('No "file" knob found in selected Nodes.')

def SelNodeWithFile():
    for n in nodeWithFile():
        n.knob('selected').setValue('True')

nodeMenu = nuke.menu('Nuke').findItem('Edit/Node')
nodeMenu.addCommand('Custom/Convert file path to absolute', 'setProjDir.absFilePathsSel()')
nodeMenu.addCommand('Custom/Select nodes with File Knob', 'setProjDir.SelNodeWithFile()')

fileMenu = nuke.menu('Nuke').findItem('File').addMenu('Set Project Directory')
fileMenu.addCommand('Custom path', 'setProjDir.setProjDir(0)')


def addRelPathCommand():
    fileMenu.addCommand(re.escape(nuke.script_directory().rsplit('/',4)[0]), 'setProjDir.setProjDir(5)')
    fileMenu.addCommand(re.escape(nuke.script_directory().rsplit('/',3)[0]), 'setProjDir.setProjDir(4)')
    fileMenu.addCommand(re.escape(nuke.script_directory().rsplit('/',2)[0]), 'setProjDir.setProjDir(3)')
    fileMenu.addCommand(re.escape(nuke.script_directory().rsplit('/',1)[0]), 'setProjDir.setProjDir(2)')
    fileMenu.addCommand(re.escape(nuke.script_directory().rsplit('/',0)[0]), 'setProjDir.setProjDir(1)')

#Add relative project directory to File menu when a script is open
nuke.addOnScriptLoad(addRelPathCommand, nodeClass='Root')
