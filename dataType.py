from msvcrt import getch
from unicodedata import name


class DataType:
    def __init__(self, name, childList=None, isRoot=False):
        self.name = name
        if childList is None:
            self.childData = []
        else:
            self.childData = childList
        self.isRoot = isRoot

    def getName(self):
        return self.name

    def getConntectorType(self, title, connecter_type=""):
        hasChild = True if len(self.childData) > 0 else False
        if(self.isRoot):
            connecter_type = self.name

        if self.name == title:
            return connecter_type
        else:
            if hasChild:
                for item in self.childData:
                    result = item.getConntectorType(title, connecter_type)
                    if(result):
                        return result

        return ""

    def getSameNames(self, title):
        returnList = []
        if title in self.name:
            returnList.append(self.name)
        for item in self.childData:
            hasChild = True if len(item.childData) > 0 else False
            if title in item.name:
                returnList.append(item.name)
            if hasChild:
                for item2 in item.childData:
                    for item3 in item2.getSameNames(title):
                        if(item3):
                            returnList.append(item3)
        return returnList
