import json
from lxml import objectify
import pandas as pd
import os


class XMLToObject:
    def __init__(self, xml):
        self.xml = objectify.parse(xml).getroot().getchildren()

    def steps(self, xml):
        ret = {}
        for ele in xml:
            if str(ele.tag) == 'object':
                ret[ele.tag] = self.get_boundbox(ele)
            elif str(ele) == '':
                ret[str(ele.tag)] = self.steps(ele.getchildren())
            else:
                ret[str(ele.tag)] = str(ele)
        return ret

    def get_boundbox(self, xml):
        piece = xml.getchildren()
        ret = {'parts': []}
        for ele in piece:
            if str(ele) != '':
                ret[str(ele)] = str(ele)
            elif str(ele.tag) == 'bndbox':
                ret[str(ele.tag)] = self.steps(ele.getchildren())
            else:
                part = self.steps(ele.getchildren())
                ret['parts'].append(part)
        return ret


    def run(self):
        ret = self.steps(self.xml)
        return ret


if __name__ == "__main__":
    xml = open('./VOC2012/Annotations/2007_000027.xml')
    xto = XMLToObject(xml)
    xto_res = xto.run()
    with open('./xml_to_obj_test.json', 'w', encoding='utf-8') as fs:
        fs.write(json.dumps(xto_res, indent=4))
        fs.write('\n')