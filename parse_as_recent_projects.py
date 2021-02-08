# coding:utf-8
# !/usr/bin/python
import os
import sys
import xml.sax
from workflow import Workflow

reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = "Egan"

recentProjectPath = os.environ["HOME"] + \
                    "/Library/Application Support/Google/AndroidStudio4.1/options/recentProjects.xml"


class RecentProjectHandler(xml.sax.ContentHandler):
    tempResultList = []

    def __init__(self):
        self.projectName = ""

    def startElement(self, projectName, attributes, resultList=tempResultList):
        self.projectName = projectName
        if projectName == "entry":
            resultList.append(attributes["key"].lstrip())

    # def endElement(self, projectName):
    #     # if self.projectName == ""
    #     print("endElement >>>> " + projectName)
    #
    # def parseContent(self, content):
    #     print("parseContent >>>> " + content)


if __name__ == "__main__":
    wf = Workflow()

    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off name spaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = RecentProjectHandler()
    parser.setContentHandler(Handler)
    # 解析数据
    parser.parse(recentProjectPath)

    # 获取关键字
    keyWord = ""
    if len(wf.args) != 0:
        keyWord = wf.args[0]

    Handler.tempResultList.reverse()
    for i in Handler.tempResultList:
        projectName = str(i)[str(i).rfind("/") + 1:]
        projectPath = str(i).replace("$USER_HOME$", os.environ["HOME"])
        if keyWord:
            if str(keyWord).lower() in projectName.lower():
                wf.add_item(
                    title=projectName,
                    subtitle=projectPath,
                    icon="icon.png",
                    arg=projectPath,
                    valid=True
                )
        else:
            wf.add_item(
                title=projectName,
                subtitle=projectPath,
                icon="icon.png",
                arg=projectPath,
                valid=True
            )
    # 结果发送回 alfred
    wf.send_feedback()
