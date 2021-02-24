# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import re
import requests
import json

gregorianDaysFormats = {1: ["1", "01", "ריאשון", "ראשון"],
                        2: ["2", "02", "שני"],
                        3: ["3", "03", "שלישי"],
                        4: ["4", "04", "רביעי"],
                        5: ["5", "05", "חמישי"],
                        6: ["6", "06", "שישי"],
                        7: ["7", "07", "שביעי"],
                        8: ["8", "08", "שמיני"],
                        9: ["9", "09", "תשיעי"],
                        10: ["10", "עשירי"],
                        11: ["11", "אחד עשר", "אחת עשר", "אחד עשרה", "אחת עשרה"],
                        12: ["12", "שני עשר", "שתי עשר", "שני עשרה", "שתי עשרה", "שתיים עשר", "שתיים עשרה", "שניים עשר", "שניים עשרה"],
                        13: ["13", "שלוש עשר", "שלושה עשר", "שלוש עשרה", "שלושה עשרה"],
                        14: ["14", "ארבע עשר", "ארבעה עשר", "ארבע עשרה", "ארבעה עשרה"],
                        15: ["15", "חמש עשר", "חמישה עשר", "חמש עשרה", "חמישה עשרה", "חמשה עשר", "חמשה עשרה"],
                        16: ["16", "שש עשר", "שישה עשר", "שש עשרה", "שישה עשרה", "ששה עשר", "ששה עשרה"],
                        17: ["17", "שבע עשר", "שבעה עשר", "שבע עשרה", "שבעה עשרה", "שיבעה עשר", "שיבעה עשרה"],
                        18: ["18", "שמונה עשר", "שמונה עשרה"],
                        19: ["19", "תשע עשר", "תשעה עשר", "תשע עשרה", "תשעה עשרה", "תישעה עשר", "תישעה עשרה"],
                        20: ["20", "עשרים"],
                        21: ["21", "עשרים ואחד", "עשרים ואחת"],
                        22: ["22", "עשרים ושתיים", "עשרים ושניים"],
                        23: ["23", "עשרים ושלוש"],
                        24: ["24", "עשרים וארבע"],
                        25: ["25", "עשרים וחמש"],
                        26: ["26", "עשרים ושש"],
                        27: ["27", "עשרים ושבע"],
                        28: ["28", "עשרים ושמונה"],
                        29: ["29", "עשרים ותשע"],
                        30: ["30", "שלושים"],
                        31: ["31", "שלושים ואחד", "שלושים ואחת"]}

gregorianMonthFormats = {1: ["1", "01", "ראשון", "ריאשון", "ינואר"],
                         2: ["2", "02", "שני", "פברואר"],
                         3: ["3", "03", "שלישי", "מרץ"],
                         4: ["4", "04", "רביעי", "אפריל"],
                         5: ["5", "05", "חמישי", "מאי"],
                         6: ["6", "06", "שישי", "יוני"],
                         7: ["7", "07", "שביעי", "יולי"],
                         8: ["8", "08", "שמיני", "אוגוסט"],
                         9: ["9", "09", "תשיעי", "ספטמבר"],
                         10: ["10", "עשירי", "אוקטובר"],
                         11: ["11", "נובמבר", "אחד עשר", "אחד עשרה", "אחת עשר", "אחת עשרה"],
                         12: ["12", "דצמבר", "שתיים עשר", "שתיים עשרה", "שניים עשר", "שניים עשרה"]}

gregorianMonthNameArray = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"]

gregorianYear = "(?:(?:1[0-9]|2[0-9])?[0-9][0-9])"

hebrewDaysFormats = {1: ["א", "א'", "א׳"],
                     2: ["ב", "ב'", "ב׳"],
                     3: ["ג", "ג'", "ג׳"],
                     4: ["ד", "ד'", "ד׳"],
                     5: ["ה", "ה'", "ה׳"],
                     6: ["ו", "ו'", "ו׳"],
                     7: ["ז", "ז'", "ז׳"],
                     8: ["ח", "ח'", "ח׳"],
                     9: ["ט", "ט'", "ט׳"],
                     10: ["י", "י'", "י׳"],
                     11: ["יא", "י\"א", "י״א"],
                     12: ["יב", "י\"ב", "י״ב"],
                     13: ["יג", "י\"ג", "י״ג"],
                     14: ["יד", "י\"ד", "י״ד"],
                     15: ["טו", "ט\"ו", "ט״ו"],
                     16: ["טז", "ט\"ז", "ט״ז"],
                     17: ["יז", "י\"ז", "י״ז"],
                     18: ["יח", "י\"ח", "י״ח"],
                     19: ["יט", "י\"ט", "י״ט"],
                     20: ["כ", "כ'", "כ׳"],
                     21: ["כא", "כ\"א", "כ״א"],
                     22: ["כב", "כ\"ב", "כ״ב"],
                     23: ["כג", "כ\"ג", "כ״ג"],
                     24: ["כד", "כ\"ד", "כ״ד"],
                     25: ["כה", "כ\"ה", "כ״ה"],
                     26: ["כו", "כ\"ו", "כ״ו"],
                     27: ["כז", "כ\"ז", "כ״ז"],
                     28: ["כח", "כ\"ח", "כ״ח"],
                     29: ["כט", "כ\"ט", "כ״ט"],
                     30: ["ל", "ל'", "ל׳"]}

hebrewMonthFormats = {"Nisan": ["ניסן"],
                      "Iyyar": ["אייר", "איר"],
                      "Sivan": ["סיוון", "סיון"],
                      "Tamuz": ["תמוז"],
                      "Av": ["אב"],
                      "Elul": ["אלול"],
                      "Tishrei": ["תשרי"],
                      "Cheshvan": ["חשוון", "מרחשון", "מרחשוון"],
                      "Kislev": ["כסלו", "כסליו"],
                      "Tevet": ["טבת"],
                      "Shvat": ["שבט"],
                      "Adar1": ["אדר א'?"],
                      "Adar2": ["אדר ב'?", "אדר"]}

hebrewYear = "(?:[א-ת][א-ת][א-ת](?:״|\")?[א-ת])"

hebrewMonthArray = ["Nisan", "Iyyar", "Sivan", "Tamuz", "Av", "Elul", "Tishrei", "Cheshvan", "Kislev", "Tevet", "Shvat", "Adar1", "Adar2"]

gematriaValues = {'א': 1,
                  'ב': 2,
                  'ג': 3,
                  'ד': 4,
                  'ה': 5,
                  'ו': 6,
                  'ז': 7,
                  'ח': 8,
                  'ט': 9,
                  'י': 10,
                  'כ': 20,
                  'ל': 30,
                  'מ': 40,
                  'נ': 50,
                  'ס': 60,
                  'ע': 70,
                  'פ': 80,
                  'צ': 90,
                  'ק': 100,
                  'ר': 200,
                  'ש': 300,
                  'ת': 400
                  }

separators = [",", "-", "\.", "\/", "ה", "ל", " ", "ב", "מ"]

idCounter = 0

datesDict = {}

def makeSeparatorsExp():
    exp = " ?(?:-|:)? ?"
    return exp + "(?:" + "|".join(separators) + ")" + exp


def makeOrExp(keys, dictionary):
    valsArr = []
    for key in keys:
        valsArr.append(dictionary.get(key))

    orExp = "(?:"
    for val in valsArr:
        orExp += '|'.join(val) + '|'

    orExp = orExp[0: len(orExp) - 1] + ")"
    return orExp


def getHebrewDateAttribute(date):
    d = "??"
    m = "??"
    y = "????"

    separate = [",", "-", "\.", "\/", " "]
    separatedDate = re.split("|".join(separate), date)
    while "" in separatedDate:
        separatedDate.remove("")

    findDay = re.findall(makeOrExp(reversed(range(1, 31)), hebrewDaysFormats), separatedDate[0])
    for day, value in reversed(hebrewDaysFormats.items()):
        if findDay[0] in value:
            d = "%s" % day
            break
    findMonth = re.findall(makeOrExp(hebrewMonthArray, hebrewMonthFormats), separatedDate[1])
    for month, value in reversed(hebrewMonthFormats.items()):
        if findMonth[0] in value:
            m = "%s" % month
            break
    findYear = re.findall(hebrewYear, separatedDate[2])[0]
    findYear = findYear.replace('״', '')
    findYear = findYear.replace('"', '')

    y = "%s" % (getGematriaValue(findYear) + 1240)

    return y + "-" + m + "-" + d


def getGematriaValue(str):
    count = 0
    for c in str:
        x = gematriaValues.get(c)
        count += x

    return count


def getGregorianDateAttribute(date):
    separate = [",", "-", "\.", "\/", " "]
    separatedDate = re.split("|".join(separate), date)
    while "" in separatedDate:
        separatedDate.remove("")

    monthNameExp = "(?:" + "|".join(gregorianMonthNameArray) + ")"
    between13To31Exp = "(?:(?:1[3-9])|(?:2[0-9])|(?:3[0-1]))"
    dayGreaterThan12Exp = makeOrExp(reversed(range(13, 32)), gregorianDaysFormats)

    if len(separatedDate) == 2:
        findMonthInCell0 = re.findall(monthNameExp, separatedDate[0])
        findDayGreaterThan12InCell1 = re.findall(dayGreaterThan12Exp, separatedDate[1])
        if len(findMonthInCell0) > 0 | len(findDayGreaterThan12InCell1) > 0:
            return generateGregorianDateAttribute(separatedDate, 1, 0, None)

        return generateGregorianDateAttribute(separatedDate, 0, 1, None)

    elif len(separatedDate) == 3:
        findMonthInCell0 = re.findall(monthNameExp, separatedDate[0])
        findMonthInCell1 = re.findall(monthNameExp, separatedDate[1])
        findMonthInCell2 = re.findall(monthNameExp, separatedDate[2])

        findDayInCell0 = re.findall(makeOrExp(reversed(range(1, 32)), gregorianDaysFormats), separatedDate[0])
        findDayInCell1 = re.findall(makeOrExp(reversed(range(1, 32)), gregorianDaysFormats), separatedDate[1])
        findDayInCell2 = re.findall(makeOrExp(reversed(range(1, 32)), gregorianDaysFormats), separatedDate[2])

        findDayGreaterThan12InCell0 = re.findall(dayGreaterThan12Exp, separatedDate[0])
        findDayGreaterThan12InCell1 = re.findall(dayGreaterThan12Exp, separatedDate[1])
        findDayGreaterThan12InCell2 = re.findall(dayGreaterThan12Exp, separatedDate[2])

        findRange13To31InCell0 = re.findall(between13To31Exp, separatedDate[0])
        findRange13To31InCell1 = re.findall(between13To31Exp, separatedDate[1])
        findRange13To31InCell2 = re.findall(between13To31Exp, separatedDate[2])

        findYearInCell0 = re.findall("(?:(?:(?:[4-9][0-9])|(?:3[2-9]))|(?:[1-9][0-9][0-9][0-9]))", separatedDate[0])
        findYearInCell2 = re.findall("(?:(?:(?:[4-9][0-9])|(?:3[2-9]))|(?:[1-9][0-9][0-9][0-9]))", separatedDate[2])

        if len(findYearInCell0) > 0:
            return generateGregorianDateAttribute(separatedDate, 2, 1, 0)
        elif len(findYearInCell2) > 0:
            if len(findMonthInCell0) > 0:
                return generateGregorianDateAttribute(separatedDate, 1, 0, 2)
            elif len(findMonthInCell1) > 0:
                return generateGregorianDateAttribute(separatedDate, 0, 1, 2)
            elif len(findDayGreaterThan12InCell0) > 0:
                return generateGregorianDateAttribute(separatedDate, 0, 1, 2)
            elif len(findDayGreaterThan12InCell1) > 0:
                return generateGregorianDateAttribute(separatedDate, 1, 0, 2)
            return generateGregorianDateAttribute(separatedDate, 0, 1, 2)
        else:
            if len(findMonthInCell0) > 0:
                return generateGregorianDateAttribute(separatedDate, 1, 0, 2)
            elif len(findMonthInCell1) > 0:
                return generateGregorianDateAttribute(separatedDate, 0, 1, 2)
            else:
                if len(findRange13To31InCell0) > 0 & len(findRange13To31InCell2) > 0:
                    return generateGregorianDateAttribute(separatedDate, 0, 1, 2)
                elif  len(findRange13To31InCell1) > 0 & len(findRange13To31InCell2) > 0:
                    return generateGregorianDateAttribute(separatedDate, 1, 0, 2)
                elif len(findDayGreaterThan12InCell0) > 0:
                    return generateGregorianDateAttribute(separatedDate, 0, 1, 2)
                elif len(findDayGreaterThan12InCell1) > 0:
                    return generateGregorianDateAttribute(separatedDate, 1, 0, 2)
                else:
                    if len(findDayInCell0) > 0 & len(findDayInCell1) > 0:
                        return generateGregorianDateAttribute(separatedDate, 0, 1, 2)
                    elif len(findDayInCell1) > 0 & len(findDayInCell2) > 0:
                        return generateGregorianDateAttribute(separatedDate, 1, 2, 0)

        return generateGregorianDateAttribute(separatedDate, 0, 1, 2)


def generateGregorianDateAttribute(separatedDate, dayIndex, monthIndex, yearIndex):
    d = "??"
    m = "??"
    y = "????"

    findDay = re.findall(makeOrExp(reversed(range(1, 32)), gregorianDaysFormats), separatedDate[dayIndex])
    for day, value in reversed(gregorianDaysFormats.items()):
        if findDay[0] in value:
            if day > 9:
                d = "%s" % day
            else:
                d = "0%s" % day
            break

    findMonth = re.findall(makeOrExp(reversed(range(1, 13)), gregorianMonthFormats), separatedDate[monthIndex])
    if len(findMonth) > 0:
        for month, value in reversed(gregorianMonthFormats.items()):
            if findMonth[0] in value:
                if month > 9:
                    m = "%s" % month
                else:
                    m = "0%s" % month
                break

    if yearIndex is not None:
        if len(separatedDate[yearIndex]) < 3:
            if int(separatedDate[yearIndex]) > 30:
                y = "% s" % (1900 + int(separatedDate[2]))
            else:
                y = "% s" % (2000 + int(separatedDate[2]))
        else:
            y = separatedDate[yearIndex]

    return y + "-" + m + "-" + d


def getDatesForAttribute(dateArr, dayIndex, monthIndex, yearIndex):
    dateAttributeArr = []
    for date in dateArr:
        separate = [",", "-", "\.", "\/", " "]
        separatedDate = re.split("|".join(separate), date)
        while "" in separatedDate:
            separatedDate.remove("")

        d = re.findall(makeOrExp(reversed(range(1, 32)), gregorianDaysFormats), separatedDate[dayIndex])
        for day, value in reversed(gregorianDaysFormats.items()):
            if d in value:
                separatedDate[dayIndex] = "% s" % day
                break

        m = re.findall(makeOrExp(reversed(range(1, 13)), gregorianMonthFormats), separatedDate[monthIndex])
        for month, value in reversed(gregorianMonthFormats.items()):
            if m[0] in value:
                separatedDate[monthIndex] = "% s" % month
                break
        if len(separatedDate) == 2:
            dateAttributeArr.append("????-" + separatedDate[monthIndex] + "-" + separatedDate[dayIndex])
        elif len(separatedDate) == 3:
            if len(separatedDate[yearIndex]) < 3:
                if int(separatedDate[yearIndex]) > 30:
                    separatedDate[yearIndex] = "% s" % (1900 + int(separatedDate[2]))
                else:
                    separatedDate[yearIndex] = "% s" % (2000 + int(separatedDate[2]))
            dateAttributeArr.append(separatedDate[yearIndex] + "-" + separatedDate[monthIndex] + "-" + separatedDate[dayIndex])

    return dateAttributeArr


def removeSpacesInEndOfString(str):
    while str[-1] == " ":
        str = str[: len(str) - 1]
    return str


def findDates(str):
    if str is None:
        return []

    gregorianDayMonthYear = "(?:" + makeOrExp(reversed(range(1, 32)), gregorianDaysFormats) + makeSeparatorsExp() + makeOrExp(reversed(range(1, 13)), gregorianMonthFormats) + makeSeparatorsExp() + gregorianYear + ")"
    gregorianDayMonth = "(?:" + makeOrExp(reversed(range(1, 32)), gregorianDaysFormats) + makeSeparatorsExp() + makeOrExp(reversed(range(1, 13)), gregorianMonthFormats) + makeSeparatorsExp() + ")"
    gregorianMonthDayYear = "(?:" + makeOrExp(reversed(range(1, 13)), gregorianMonthFormats) + makeSeparatorsExp() + makeOrExp(reversed(range(1, 32)), gregorianDaysFormats) + makeSeparatorsExp() + gregorianYear + ")"
    gregorianMonthDay = "(?:" + makeOrExp(reversed(range(1, 13)), gregorianMonthFormats) + makeSeparatorsExp() + makeOrExp(reversed(range(1, 32)), gregorianDaysFormats) + makeSeparatorsExp() + ")"
    gregorianYearMonthDay = "(?:" + gregorianYear + makeSeparatorsExp() + makeOrExp(reversed(range(1, 13)), gregorianMonthFormats) + makeSeparatorsExp() + makeOrExp(reversed(range(1, 32)), gregorianDaysFormats) + ")"

    hebrewDayMonthYear = "(?:" + makeOrExp(reversed(range(1, 31)), hebrewDaysFormats) + makeSeparatorsExp() + makeOrExp(hebrewMonthArray, hebrewMonthFormats) + makeSeparatorsExp() + hebrewYear + ")"

    allExps = "(?:" + gregorianDayMonthYear + "|" + gregorianDayMonth + "|" + gregorianMonthDayYear + "|" + gregorianMonthDay + "|" + gregorianYearMonthDay + "|" + hebrewDayMonthYear + ")"


    dateArr = re.findall(allExps, str)
    # dateArr = re.findall(hebrewDayMonthYear, str)

    return dateArr


def idGen():
    global idCounter
    idCounter += 1
    return "date_" + str(idCounter)


def addDateTagToNodeFromText(node, dateArr):
    date = ""
    if node.tag == "date":
        return
    id = idGen()
    tempStr = node.text
    node.text = tempStr[0: tempStr.index(dateArr[0])]

    for i in range(len(dateArr) - 1):
        dateArr[i] = removeSpacesInEndOfString(dateArr[i])
        if len(re.findall(makeOrExp(hebrewMonthArray, hebrewMonthFormats), dateArr[i])) > 0:
            date = getHebrewDateAttribute(dateArr[i])
        else:
            date = getGregorianDateAttribute(dateArr[i])
        alternativeDate = datesDict.get(date, None)
        if alternativeDate is None:
            datesDict[date] == id
            element = ET.Element('date', attrib={'eId': id, 'date': date})
        else:
            element = ET.Element('date', attrib={'eId': id, 'date': date, 'alternativeTo' : alternativeDate})
        element.text = dateArr[i]
        tempStr = tempStr[tempStr.index(dateArr[i]) + len(dateArr[i]):]
        element.tail = tempStr[: tempStr.index(dateArr[i + 1])]
        node.insert(i, element)

    i = len(dateArr) - 1
    dateArr[i] = removeSpacesInEndOfString(dateArr[i])
    if len(re.findall(makeOrExp(hebrewMonthArray, hebrewMonthFormats), dateArr[i])) > 0:
        date = getHebrewDateAttribute(dateArr[i])
    else:
        date = getGregorianDateAttribute(dateArr[i])
    alternativeDate = datesDict.get(date, None)
    if alternativeDate is None:
        datesDict[date] = id
        element = ET.Element('date', attrib={'eId': id, 'date': date})
    else:
        element = ET.Element('date', attrib={'eId': id, 'date': date, 'alternativeTo' : alternativeDate})
    element.text = dateArr[i]
    tempStr = tempStr[tempStr.index(dateArr[i]) + len(dateArr[i]):]
    element.tail = tempStr
    node.insert(i, element)


def addDateTagToNodeFromTail(node, dateArr):
    date = ""
    if node.tag == "date":
        return

    tempStr = node.tail
    node.tail = tempStr[0: tempStr.index(dateArr[0])]
    id = idGen()

    for i in range(len(dateArr) - 1):
        dateArr[i] = removeSpacesInEndOfString(dateArr[i])
        if len(re.findall(makeOrExp(hebrewMonthArray, hebrewMonthFormats), dateArr[i])) > 0:
            date = getHebrewDateAttribute(dateArr[i])
        else:
            date = getGregorianDateAttribute(dateArr[i])
        alternativeDate = datesDict.get(date, None)
        if alternativeDate is None:
            datesDict[date] = id
            element = ET.Element('date', attrib={'eId': id, 'date': date})
        else:
            element = ET.Element('date', attrib={'eId': id, 'date': date, 'alternativeTo' : alternativeDate})
        element.text = dateArr[i]
        tempStr = tempStr[tempStr.index(dateArr[i]) + len(dateArr[i]):]
        element.tail = tempStr[0: tempStr.index(dateArr[i + 1])]
        node.append(element)

    i = len(dateArr) - 1
    dateArr[i] = removeSpacesInEndOfString(dateArr[i])
    if len(re.findall(makeOrExp(hebrewMonthArray, hebrewMonthFormats), dateArr[i])) > 0:
        date = getHebrewDateAttribute(dateArr[i])
    else:
        date = getGregorianDateAttribute(dateArr[i])
    alternativeDate = datesDict.get(date, None)
    if alternativeDate is None:
        datesDict[date] = id
        element = ET.Element('date', attrib={'eId': id, 'date': date})
    else:
        element = ET.Element('date', attrib={'eId': id, 'date': date, 'alternativeTo' : alternativeDate})
    element.text = dateArr[i]
    tempStr = tempStr[tempStr.index(dateArr[i]) + len(dateArr[i]):]
    element.tail = tempStr
    node.append(element)


def iterateETree(node):
    nodeTextDates = findDates(node.text)
    nodeTailDates = findDates(node.tail)
    if len(nodeTextDates) > 0:
        addDateTagToNodeFromText(node, nodeTextDates)
    if len(nodeTailDates) > 0:
        addDateTagToNodeFromTail(node, nodeTailDates)

    for child in node.iter():
        if child is not node:
            iterateETree(child)

#--------------------------------------------test for api ------------------------------------------------
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=1)
    print(text)

def test():
    # api site : https://www.hebcal.com/home/219/hebrew-date-converter-rest-api
    # in url string:
    # hy = hebrew year, hm = Hebrew month, hd = hebrew day. h2g = hebrew to georgian, cfg = what file type to return
    response = requests.get("https://www.hebcal.com/converter?cfg=json&hy=5749&hm=Kislev&hd=25&h2g=1")
    print(response.status_code)
    jprint(response.json())
#------------------------------------------------------------------------------------------------------

def main():
    originXmlTree = ET.parse("main.xml")
    originRoot = originXmlTree.getroot()
    iterateETree(originRoot)
    tree = ET.ElementTree(originRoot)
    tree.write('fixedRule.xml', 'utf-8')
    print("done!")
    test()


if __name__ == "__main__":
    main()
