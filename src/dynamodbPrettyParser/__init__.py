from decimal import Decimal

def parseResults(items):
    items = items.get('Items') or []

    def parseList(dynamoList):
        i = 0
        for d in dynamoList:
            dynamoType = list(d.keys())[0]
            dynamoList[i] = typeMap[dynamoType](d[dynamoType])
            i += 1
        return dynamoList

    def parseMap(dynamoMap):
        for d in dynamoMap:
            dynamoType = list(dynamoMap[d].keys())[0]
            dynamoMap[d] = typeMap[dynamoType](dynamoMap[d][dynamoType])
        return dynamoMap

    typeMap = {
        'S': lambda x: x,
        'N': lambda x: (int, Decimal)[len(x.split('.')) - 1](x),
        'L': parseList,
        'B': str,
        'BS': parseList,
        'BOOL': lambda x: x == 'true',
        'NS': parseList,
        'NULL': lambda: None,
        'SS': list,
        'M': parseMap
    }

    i = 0
    for item in items:
        newItem = {}
        for attributeName in item.keys():
            dynamoType = next(iter(item[attributeName]))
            val = typeMap[dynamoType](item[attributeName][dynamoType])
            newItem[attributeName] = val
        items[i] = newItem
        i += 1

    return items
