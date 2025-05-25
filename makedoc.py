#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------
# (c) kelu124
# cc-by-sa/4.0/
# -------------------------
# Requires GraphViz and Wand
# -------------------------
# Use ./makedoc.py full
# to have the graphs generated
# -------------------------

"""Description: script to build autodocumentation."""

__author__ = "kelu124"
__copyright__ = "Copyright 2016, Kelu124"
__license__ = "cc-by-sa/4.0/"

import time
import os
import markdown
import re
import graphviz as gv
import functools

# Wand for SVG to PNG Conversion
# from wand.api import library
# import wand.color
# import wand.image
from PIL import Image
import sys
from bs4 import BeautifulSoup
from doc.mkdoc import *
from pprint import pprint

import gc
gc.set_threshold(0)

FullSVG = 0

GrosJaSON = {"images": {}, "md": {}}

# -------------------------
# arguments
# -------------------------

if len(sys.argv) > 0:
    for element in sys.argv:
        # Add full in the args to make graphs
        if "full" in element:
            FullSVG = 1

# -------------------------
# Manage suppliers
# -------------------------

Suppliers = GetSuppliersList("retired/cletus/suppliers/")
OpenWrite("# Status of suppliers\n\n" + Suppliers, "retired/cletus/suppliers/Readme.md")

# echo = GetMurgenStats()

d = GetLogs("./")
OpenWrite(CreateWorkLog(d), "include/AllLogs.md")

if 0:
    CopyGitBookFile("include/AllLogs.md", "gitbook/Chapter4/AllLogs.md")

# -------------------------
# Probes
# -------------------------

ListOfProbes, GrosJaSON = ListProbes("./include/probes/define.md", GrosJaSON)
print(ListOfProbes)
# -------------------------
# Contributors
# -------------------------

ListofContribs, GrosJaSON = ListContrib("./include/community/", GrosJaSON)

# -------------------------
# Preparing Images
# -------------------------

ListJPGfromBMP("./")

GenFiles = "# Getting images\n"
ImgList = GetImgFiles("./")
ImgList = [x for x in ImgList if ".venv" not in x]
ListIfImages = []
ListOfExperiment = []
for k in ImgList:
    probeFound = ""
    GrosJaSON["images"][k] = {}
    if "gitbook" not in k:
        Tags = CreateImgTags("." + k)

    AllTags = GetTags(Tags)
    GrosJaSON["images"][k]["path"] = k
    GrosJaSON["images"][k]["author"] = AllTags[0]
    if AllTags[0] in GrosJaSON["contributors"].keys():
        GrosJaSON["contributors"][AllTags[0]]["images"].append("." + k)
    GrosJaSON["images"][k]["modules"] = AllTags[1]
    modz = AllTags[1].split(",")
    modz = [x.strip() for x in modz]
    for probe in ListOfProbes:
        if probe in modz:
            GrosJaSON["probes"][probe]["images"].append(k)
            probeFound = probe
            # print probe, k, modz

    GrosJaSON["images"][k]["category"] = AllTags[2]
    GrosJaSON["images"][k]["experiment"] = AllTags[3]
    GrosJaSON["images"][k]["description"] = AllTags[4]

    ListIfImages.append(AllTags)
    if "ToTag" not in AllTags[3]:
        if len(probeFound):
            GrosJaSON["probes"][probe]["experiments"].append(AllTags[3])
            # print GrosJaSON["probes"][probe]["experiments"]
        if len(AllTags[3]):
            ListOfExperiment.append(AllTags[3])
        if AllTags[0] in GrosJaSON["contributors"].keys():
            GrosJaSON["contributors"][AllTags[0]]["experiments"].append(AllTags[3])
        # print AllTags[0],AllTags[3]
    GenFiles += "* __" + k + "__:\n  * " + "\n  * ".join(AllTags) + "\n"

ListOfExperiment = list(set(ListOfExperiment))
ListOfExperiment.sort()

# print ListOfExperiment


OpenWrite(GenFiles.replace("  * ToTag\n","").replace("  * kelu124\n",""), "include/FilesList/ImgFiles.md")


# -------------------------
# Presentations
# -------------------------

GrosJaSON["module"] = {}

for k in ModulesList:
    GrosJaSON["module"][k] = {}
    GrosJaSON["module"][k]["path"] = "/" + k + "/"
for k in ModulesRetiredList:
    GrosJaSON["module"][k] = {}
    GrosJaSON["module"][k]["path"] = "/retired/" + k + "/"

# print GrosJaSON


# -------------------------
# Presentations
# -------------------------


PPTz = GetPptFiles("./")
PPTFiles = ""
for i in range(len(PPTz)):
    PPTName = PPTz[i].split("/")[-1]
    PPTFiles += (
        "* ["
        + PPTName
        + "]("
        + PPTz[i][1:]
        + ") - see [Presentation online](http://kelu124.github.io/echomods/"
        + PPTName.split(".")[0]
        + ".html)\n"
    )
    CopyGitBookFile(PPTz[i][1:], "gh-pages/" + PPTz[i].split("/")[-1])
OpenWrite(PPTFiles, "include/FilesList/PPTFiles.md")

# -------------------------
# Obtenir la liste des modules
# -------------------------

GraphModules = digraph()

MDFiles = GetGeneratedFiles("./")
MDFiles = [x for x in MDFiles if ".venv" not in x]
for MDFile in MDFiles[5]:
    GrosJaSON["md"][MDFile[1:]] = {}
    GrosJaSON["md"][MDFile[1:]]["path"] = MDFile
log = log + MDFiles[3]
GenFiles = "* " + "\n* ".join(MDFiles[0])
OpenWrite(GenFiles, "include/FilesList/GeneratedFiles.md")

NbMDManuels = len(MDFiles[1])

## For experiences... MDFiles[4],MDFiles[5] are filescontent, fileslist @todo 201710

MdLog = ""

ListeOfManualFiles = MDFiles[1]
ListeOfManualFilesDesc = MDFiles[2]

for i in range(len(MDFiles[1])):
    MdLog += (
        "* ["
        + ListeOfManualFiles[i]
        + "]("
        + ListeOfManualFiles[i][1:]
        + "): "
        + ListeOfManualFilesDesc[i]
        + " "
    )
    CheckRef = CreateRefFiles(
        NbMDManuels, ListeOfManualFiles[i][1:], MDFiles[4], MDFiles[5]
    )

    if ListeOfManualFiles[i][1:] in GrosJaSON["md"]:
        GrosJaSON["md"][ListeOfManualFiles[i][1:]]["references"] = CheckRef[2]

    MdLog += CheckRef[0]
    log = log + CheckRef[1]
    MdLog += "\n"

OpenWrite(MdLog, "include/FilesList/ManualFiles.md")


# check auto files
for mdFile in MDFiles[0]:
    log = log + CheckLink(mdFile, True)
# check manual files
for mdFile in MDFiles[1]:
    log = log + CheckLink(mdFile, False)

ListOfDirs = GetListofModules("./")
for eachInput in ListOfDirs:
    GraphModules.node(
        eachInput, style="filled", fillcolor="blue", shape="box", fontsize="22"
    )
# print ListOfDirs

GrosJaSON = MDProbes(GrosJaSON)

# -------------------------
# Doing the templates files
# -------------------------

TPLLog = ""
ListeOfTPL = GetTPLFiles("./")

for i in range(len(ListeOfTPL)):
    TPLLog += (
        "* ["
        + ListeOfTPL[i].split("/")[-1]
        + "]("
        + ListeOfTPL[i][1:]
        + "): "
        + ListeOfTPL[i]
    )
    CheckRef = CreateRefFiles(NbMDManuels, ListeOfTPL[i][1:], MDFiles[4], MDFiles[5])
    TPLLog += CheckRef[0]
    log = log + CheckRef[1]
    TPLLog += "\n"
    ##
    # print "-- "+ListeOfTPL[i][2:]
    for pp in range(1):
        # Doing it twice for tpl using tpl-generated files
        # @TODO: error ici
        RPI = GetIncludes(
            getText(ListeOfTPL[i][2:]), MDFiles[5], MDFiles[4], ListeOfTPL[i][2:]
        )
        RPI_article = RPI[0]
        OpenWrite(IncludeImage(RPI_article), ListeOfTPL[i][2:].split(".tpl")[0])

    log += RPI[1]

print(ListeOfTPL[i][2:])




OpenWrite(TPLLog, "include/FilesList/TPLFiles.md")


# -------------------------
# Source code listing -- python
# -------------------------

PythonLog = ""
ListeOfPython = GetPythonFiles("./")
ListeOfPython = [x for x in ListeOfPython if ".venv" not in x]
PythonFiles = CheckPythonFile(ListeOfPython)
GrosJaSON["python"] = {}

for pythonfile in ListeOfPython:
    path = pythonfile[1:]

    GrosJaSON["python"][path] = {}
    GrosJaSON["python"][path]["path"] = path

log = log + PythonFiles[0]


for i in range(len(PythonFiles[1])):
    try:
        PythonLog += (
            "* ["
            + ListeOfPython[i].split("/")[-1]
            + "]("
            + ListeOfPython[i][1:]
            + "): "
            + PythonFiles[1][i]
        )
        CheckRef = CreateRefFiles(
            NbMDManuels, ListeOfPython[i][1:], MDFiles[4], MDFiles[5]
        )
        ##@TODO ca a l'air de planter la
        GrosJaSON["python"][ListeOfPython[i][1:]]["references"] = CheckRef[
            2
        ]  # checks if any file refer to the python
        PythonLog += CheckRef[0]
        log = log + CheckRef[1]
        PythonLog += "\n"
    except:
        print("Error with ", i, "at source python")
OpenWrite(PythonLog + "\n\nDONE!", "include/FilesList/PythonFiles.md")

# -------------------------
# Source code listing
# -------------------------

CLog = ""
ListeOfC = GetCFiles("./")
ListeOfC = [x for x in ListeOfC if ".venv" not in x]
CFiles = CheckCFile(ListeOfC)
GrosJaSON["C"] = {}

for pythonfile in ListeOfC:
    path = pythonfile[1:]
    GrosJaSON["C"][path] = {}
    GrosJaSON["C"][path]["path"] = path

log = log + CFiles[0]

for i in range(len(CFiles[1])):
    try:
        CLog += (
            "* ["
            + ListeOfC[i].split("/")[-1]
            + "]("
            + ListeOfC[i][1:]
            + "): "
            + CFiles[1][i]
        )
        CheckRef = CreateRefFiles(NbMDManuels, ListeOfC[i][1:], MDFiles[4], MDFiles[5])
        GrosJaSON["C"][ListeOfC[i][1:]]["references"] = CheckRef[
            2
        ]  # checks if any file refer to the python
        CLog += CheckRef[0]
        log = log + CheckRef[1]
        CLog += "\n"
    except:
        print("Error with ", i, "at C source")
OpenWrite(CLog, "include/FilesList/CFiles.md")

## Jupyter files

ListeOfJupy = GetJupyFiles("./")
JupyLog = ""
GrosJaSON["jupyter"] = {}

for jupyfile in ListeOfJupy:
    path = jupyfile[1:]
    GrosJaSON["jupyter"][path] = {}
    GrosJaSON["jupyter"][path]["path"] = path

for i in range(len(ListeOfJupy)):
    JupyLog += "* [" + ListeOfJupy[i].split("/")[-1] + "](" + ListeOfJupy[i][1:] + ")"
    CheckRef = CreateRefFiles(NbMDManuels, ListeOfJupy[i][1:], MDFiles[4], MDFiles[5])
    JupyLog += CheckRef[0]
    log = log + CheckRef[1]
    PythonLog += "\n"
OpenWrite(JupyLog, "include/FilesList/JupyFiles.md")

InoLog = ""
ListeOfArduino = GetInoFiles("./")
GrosJaSON["arduino"] = {}

for inofile in ListeOfArduino:
    path = inofile[1:]
    GrosJaSON["arduino"][path] = {}
    GrosJaSON["arduino"][path]["path"] = path

InoFi = CheckInoFile(ListeOfArduino)
log = log + InoFi[0]
for i in range(len(InoFi[1])):
    InoLog += (
        "* ["
        + ListeOfArduino[i].split("/")[-1]
        + "]("
        + ListeOfArduino[i][1:]
        + "): "
        + InoFi[1][i]
    )
    CheckRef = CreateRefFiles(
        NbMDManuels, ListeOfArduino[i][1:], MDFiles[4], MDFiles[5]
    )
    InoLog += CheckRef[0]
    log = log + CheckRef[1]
    InoLog += "\n"

OpenWrite(InoLog, "include/FilesList/ArduinoFiles.md")

AllFilesLog = ""
AllFilesLog += "## Manually written files\n\n" + MdLog + "\n"
AllFilesLog += "## Arduino files\n\n" + InoLog + "\n"
AllFilesLog += "## Jupyter files\n\n" + JupyLog + "\n"
AllFilesLog += "## Python files\n\n" + PythonLog + "\n"
AllFilesLog += "## Presentation files\n\n" + PPTFiles + "\n"
AllFilesLog += (
    "## " + str(len(MDFiles[0])) + " Auto generated files\n\n" + GenFiles + "\n"
)

AllFilesLog = AddRawHURL(AllFilesLog)

OpenWrite(AllFilesLog, "include/FilesList/AllFiles.md")

# -------------------------
# Creating Experiments
# -------------------------

AllExpeList, ExpeJSON, LogExpe = MakeExperiments(
    ListOfExperiment, ListIfImages, GrosJaSON
)
log = log + LogExpe
GrosJaSON["experiments"] = ExpeJSON

# Adding Experiments descriptions in

GrosJaSON, GHList = DescribeExpes(GrosJaSON)

# And putting back experiments in the probes list of experiments

GrosJaSON = PutBackProbes(GrosJaSON)

# -------------------------
# Retired modules List
# -------------------------


ListOfRetiredDirs = GetListofModules("./retired")
# print ListOfRetiredDirs

# -------------------------
# Files includes
# -------------------------

pitch = getText("include/AddPitch.md")
HeaderDocTxt = getText("include/AddEchomods.md") + getText("include/sets/KitCosts.md")
AddInterfacesDocTxt = getText("include/AddInterfaces.md")
AddLicenseDocTxt = getText("include/AddLicense.md")
AddPrinciples = getText("include/AddPrinciples.md")
AddStructure = getText("include/AddStructure.md")
AddStructureDetails = getText("include/AddStructureDetails.md")
AddShoppingList = getText("include/AdHocShoppingList.md")


# -------------------------
# Préparer un tableau de présentation
# -------------------------

TableModules = "# A recap of the modules \n\n\n"
TableModulesShort = "# A recap of the modules \n\n\n"

TableModules += "| ThumbnailImage | Name | In | Out |\n|------|-------|----|------|\n"
TableModulesShort += "| ThumbnailImage | Name | \n|------|-------| \n"

for ReadMe in ListOfDirs:
    [soup, ReadMehHtmlMarkdown] = returnSoup(ReadMe + "/Readme.md")

    # print getParam(ReadMe,"ds")
    ModuleDesc = returnHList(soup, "h2", "Description")
    if len(GetParams(ModuleDesc)) > 0:
        Parameter = "__[MDL " + ReadMe + "]__ " + GreenMark + " Metadata ("
        Parameter += ", ".join(GetParams(ModuleDesc)) + ")"
        log.append(Parameter + "\n")
    else:
        log.append("__[MDL " + ReadMe + "]__ " + RedMark + "Metadata missing" + "\n")

    [soup, ReadMehHtmlMarkdown] = returnSoup(ReadMe + "/Readme.md")
    # OK - Check real name
    ModuleNomenclature = getHs(soup, "h2", "Name")
    if len(ModuleNomenclature) > 0:
        NameCheck = (
            "__[MDL "
            + ReadMe
            + "]__ "
            + GreenMark
            + " 01. Real name found: "
            + ModuleNomenclature.find_next("code").text
            + "\n"
        )
        log.append(NameCheck)
        if len(NameCheck) == 0:
            log.append(
                "__[MDL "
                + ReadMe
                + "]__ "
                + RedMark
                + " 01. No Real name found "
                + "\n"
            )

    [soup, ReadMehHtmlMarkdown] = returnSoup(ReadMe + "/Readme.md")
    # Getting the Desc of the Module
    ModuleDesc = getHs(soup, "h3", "What is it supposed to do?")
    Desc = ModuleDesc.find_next("p").text

    [soup, ReadMehHtmlMarkdown] = returnSoup(ReadMe + "/Readme.md")
    # OK - Getting the Innards of the Module // inside the block diagram
    GraphThisModule = digraph()
    Paires = returnHList(soup, "h3", "block diagram")
    if len(Paires) > 0:
        GraphModule(Paires, GraphThisModule, ReadMe, FullSVG)
        log.append(
            "__[MDL " + ReadMe + "]__ " + GreenMark + " 01. Block diagram OK" + "\n"
        )
    else:
        log.append(
            "__[MDL "
            + ReadMe
            + "]__ "
            + RedMark
            + " 01. No block diagram section "
            + "\n"
        )

    # OK - Getting the Inputs of the Module
    ItemList = returnHList(soup, "h3", "Inputs")
    inpoots = ""
    Module = []
    for OneIO in ItemList:
        codes = getCode(OneIO)
        if len(codes) > 0:
            for EachIO in codes:
                Module.append(EachIO)
    if len(Module) > 0:
        inpoots = "<ul>"
        for item in Module:
            inpoots += "<li>" + item + "</li>"
            if "ITF-m" not in item:
                GraphModules.node(item, style="rounded,filled", fillcolor="yellow")
            else:
                GraphModules.node(item, style="rounded,filled", fillcolor="green")
            GraphModules.edge(item, ReadMe, splines="line", nodesep="1")
            inpoots += "</ul>"
            log.append(
                "__[MDL "
                + ReadMe
                + "]__ "
                + GreenMark
                + " "
                + str(len(ItemList))
                + " input(s)"
                + "\n"
            )
    if len(ItemList) == 0:
        log.append("__[MDL " + ReadMe + "]__ " + RedMark + " 02. No inputs " + "\n")

    # OK - Getting the Outputs of the Module
    ItemList = returnHList(soup, "h3", "Outputs")
    Module = []
    outpoots = ""
    for OneIO in ItemList:
        codes = getCode(OneIO)
        if len(codes) > 0:
            for EachIO in codes:
                Module.append(EachIO)
    if len(Module) > 0:
        outpoots = "<ul>"
        for item in Module:
            outpoots += "<li>" + item + "</li>"
            if "ITF-m" not in item:
                GraphModules.node(item, style="rounded,filled", fillcolor="yellow")
            else:
                GraphModules.node(item, style="rounded,filled", fillcolor="green")
            GraphModules.edge(item, ReadMe, splines="line", nodesep="1")
            outpoots += "</ul>"
            log.append(
                "__[MDL "
                + ReadMe
                + "]__ "
                + GreenMark
                + " "
                + str(len(ItemList))
                + " output(s)"
                + "\n"
            )
            if len(ItemList) == 0:
                log.append(
                    "__[MDL " + ReadMe + "]__ " + RedMark + " 02. No outputs " + "\n"
                )

    TableModules += (
        "|<img src='https://github.com/kelu124/echomods/blob/master/"
        + ReadMe
        + "/viewme.png' align='center' width='150'>|**["
        + ReadMe
        + "](/"
        + ReadMe
        + "/Readme.md)**: "
        + Desc
        + "|"
        + inpoots
        + "|"
        + outpoots
        + "|\n"
    )

    TableModulesShort += (
        "|<img src='https://github.com/kelu124/echomods/blob/master/"
        + ReadMe
        + "/viewme.png' align='center' width='150'>|**["
        + ReadMe
        + "](/"
        + ReadMe
        + "/Readme.md)**: "
        + Desc
        + "|\n"
    )


# Saving it in a file
OpenWrite(TableModules + "\n\n", "include/AddModulesSummary.md")


# -------------------------
# Retired Modules Table
# -------------------------

TableRetiredModules = "# A recap of our retired modules \n\n\n"
TableRetiredModules += "| ThumbnailImage | Name | In | Out |\n"
TableRetiredModules += "|------|-------|----|------|\n"

for ReadMe in ListOfRetiredDirs:

    [soup, ReadMehHtmlMarkdown] = returnSoup("./retired/" + ReadMe + "/Readme.md")

    # Getting the Desc of the Module
    pattern = r"</h3>([\s\S]*)<h3>How"
    results = re.findall(pattern, ReadMehHtmlMarkdown, flags=0)
    patternCode = r"<p>(.*?)</p>"
    Desc = []
    for item in results:
        Desc = map(str, re.findall(patternCode, item, flags=0))
    print(list(Desc))
    if len(list(Desc)) >= 1:
        Desc = list(Desc)[0]
    else:
        Desc = ""

    # Getting the Innards of the Module // inside the block diagram
    pattern = r"block diagram</h3>([\s\S]*)<h2>About"
    results = re.findall(pattern, ReadMehHtmlMarkdown, flags=0)
    patternCode = r"<li>(.*?)</li>"
    Pairs = []
    GraphThisModule = digraph()
    for item in results:
        Pairs = map(str, re.findall(patternCode, item, flags=0))
        for eachPair in Pairs:
            eachPair = eachPair.replace("<code>", "")
            eachPair = eachPair.replace("</code>", "")
            Couples = eachPair.split("-&gt;")

    # Getting the Inputs of the Module
    pattern = r"Inputs</h3>([\s\S]*)<h3>Outputs"
    results = re.findall(pattern, ReadMehHtmlMarkdown, flags=0)
    patternCode = r"<code>(.*?)</code>"
    Inputs = []
    for item in results:
        Inputs = map(str, re.findall(patternCode, item, flags=0))
        if len(list(Inputs)) > 0:
            inpoots = "<ul><li>" + "</li><li>".join(Inputs) + "</li></ul>"
        else:
            inpoots = ""

    # Getting the Ouputs of the Module
    pattern = r"Outputs</h3>([\s\S]*)<h2>Key"
    results = re.findall(pattern, ReadMehHtmlMarkdown, flags=0)
    patternCode = r"<code>(.*?)</code>"
    Outputs = []
    for item in results:
        Outputs = map(str, re.findall(patternCode, item, flags=0))
        if len(list(Outputs)) > 0:
            outpoots = "<ul><li>" + "</li><li>".join(Outputs) + "</li></ul>"
        else:
            outpoots = ""

    TableRetiredModules += (
        "|<img src='https://github.com/kelu124/echomods/blob/master/retired/"
        + ReadMe
        + "/viewme.png' align='center' width='150'>|**["
        + ReadMe
        + "](/retired/"
        + ReadMe
        + "/Readme.md)**: "
        + Desc
        + "|"
        + inpoots
        + "|"
        + outpoots
        + "|\n"
    )

TableRetiredDocTxt = "\n\n" + TableRetiredModules + "\n\n"

# -------------------------
# Créer le tableau d'avancement & TODOs
# -------------------------

TableAvancement = "# Progress on building the modules \n\n\n"
TableAvancement += "## Module-wise \n\n\n"
TableAvancement += "Note that the 'BONUS!' represents something that _could_ be done, and does not count as a strict TODO.\n\n\n"
TableAvancement += "| Name of module | ToDo | Done |  Progress |\n"
TableAvancement += "|------|-------|----|-----|\n"

TODOsToShopping = "### Todos from Modules\n"

for ReadMe in ListOfDirs:
    f = open(ReadMe + "/Readme.md", "r")
    ReadMehHtmlMarkdown = markdown.markdown(f.read())
    f.close()
    # print ReadMehHtmlMarkdown
    # Getting the todo-list for the module
    pattern = r"Discussions</h2>([\s\S]*)<h3>DONE"
    results = re.findall(pattern, ReadMehHtmlMarkdown, flags=0)
    patternCode = r"<li>(.*?)</li>"
    bonus = 0

    for item in results:

        todos = list(map(str, re.findall(patternCode, item, flags=0)))
        if len(todos) > 0:
            TODO = "<ul><li>" + "</li><li>".join(todos) + "</li></ul>"
            for todo in todos:
                TODOsToShopping = (
                    TODOsToShopping
                    + "* "
                    + todo
                    + " (in ["
                    + ReadMe
                    + "](/"
                    + ReadMe
                    + "/))\n"
                )
        else:
            TODO = ""
        for itemtodo in todos:
            if "BONUS!" in itemtodo:
                bonus = bonus + 1
    # print bonus
    # Getting the done-list for the module
    pattern = r"DONE</h3>([\s\S]*)<h3>People"
    results = re.findall(pattern, ReadMehHtmlMarkdown, flags=0)
    patternCode = r"<li>(.*?)</li>"
    for item in results:
        dones = list(map(str, re.findall(patternCode, item, flags=0)))
        if len(dones) > 0:
            DONE = "<ul><li>" + "</li><li>".join(dones) + "</li></ul>"
        else:
            DONE = ""
    # Getting the peoplefor the module
    pattern = r"People</h3>([\s\S]*)<h2>License"
    results = re.findall(pattern, ReadMehHtmlMarkdown, flags=0)
    patternCode = r"<li>(.*?)</li>"
    for item in results:
        peoples = list(map(str, re.findall(patternCode, item, flags=0)))
        if len(peoples) > 0:
            PEOPLE = "<ul><li>" + "</li><li>".join(peoples) + "</li></ul>"
        else:
            PEOPLE = ""
    # Getting the progress
    nbDone = len(dones)
    todos = list(map(str, re.findall(patternCode, item, flags=0)))
    nbTodo = len(todos)

    if (nbTodo + nbDone) > 0:
        PCProgress = ((nbDone) * 100) / (nbTodo + nbDone - bonus)
    else:
        PCProgress = "NA"

    # TableAvancement += "|"+ReadMe+"|"+TODO+"|"+DONE+"|"+str(PCProgress)+"% |\r\n"
TableAvancement += "\n\n"

# Getting Todos from the worklog
WorklogTodos = "\n\n### Todos from worklog\n"
with open("Worklog.md") as f:
    for line in f:
        if "@todo" in line:
            WorklogTodos += line.replace("@todo", "").replace("  ", " ")


TODOsToShopping = AddShoppingList + TODOsToShopping + WorklogTodos + "\n\n"

# Saving it in a file
OpenWrite(TableAvancement, "include/AddTableAvancement.md")

# Saving it in a file
OpenWrite(TODOsToShopping, "include/AddShoppingList.md")

# -------------------------
# Créer le graphe des modules
# -------------------------

GraphPath = "include/ModulesGraph"
if FullSVG:
    GraphModules.render(GraphPath)
    Svg2Png(GraphPath)

# -------------------------
# Créer le ReadMe
# -------------------------

GraphModulesTxt = "\n# The modules organization \n\n"
GraphModulesTxt += "![Graph](/include/sets/basic.png) \n\n"

FinalDoc = (
    pitch
    + "\n\n"
    + HeaderDocTxt
    + AddStructure
    + GraphModulesTxt
    + TableModules
    + "\n\n"
    + GHList
    + "\n\n"
    + TableAvancement
    + TODOsToShopping
    + TableRetiredDocTxt
    + AddInterfacesDocTxt
    + AddLicenseDocTxt
)
print(GHList)
OpenWrite(GHList, "include/rmGHList.md")
OpenWrite(TableRetiredDocTxt, "include/rmRetiredModules.md")
OpenWrite(TODOsToShopping, "include/rmTODOsToShopping.md")
OpenWrite(TableAvancement, "include/rmTableAvancement.md")

OpenWrite(FinalDoc, "Readme.md.old")

OpenWrite(FinalDoc, "Readme.md.old")

# -------------------------
# Create the slider
# -------------------------

f = open("gh-pages/ppt.md", "w+")
Presentation = (
    "% Habits\n% John Doe\n% March 22, 2005\r\n \r\n"
    + "\n# What do we do?\r\n \r\n"
    + HeaderDocTxt
    + " \n# Graphing the modules\r\n \r\n"
    + GraphModulesTxt
    + " \n# Table Docs\r\n"
    + TableModules
    + "\n\n"
    + GHList
    + "\r\n# Progress\r\n \r\n"
    + TableAvancement
)
f.write(Presentation)
f.close()


# -------------------------
# Graphing the links
# -------------------------


GraphMyMind = digraph()

f = open("Worklog.md", "r")
WorkLogMd = markdown.markdown(f.read())
f.close()
# Getting the TODOs


pattern = r"<li>TODO: (.*?)</li>"
results = re.findall(pattern, WorkLogMd, flags=0)
for item in results:
    GraphMyMind.node(
        item.replace(":", "-"), style="rounded,filled", fillcolor="yellow", penwidth="0"
    )

pattern = r"Graphing</h3>([\s\S]*)</ul>"
results = re.findall(pattern, WorkLogMd, flags=0)
patternCode = r"<li>(.*?)</li>"
for item in results:
    Pairs = map(str, re.findall(patternCode, item, flags=0))
    for eachPair in Pairs:
        eachPair = eachPair.replace("<li>", "")
        eachPair = eachPair.replace("</li>", "")
        Couples = eachPair.split("-&gt;")
        for single in Couples:
            GraphMyMind.node(single, penwidth="0")
        # Add the edge
        for k in range(len(Couples) - 1):
            GraphMyMind.edge(Couples[k], Couples[k + 1])

GraphPath = "include/GraphMyMind"
GraphMyMind = apply_styles(GraphMyMind, styles)

if FullSVG:
    GraphMyMind.render(GraphPath)
    Svg2Png(GraphPath)


# -------------------------
# Creating blog posts with the worklog
# -------------------------
if 0:

    f = open("Worklog.md", "r")
    WorkLogText = f.read()
    ReadMehHtmlMarkdown = markdown.markdown(WorkLogText)
    f.close()

    # Getting the title of the article
    pattern = r"<h4>(\d{4}-\d{2}-\d{2}.*)<\/h4>"  # gets the contents
    results = re.findall(pattern, ReadMehHtmlMarkdown, flags=0)
    titre = r"(.?*)<\/h4>"  # gets the titles
    resultstitre = re.findall(pattern, results[0], flags=0)

    ListePosts = []
    for content in results:
        pair = []
        pattern2 = r"" + content + "<\/h4>[\s\S]*?<h"  # gets the titles
        results2 = "<h4>" + re.findall(pattern2, ReadMehHtmlMarkdown, flags=0)[0] + "4>"
        contenu = results2 + "\n\n\n"
        tmp = re.findall(pattern, contenu, flags=0)[0]
        pair.append(tmp)
        pair.append(contenu)
        ListePosts.append(pair)

    for item in ListePosts:
        titre = str(item[0])
        titre2 = titre
        titre = titre.replace(" ", "-")
        adresse = "./gh-pages/_posts/" + titre + ".html"
        postcontent = str(item[1])
        entete = "--- <p>layout: post<p>title: " + titre2 + "<p>---<p>"
        # We save the post
        text_file = open(adresse, "w")
        text_file.write(entete + postcontent)
        text_file.close()

    log.append("__[WEB Blog]__ " + str(len(ListePosts)) + " posts added" + "\n")
print("Doing the the probes")
GrosJaSON = CreateProbesFiles(GrosJaSON)

# -------------------------------------------------- #
#                    Gitbooking                      #
# -------------------------------------------------- #
if 0:
    # -------------------------
    # Gitbooking worklog
    # -------------------------

    MyLogs = SearchString(WorkLogText, "-------", "uControllers")
    OpenWrite(MyLogs, "include/AddMyLogs.md")

    # -------------------------
    # Preface
    # -------------------------

    Preface = AddRawHURL(
        AddOneLevel(getText("include/AddPitch.md"))
        + "\n"
        + getText("include/AddEchomods.md")
    )
    OpenWrite(IncludeImage(Preface), "gitbook/README.md")

    # -------------------------
    # Adding CHAPTER 1 : Histoire et principe des ultrasons
    # -------------------------

    CopyGitBookFile("include/AddHistory.md", "gitbook/Chapter1/history.md")
    CopyGitBookFile("/WordOfCaution.md", "gitbook/caution.md")

    AddEngineering = getText("include/AddEngineering.md")
    OpenWrite(
        IncludeImage(AddRawHURL(AddEngineering)), "gitbook/Chapter1/engineering.md"
    )

    PrinciplesOfEchoes = ""
    f = open("include/AddPrinciples.md", "r")
    PrinciplesOfEchoes += f.read()
    f.close()
    f = open("include/AddStructure.md", "r")
    PrinciplesOfEchoes += f.read()
    f.close()
    f = open("include/AddStructureDetails.md", "r")
    PrinciplesOfEchoes += f.read()
    f.close()

    OpenWrite(
        IncludeImage(AddRawHURL(PrinciplesOfEchoes)), "gitbook/Chapter1/principles.md"
    )
    OpenWrite(AddRawHURL(HeaderDocTxt), "gitbook/Chapter1/modules.md")

    CopyGitBookFile("include/NDT.md", "gitbook/Chapter1/ndt.md")

    # list of modules
    OpenWrite(
        IncludeImage(AddRawHURL(TableModulesShort + "\n\n" + TableRetiredDocTxt)),
        "gitbook/Chapter1/listofmodules.md",
    )

    # -------------------------
    # Adding Quickstart
    # -------------------------

    # GrosJaSON = CreateProbesFiles(GrosJaSON)
    for probe in GrosJaSON["probes"].keys():
        CopyGitBookFile(
            "include/probes/auto/" + probe + ".md", "gitbook/probes/" + probe + ".md"
        )

    CopyGitBookFile("include/probes/Readme.md", "gitbook/probes/Readme.md")

    CopyGitBookFile("include/QuickStart.md", "gitbook/Chapter1/QuickStart.md")

    # -------------------------
    # Adding RPi article
    # -------------------------

    # RPI = GetIncludes(getText("include/RPiHSDK.md"),  MDFiles[5], MDFiles[4],"include/RPiHSDK.md")
    # RPI_article = RPI[0]
    # OpenWrite(IncludeImage(AddRawHURL(RPI_article)),"gitbook/RPI.md")
    # log += RPI[1]
    CopyGitBookFile("include/RPiHSDK.md", "gitbook/RPI.md")

    # -------------------------
    # Adding CHAPTER 2 : Basic kit
    # -------------------------

    for eachModule in ModulesChaptDeux:
        ModuleDesc = getText(eachModule + "/Readme.md")
        OpenWrite(
            AddRawHURL(GitBookizeModule(ModuleDesc, eachModule)) + "\n\n",
            "gitbook/Chapter2/" + eachModule + ".md",
        )

    for eachModule in ModulesChaptDeuxRT:
        ModuleDesc = getText("./retired/" + eachModule + "/Readme.md")
        OpenWrite(
            AddRawHURL(GitBookizeModule(ModuleDesc, "retired/" + eachModule)) + "\n\n",
            "gitbook/Chapter2/" + eachModule + ".md",
        )

    # Resume pour Murgen
    MurgenSummary = "# The first iteration, Murgen\n\n"
    f = open("include/AddMurgenSummary.md", "r")
    MurgenSummary = MurgenSummary + "\n\n" + AddOneLevel(f.read())
    f.close()
    f = open("./../murgen-dev-kit/Readme.md", "r")
    MurgenSummary = MurgenSummary + "\n\n" + AddOneLevel(f.read())
    f.close()
    OpenWrite(AddRawMurgenURL(MurgenSummary) + "\n\n", "gitbook/devkit0.md")

    # Resume pour le wireless

    WirelessSet = "# Wireless implementation of the modules\n\n" + "\n\n"
    WirelessSet += AddOneLevel(getText("include/AddWireless.md")) + "\n\n"
    WirelessSet += AddOneLevel(getText("include/sets/wifi-dev-kit.cost.md")) + "\n\n"
    WirelessSet += (
        AddOneLevel(
            getText(
                "retired/croaker/data/20161217/20161217-TestingArduinoAndPhantom.md"
            )
        )
        + "\n\n"
    )
    OpenWrite(IncludeImage(AddRawHURL(WirelessSet)) + "\n\n", "gitbook/devkit11.md")

    # Resume pour le basicdevkit

    BasicKit = "# Basic Dev Kit with BeagleBone\n\n" + "\n\n"
    BasicKit += AddOneLevel(getText("include/AddBasicDevKit.md")) + "\n\n"
    BasicKit += AddOneLevel(getText("include/sets/highspeed.cost.md")) + "\n\n"
    BasicKit += AddOneLevel(getText("include/AddBasicDevKitResults.md")) + "\n\n"
    OpenWrite(BasicKit + "\n\n", "include/basicdevkit.md")

    OpenWrite(
        IncludeImage(AddRawHURL(BasicKit)) + "\n\n", "gitbook/Chapter2/basicdevkit.md"
    )

    # Resume technique de Murgen
    OpenWrite(
        AddRawHURL(getText("include/AddIntroMurgen.md")) + "\n\n",
        "gitbook/Chapter2/murgensetup.md",
    )

    # Adding zach's work
    Zach = ""
    f = open("./../murgen-dev-kit/worklog/Zach/Zach.md", "r")
    Zach = f.read()
    f.close()

    f = open("./../murgen-dev-kit/worklog/Zach/2016-06-22.md", "r")
    Zach = Zach + "\n\n" + AddOneLevel(f.read())
    f.close()

    f = open("./../murgen-dev-kit/worklog/Zach/2016-07-06.md", "r")
    Zach = Zach + "\n\n" + AddOneLevel(f.read())
    f.close()

    OpenWrite(AddRawMurgenURL(Zach) + "\n\n", "gitbook/Chapter2/zach.md")
    OpenWrite(
        AddRawMurgenURL(getText("./../murgen-dev-kit/hardware/Readme.md")) + "\n\n",
        "gitbook/Chapter2/murgenhardware.md",
    )
    OpenWrite(
        AddRawMurgenURL(getText("./../murgen-dev-kit/software/Readme.md")) + "\n\n",
        "gitbook/Chapter2/murgensoftware.md",
    )

    # -------------------------
    # Adding CHAPTER 3 : Modules
    # -------------------------

    for eachModule in ModulesChaptTrois:
        ModuleDesc = getText(eachModule + "/Readme.md")
        OpenWrite(
            AddRawHURL(GitBookizeModule(ModuleDesc, eachModule)) + "\n\n",
            "gitbook/Chapter3/" + eachModule + ".md",
        )

    for eachModule in ModulesChaptTroisRT:
        ModuleDesc = getText("./retired/" + eachModule + "/Readme.md")
        OpenWrite(
            AddRawHURL(GitBookizeModule(ModuleDesc, "retired/" + eachModule)) + "\n\n",
            "gitbook/Chapter3/" + eachModule + ".md",
        )

    CopyGitBookBomanzFile("../bomanz/Readme.md", "gitbook/Chapter3/bomanz.md")
    CopyGitBookBomanzFile(
        "../bomanz/20170430-PushingADCLimits.md", "gitbook/Chapter3/bomanz2.md"
    )

    CopyGitBookFile(
        "retroATL3/2017-05-20_APeakInside.md", "gitbook/Chapter3/atl_more.md"
    )

    # -------------------------
    # Adding CHAPTER 4 : Notes and worklog
    # -------------------------

    walk_dir = "./"
    DetailedLogs = []
    notesLogs = []
    for root, subdirs, files in os.walk(walk_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            if (
                ".md" in filename in filename
                and not "gh-pages" in file_path
                and not "gitbook" in file_path
            ):
                if "2016-" in filename:
                    DetailedLogs.append(file_path)
                if "notes_" in filename:
                    notesLogs.append(file_path)

    detailedLogText = "# Detailed logs of experiments\n\n"
    for detailedlog in DetailedLogs:
        Adddetailedlog = open(detailedlog)
        detailedlog = detailedlog.split("/")[-1].replace(".md", "")
        detailedLogText += "# " + detailedlog + "\n\n"
        detailedLogText += AddTwoLevels(Adddetailedlog.read()) + "\n\n"
        Adddetailedlog.close()

    detailedNotesText = "# Detailed notes of research\n\n"
    for detailednote in notesLogs:
        Adddetailednote = open(detailednote)
        detailednote = (
            detailednote.split("/")[-1]
            .replace(".md", "")
            .replace("notes_", "Notes on ")
        )
        detailedNotesText += "# " + detailednote + "\n\n"
        detailedNotesText += AddTwoLevels(Adddetailednote.read()) + "\n\n"
        Adddetailednote.close()

    # Saving it in a file
    OpenWrite("# Introduction to the Chapter 4\n\n", "gitbook/Chapter4/README.md")
    OpenWrite(AddRawHURL(detailedLogText) + "\n\n", "gitbook/Chapter4/detailedlog.md")
    OpenWrite(
        AddRawHURL(detailedNotesText) + "\n\n", "gitbook/Chapter4/detailednotes.md"
    )
    OpenWrite(
        "# Raw worklog\n\n" + AddRawHURL(WorkLogLevel(MyLogs)) + "\n\n",
        "gitbook/Chapter4/rawworklog.md",
    )

    # Adding murgen's work

    Sessions = []
    for SessionLog in ListOfMurgenSessions:
        f = open("./../murgen-dev-kit/worklog/" + SessionLog, "r")
        Sessions.append(f.read())
        f.close()
    for i in range(len(Sessions)):
        OpenWrite(
            AddRawMurgenURL(Sessions[i]) + "\n\n",
            "gitbook/Chapter4/" + ListOfMurgenSessions[i],
        )
    # And the log
    CopyGitBookMurgenFile(
        "./../murgen-dev-kit/worklog/notes.md", "gitbook/Chapter4/murgenworklog.md"
    )

    # -------------------------
    # Adding CHAPTER 5 : Data
    # -------------------------

    DataFormat = getText("include/AddFormatRules.md")
    OpenWrite(
        "# DataFormat \n\n" + AddRawHURL(DataFormat) + "\n\n",
        "gitbook/Chapter5/dataformat.md",
    )

    Examples = getText("./../murgen-dev-kit/software/examples/Readme.md").split("# ")
    TableDataExamples = "# " + Examples[-1]
    OpenWrite(
        "# Still images from murgen \n\n" + TableDataExamples + "\n\n",
        "gitbook/Chapter5/images.md",
    )

    Examples_croaker = getText("retired/croaker/data/examples/Readme.md")
    OpenWrite(
        "# Images acquired using Croaker \n\n"
        + AddRawHURL(AddOneLevel(Examples_croaker))
        + "\n\n",
        "gitbook/Chapter5/croaker_data.md",
    )

    Loops = ""
    f = open("include/20160814/20160814a.md", "r")
    Loops += f.read() + "\n\n"
    f.close()
    f = open("include/20160822/2016-08-22-Fantom.md", "r")
    Loops += f.read() + "\n\n"
    f.close()

    OpenWrite(
        "# Adding videos \n\n There are two loops saved so far. \n\n"
        + AddRawHURL(AddOneLevel(Loops))
        + "\n\n",
        "gitbook/Chapter5/loops.md",
    )

    print(ListOfExperiment)

    for expe in ListOfExperiment:
        CopyGitBookFile(
            "include/experiments/auto/" + expe + ".md", "gitbook/exp/" + expe + ".md"
        )

    # -------------------------
    # Adding CHAPTER 6 : Biblio
    # -------------------------

    CopyGitBookFile("include/biblio/bib/Readme.md", "gitbook/Chapter6/FullBiblio.md")

    articles = getText("include/Bibliography.md")
    OpenWrite(
        "# Bibliography \n\n" + AddRawHURL(articles) + "\n\n",
        "gitbook/Chapter6/articles.md",
    )

    electronics = getText("./../murgen-dev-kit/worklog/bibliographie.md").replace(
        "# Our setup\n", ""
    )
    OpenWrite(
        "# Our choice of electronics \n\n" + electronics + "\n\n",
        "gitbook/Chapter6/components.md",
    )

    OpenWrite(
        "# List of modules Interfaces \n\n" + AddRawHURL(AddInterfacesDocTxt) + "\n\n",
        "gitbook/Chapter6/interfaces.md",
    )

    AddDocProcess = getText("include/AddDocProcess.md")
    OpenWrite(
        "# Automating documentation \n\n" + AddRawHURL(AddDocProcess) + "\n\n",
        "gitbook/Chapter6/documentationprocess.md",
    )

    CopyGitBookFile("include/biblio/Readme.md", "gitbook/Chapter6/academicbiblio.md")
    CopyGitBookFile("include/FilesList/AllFiles.md", "gitbook/Chapter6/fileslist.md")

    # Product work
    CopyGitBookFile("include/fda.gov/Readme.md", "gitbook/Chapter6/fda.md")
    CopyGitBookFile("include/AddBench.md", "gitbook/Chapter6/bench.md")
    CopyGitBookFile("include/vscan/Readme.md", "gitbook/Chapter6/vscan.md")
    # Friend work
    CopyGitBookFile("include/community/WillT/Readme.md", "gitbook/Chapter6/c_will.md")

    # -------------------------
    # Adding CHAPTER 7 : Contributing
    # -------------------------

    OpenWrite(
        "# The table of progress \n\n" + TableAvancement + "\n\n",
        "gitbook/Chapter7/progress.md",
    )
    OpenWrite(TODOsToShopping + "\n\n", "gitbook/Chapter7/shoppingList.md")
    OpenWrite(AddLicenseDocTxt + "\n\n", "gitbook/Chapter7/license.md")

    # CopyGitBookFile("CLA.md","gitbook/CLA.md")
    CopyGitBookFile("include/AddDevices.md", "gitbook/Chapter6/otherprobes.md")

    CopyGitBookFile("include/autodoc.md", "gitbook/Chapter7/autodoc.md")

    CopyGitBookFile("include/AddPressReview.md", "gitbook/Chapter7/pressreview.md")

    CopyGitBookFile(
        "retired/croaker/data/20161217/20161217-TestingArduinoAndPhantom.md",
        "gitbook/Chapter4/newphantom.md",
    )

    # -------------------------
    # Adding Readmes (chapters intros)
    # -------------------------

    for i in range(7):
        AddChaptersIntro = getText("./include/AddChaptersIntro.md")
        linesChapters = AddChaptersIntro.split("\n")
        i = i + 1
        ResultatChapter = []
        DebutFound = False

        for line in linesChapters:
            if "#### Chapter" in line:
                if ("Chapter" + str(i)) in line:
                    DebutFound = True
                else:
                    DebutFound = False

            if DebutFound:
                ResultatChapter.append(line)

        OpenWrite(
            "\n".join(ResultatChapter) + "\n\n",
            "gitbook/Chapter" + str(i) + "/Readme.md",
        )


# -------------------------
# Saving the compilation log
# -------------------------
if 0:
    ResultKits = CreateKits("./include/", "./", FullSVG)
    log = log + ResultKits

# -------------------------
# Saving the compilation log
# -------------------------

log.sort()
log = [x.strip() for x in log]
log = [x for x in log if len(x.strip())]
log = list(set(log))
log.sort()
OpenWrite("* "+"\n* ".join(log), "doc/log.md")

urgent = [x.strip() for x in log if ":no_entry:" in x]
OpenWrite("* " + "\n* ".join(urgent), "doc/urgent.md")

# -------------------------
# Updating Summary log
# -------------------------
if 0:
    UpdateSUMMARY("gitbook/toc.md")


with open("include/doc.json", "wt") as out:
    pprint(GrosJaSON, stream=out)
