import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import re


# gregorianMonthNumberArray = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

def findDates(str):
    if str == None:
        return []

    day31 = "(?:(?:31)(?:\/|-|\.)(?:0?[13578]|1[02]))(?:\/|-|\.)"
    day29To30 = "(?:(?:29|30)(?:\/|-|\.)(?:0?[1-9]|1[02]))(?:\/|-|\.)"
    day1To28 = "(?:(?:0?[1-9]|1[0-9]|2[0-8])(?:\/|-|\.)(?:1[02]|0?[1-9]))(?:\/|-|\.)"
    year = "(?:(?:1[0-9]|2[0-9])?[0-9][0-9])"

    regularExp = "(?:(?:" + day31 + "|" + day29To30 + "|" + day1To28 + ")" + year + ")"
    dateArr = re.findall(regularExp, str)

    return dateArr


def addDateTagToNodeFromText(node, dateArr):
    tempStr = node.text
    node.text = tempStr[0: tempStr.index(dateArr[0])]

    for i in range(len(dateArr) - 1):
        element = Element('date')
        element.text = dateArr[i]
        tempStr = tempStr[tempStr.index(dateArr[i]) + len(dateArr[i]):]
        element.tail = tempStr[: tempStr.index(dateArr[i+1])]
        node.insert(i, element)

    i = len(dateArr) - 1
    element = Element('date')
    element.text = dateArr[i]
    tempStr = tempStr[tempStr.index(dateArr[i]) + len(dateArr[i]):]
    element.tail = tempStr
    node.insert(i, element)


def addDateTagToNodeFromTail(node, dateArr):
    tempStr = node.tail
    node.tail = tempStr[0: tempStr.index(dateArr[0])]

    for i in range(len(dateArr) - 1):

        element = Element('date')
        element.text = dateArr[i]
        tempStr = tempStr[tempStr.index(dateArr[i]) + len(dateArr[i]):]
        element.tail = tempStr[0: tempStr.index(dateArr[i + 1])]
        node.append(element)

    i = len(dateArr) - 1
    element = Element('date')
    element.text = dateArr[i]
    tempStr = tempStr[tempStr.index(dateArr[i]) + len(dateArr[i]):]
    element.tail = tempStr
    node.append(element)


def iterateETree(node):
    for child in node.getchildren():
        iterateETree(child)

    nodeTextDates = findDates(node.text)
    nodeTailDates = findDates(node.tail)
    if len(nodeTextDates) > 0:
        addDateTagToNodeFromText(node, nodeTextDates)
    if len(nodeTailDates) > 0:
        addDateTagToNodeFromTail(node, nodeTailDates)


def main():
    originXmlTree = ET.parse("main.xml")
    originRoot = originXmlTree.getroot()
    iterateETree(originRoot)
    tree = ET.ElementTree(originRoot)
    tree.write('fixedRule.xml', 'utf-8')
    print("done!")


if __name__ == "__main__":
    main()
