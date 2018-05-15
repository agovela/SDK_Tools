# -= ag_SkinDetachAttach.py =-
#                  by Antonio Govela
#				   agovela@yahoo.com
#         ________                   .__          
#_____   /  _____/  _______  __ ____ |  | _____   
#\__  \ /   \  ___ /  _ \  \/ // __ \|  | \__  \  
# / __ \\    \_\  (  <_> )   /\  ___/|  |__/ __ \_
#(____  /\______  /\____/ \_/  \___  >____(____  /
#     \/        \/                 \/          \/ 
#
#     ______________
# - -/__ License __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Copyright 2018 Antonio Govela
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of 
# this software and associated documentation files (the "Software"), to deal in 
# the Software without restriction, including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the 
# Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS 
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
#     ___________________
# - -/__ Installation __/- - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ag_skinDetachAttach.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#			import ag_SkinDetachAttach as ag_SkinDetachAttach
#			ag_SkinDetachAttach.skinTool()
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Exports the selected meshe's skinCluster data, so we can freely manipulate components,
# It generates an xml file with all the info te re-skin the meshes including maximum influences 
#
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the UI, and press the buttons to choose the action.
# 
#     ____________
# - -/__ Video __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# 
#     _________
# - -/__ Ui __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Simple UI, did not want to overcomplicate things
# 
#     ___________________
# - -/__ Requirements __/- - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# The scene must be saved to be able to write the xml file
# This scripts runs in stand alone mode, no other utilities are required
#
#
#Find the script useful?
#Donate for a coup of coffee ??
#Thanks!
#
#BTC: 	1JiYcqaE9ShDuJY7XQozmqAFbzU6mK3mw8
#ETH:	0x11b9d22b4890bf074343ac5bc3dea5b74cde4e4a
#LTC:	LKstNMi6cm1THsqQG7AB4oFHtUyEmm8qyZ
#
#
#                                                             __________
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /_ Enjoy! _/- - -


__author__ = 'Antonio Govela'
__license__ = 'MIT'
__category__ = 'None'
__revision__ = 1



import os,ast,sys
import maya.cmds as mc



def dirPath(folder = ""):
	osName, osExt = os.path.splitext(mc.file(query=True,sceneName=True))
	scnName= os.path.splitext(mc.file(query=True,sceneName=True,shortName=True))[0]
	osNameInv 				= (osName.replace ("\\","/").lower())
	presetsDir = osNameInv.rstrip(scnName.lower()+osExt) + "skinWeights/"
	
	if folder:
		presetsDir = osName.rstrip(scnName) + folder + "/"
	if not os.path.isdir(presetsDir):
		try:
			os.makedirs(presetsDir)
		except:
			print "Could not create skinWeights Dir"
	return presetsDir


def action_SaveWeights(savePath = ''):
	savePath =''
	selectionList = mc.ls(sl=True, objectsOnly=True)
	if not savePath:
		savePath = dirPath()
	for obj in selectionList:
		if mc.objectType (obj, isType = "transform"):
			mc.select(obj)
			xmlName = str(obj) + ".xml"
			try:
				mesh = mc.ls(sl=True, objectsOnly=True)
				meshSkinCluster =  str(mc.ls( mc.listHistory( mesh ), type='skinCluster' )[0])
				mc.deformerWeights(xmlName, ex=True, path = savePath, deformer = meshSkinCluster)
			except:
				e = sys.exc_info()[1]
				print "Skipping mesh: {obj}: ".format(obj=obj) + str(e)
	print "----------------------------------------"
	print savePath.replace("/","\\")		
	return savePath


def exportSkinDict(dict,mesh):
	savePath = dirPath("skinWeights")
	jsonName = str(mesh) +'.xml'
	saveFile = savePath + jsonName

	f = open(saveFile, "r")
	contents = f.readlines()
	f.close()

	contents.insert(1, "<!-- " + str(dict) + " -->\n")

	f = open(saveFile, "w")
	contents = "".join(contents)
	f.write(contents)
	f.close()

def findSkinCluster(object):
	mesh = mc.ls(sl=True, objectsOnly=True)
	meshSkinCluster =  str(mc.ls( mc.listHistory( mesh ), type='skinCluster' )[0])
	return meshSkinCluster

def importSkinDict(mesh):
	loadPath = dirPath("skinWeights")
	xmlName = str(mesh) +'.xml'
	loadFile = loadPath + xmlName
	file = open(loadFile, "r")
	xmlSkinDict= ast.literal_eval(file.readlines(3)[1].replace("<!-- ","").replace(" -->",""))
	#print xmlSkinDict
	return xmlSkinDict
	

def addToSkinDict():
	global skinDict
	for mesh in meshes:
		maxInfDic = {}
		maxInf = mc.skinCluster(mesh,q=True,maximumInfluences=True)
		meshInf = str(mesh+"_maxInf")
		maxInfDic[meshInf]=maxInf
		skinDict[meshInf]=maxInf
		mc.select(mesh)
		skinCluster = findSkinCluster(mesh)
		skinJoints  = mc.skinCluster(skinCluster,query=True,inf=True)
		skinDict[mesh] = skinJoints
		skinOutDict = {}
		skinOutDict = {mesh:skinDict[mesh]}
		skinOutDict[meshInf]=maxInf
		exportSkinDict (skinOutDict,mesh)


def freezeGroups():
	for mesh in meshes:
		print "Freezing Mesh " + mesh
		mc.select (mesh)
		mc.delete (ch=True)

		attrs = [".translateX",".translateY",".translateZ",
				 ".rotateX",".rotateY",".rotateZ",
				 ".scaleX",".scaleY",".scaleZ"]


		print "------------------------> Unlocking Transforms <------------------------"
		for attr in attrs:
			try:
				mc.setAttr(mesh+attr, lock = 0)
			except:
				pass
			try:
				mc.makeIdentity(mesh, apply=True)
			except:
				print" Could not freeze mesh " + str(mesh)
				

def action_LoadWeights(loadPath = '', pruneValue = .05):
	selectionList = mc.ls(sl=True, objectsOnly=True)
	loaded = False
	if not loadPath:
		loadPath = dirPath()
	for obj in selectionList:
		if mc.objectType (obj, isType = "transform"):
			mc.select(obj)
			xmlName = str(obj) + ".xml"
			mesh = mc.ls(sl=True, objectsOnly=True)

			try:
				meshSkinCluster =  str(mc.ls( mc.listHistory( mesh ), type='skinCluster' )[0])
				mc.deformerWeights(xmlName, im=True, method = "index", path = loadPath, deformer = meshSkinCluster)
				if pruneValue > 0:
					mc.skinPercent( meshSkinCluster, pruneWeights=0.01)
				mc.skinCluster (meshSkinCluster, edit= True, forceNormalizeWeights=True )
				print "Loaded Skinweights: " + loadPath + xmlName
				loaded = True
			except:
				e = sys.exc_info()[1]
				print "Skipping mesh: {obj}: ".format(obj=obj) + str(e)
				loaded = False
	return loaded


def rebuildAndExportScene(setMaxInf=4):
	for mesh in meshes:
		tempDict = importSkinDict(mesh)
		bindJoints = tempDict[mesh]
		mc.select (bindJoints,mesh)
		try:
			maxInf = tempDict[mesh+"_maxInf"]
		except:
			maxInf=4
		mc.skinCluster(bindJoints,mesh,tsb=True, bindMethod= 1, ignoreHierarchy= True, maximumInfluences= maxInf, obeyMaxInfluences=True)
		mc.select (mesh)
		action_LoadWeights()



def skinDetachStart(*Args):
	global meshes
	meshes = mc.ls(selection=True)
	mc.select(meshes)
	action_SaveWeights()
	addToSkinDict()
	freezeGroups()
	

def skinAttachStart(*Args):
	global meshes
	meshes = mc.ls(selection=True)
	mc.select(meshes)
	rebuildAndExportScene()
	
	
def skinTool():
	mc.window(skinUI, height = 220, width = 100, sizeable=True )
	newLayout = mc.columnLayout()
	mc.iconTextButton('skinDetach_btn', style='iconAndTextHorizontal', image1= 'alignSurface.png', label='                                 Skin Detach               ', command=skinDetachStart )
	mc.separator( style='in', width=242)
	mc.iconTextButton('skinAttach_btn', style='iconAndTextHorizontal', image1= 'attachWithoutMoving.png', label='                                 Skin Attach               ', command=skinAttachStart, scaleIcon = True )
	mc.showWindow()


meshes = mc.ls(selection=True)
skinDict = {}


skinUI = 'skinDetach_Attach'

if mc.window(skinUI, exists=True):
    mc.deleteUI(skinUI)
    
    
#skinTool()