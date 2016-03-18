#coding=utf-8
from xml.dom import minidom

def get_xml_data(filename='user.xml'):
    doc = minidom.parse(filename) 

    return ""


if __name__ == "__main__":
    #test_xmltostring()
    #test_laod_xml()
    print get_xml_data()
