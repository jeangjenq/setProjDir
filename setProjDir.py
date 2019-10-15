'''

setProjDir v2.4
Created by Jeang Jenq Loh
Last updated: 27 April 2019

Set project directory and convert all paths to relative

'''

import nuke
import nukescripts
import os
import re

# function to accquire absolute file path from node
def absFilePath(node):
    return str(nuke.filename(node))

# function to accquire list of nodes with "file" knob
def nodeWithFile(recurse):
    fileKnobNodes = [i for i in nuke.allNodes(recurseGroups=recurse) if nukescripts.searchreplace.__NodeHasFileKnob(i)]
    return fileKnobNodes

# function to replace file path in node from absolute to relative, takes in (project path, node)
def searchReplaceProjDir(projPath, node):
    searchstr = projPath # accquire project path from input
    # make sure project path ends with "/"
    if not searchstr.endswith('/'):
        searchstr += '/'
    replacestr = ''
    v = absFilePath(node)
    repl = re.sub(searchstr, replacestr, v) # new relative file path
    try:
        node['file'].setValue(repl)
    except NameError:
        pass

# Create new user knob and set its default value in python panel
def newUserKnob(knob, value):
    knob.setValue(value)
    return knob

# Panel for user to select nodes to replace file paths
def selectNodesPanel():
    p = nukescripts.PythonPanel('Conform file paths to Project Directory')
    p.nodesSelection = newUserKnob(nuke.Enumeration_Knob('nodesSel', 'Nodes selections', ['All nodes', 'Selected nodes only', 'Exclude selected nodes']), 2)
    p.checkReadGeo = newUserKnob(nuke.Boolean_Knob('checkReadGeo', 'Exclude ReadGeo nodes', '0'), 0)
    p.readGeoText = nuke.Text_Knob('readGeoText', '', 'Will affect configured alembic scenegraph')
    p.div1 = nuke.Text_Knob('div1', '')
    p.recurseGroups = newUserKnob(nuke.Boolean_Knob('checkRecurse', 'Exclude groups/gizmos', '0'), 1)
    p.tclPath = newUserKnob(nuke.Boolean_Knob('checkTCL', 'Exclude TCL knobs', '0'), 1)
    for k in (p.checkReadGeo, p.readGeoText, p.div1, p.recurseGroups):
        k.setFlag(0x1000)
    for k in (p.nodesSelection, p. checkReadGeo, p.readGeoText, p.div1, p.recurseGroups, p.tclPath):
        p.addKnob(k)

    if p.showModalDialog():
        # check if recurseGroups is true
        if p.recurseGroups.value():
            allNodes = nodeWithFile(False)
        else:
            allNodes = nodeWithFile(True)

        # check if selectedNodes
        if p.nodesSelection.value() == 'Selected nodes only':
            for node in allNodes:
                if node not in nuke.selectedNodes():
                    allNodes.remove(node)
        elif p.nodesSelection.value() == 'Exclude selected nodes':
            for node in allNodes:
                if node in nuke.selectedNodes():
                    allNodes.remove(node)

        # remove nodes with TCL
        if p.tclPath.value():
            for node in allNodes:
                hasTCL = bool(re.search(r'\[*\]', node['file'].value()))
                if hasTCL:
                    allNodes.remove(node)

        # remove readGeos node if necessary
        if p.checkReadGeo.value():
            for n in allNodes:
                if n.Class() == 'ReadGeo2':
                    allNodes.remove(n)

        return allNodes

# function to start the setProjDir process, steps commented below
def setProjDir(var):
    # launch selectNodesPanel first to acquire list of nodes to affect, if any
    changeNodes = selectNodesPanel()
    if changeNodes is not None:
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
        newPath = nuke.tcl('return ' + filepath)

        # replace file paths in list of nodes acquired above to relative file paths
        for n in changeNodes:
            searchReplaceProjDir(newPath, n)
        # set project directory to selected path as above
        nuke.root().knob("project_directory").setValue(filepath)


# function to convert selected nodes' file path to absolute
def absFilePathsSel():
        try:
            for n in nuke.selectedNodes():
                n['file'].setValue(absFilePath(n))
        except NameError:
            nuke.message('No "file" knob found in selected nodes.')


# function to select nodes with file knob
def SelNodeWithFile():
    for n in nodeWithFile(False):
        n.knob('selected').setValue('True')