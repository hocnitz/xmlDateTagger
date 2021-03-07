import easygui
from flask import Flask, render_template
import xml.etree.ElementTree as ET
import os
import datetime
from collections import OrderedDict

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './Web')

datesDict = {}
app = Flask(__name__, template_folder=template_path, static_folder='Web/assets')

@app.route('/')
def index1():
    return render_template('/index.html', content=orderedFormatted, isCounter="0")

@app.route('/counted')
def index2():
    return render_template('/index.html', content=orderedFormatted, isCounter="1")

def reformatDate(date):
    date = date.split('-')
    date = date[::-1]
    date = "/".join(date)
    return date


def validateDate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    path = easygui.fileopenbox(msg="Choose a xml file")
    if path is not None and path.endswith(".xml"):
        originXmlTree = ET.parse(path)
        originRoot = originXmlTree.getroot()

        for element in originRoot.iter():
            if element.tag == 'date':
                if validateDate(element.attrib.get('date')):
                    date = datesDict.get(element.attrib.get('date'), None)
                    refersTo = element.attrib.get('refersTo')

                    if date is None:
                        refersToDict = {}
                        if refersTo is not None:
                            refersToDict[refersTo] = 1

                        datesDict[element.attrib.get('date')] = {'count': 1, 'refersTo': refersToDict}
                    else:
                        date['count'] += 1
                        refersToDict = date.get('refersTo', None)
                        if refersTo is not None and refersToDict is not None:
                            refersToCount = refersToDict.get(refersTo, None)
                            if refersToCount is not None:
                                refersToDict[refersTo] += 1
                            else:
                                refersToDict[refersTo] = 1
    else:
        print("no xml file selected")

    ordered = OrderedDict(sorted(datesDict.items(), key=lambda t: t[0]))
    orderedFormatted = {}
    for key, val in ordered.items():
        x = reformatDate(key)
        orderedFormatted[x] = val

    
    app.run()