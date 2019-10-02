# GDML wrkbench gui init module
#
# Gathering all the information to start FreeCAD
# This is the second one of three init scripts, the third one
# runs when the gui is up

#***************************************************************************
#*   (c) Juergen Riegel (juergen.riegel@web.de) 2002                       *
#*                                                                         *
#*   This file is part of the FreeCAD CAx development system.              *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   FreeCAD is distributed in the hope that it will be useful,            *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Lesser General Public License for more details.                   *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with FreeCAD; if not, write to the Free Software        *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#*   Juergen Riegel 2002                                                   *
#*                                                                         *
#* Also copyright Keith Sloan                                              * 
#***************************************************************************/

import FreeCAD, FreeCADGui
from FreeCAD import *
from FreeCADGui import Workbench
import PartGui
from . import GDMLCommands, GDMLResources
import os, sys

def processDefault(doc) :
    from importGDML import processGDML
    processGDML(doc,FreeCAD.getResourceDir() + \
                "Mod/GDML/Resources/Default.gdml")

class GDML_Workbench (FreeCADGui.Workbench):
    Icon = os.path.join(os.path.dirname(__file__), "Resources", "icons", "GDMLWorkbench.svg")
    MenuText = "GDML"
    ToolTip = "GDML workbench"

    class MyObserver():
       def __init__(self):
           self.signal = []

       def slotCreatedDocument(self, doc):
           from importGDML import processGDML
           processGDML(doc,FreeCAD.getResourceDir() + \
                "Mod/GDML/Resources/Default.gdml")
    
    "GDML workbench object"
    def __init__(self):
        pass

    def Initialize(self):
        def QT_TRANSLATE_NOOP(scope, text):
            return text
        
        #import GDMLCommands, GDMLResources
        commands=['CycleCommand','BoxCommand','ConeCommand','ElTubeCommand', \
                  'EllipsoidCommand','SphereCommand', \
                  'TrapCommand','TubeCommand']
        toolbarcommands=['CycleCommand','BoxCommand','ConeCommand', \
                         'ElTubeCommand', 'EllipsoidCommand','SphereCommand', \
                         'TrapCommand','TubeCommand']

        parttoolbarcommands = ['Part_Cut','Part_Fuse','Part_Common']

        self.appendToolbar(QT_TRANSLATE_NOOP('Workbench','GDMLTools'),toolbarcommands)
        self.appendMenu('GDML',commands)
        self.appendToolbar(QT_TRANSLATE_NOOP('Workbech','GDML Part tools'),parttoolbarcommands)
        ResourcePath = FreeCAD.getHomePath() + "Mod/GDML/Resources/"
        print("Resource Path : "+ResourcePath)
        #FreeCADGui.addIconPath(FreeCAD.getResourceDir() + \
        #FreeCADGui.addIconPath(":/icons")
        FreeCADGui.addIconPath(ResourcePath + "icons")
        #FreeCADGui.addLanguagePath(":/translations")
        FreeCADGui.addLanguagePath(ResourcePath + "/translations")
        FreeCADGui.addPreferencePage(ResourcePath + "/ui/GDML-base.ui","GDML")

    def Activated(self):
        "This function is executed when the workbench is activated"
        print ("Activated")
        self.obs = self.MyObserver()
        App.addDocumentObserver(self.obs)
        doc = FreeCAD.activeDocument()
        if doc != None :
           if doc.Objects[0].Name != "Constants" : 
              #self.processDefault(doc)
              #processDefault(doc)
              self.MyObserver.slotCreatedDocument(self,doc)
        return

    def Deactivated(self):
        "This function is executed when the workbench is deactivated"
        App.removeDocumentObserver(self.obs)
        return
    
    def GetClassName(self):
        return "Gui::PythonWorkbench"

Gui.addWorkbench(GDML_Workbench())

