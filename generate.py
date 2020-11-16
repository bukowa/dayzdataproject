import xml.etree.ElementTree as ET

data = []

tree = ET.parse('./dayzOffline.chernarusplus/db/types.xml')
root = tree.getroot()

basic_int = lambda x: (x.tag, int(x.text))
basic_str = lambda x: (x.tag, x.attrib["name"].lower())
basic_str_list = lambda x: (x.tag, [x.attrib["name"].lower()])


CONVERT = {
    "nominal": basic_int,
    "lifetime": basic_int,
    "restock": basic_int,
    "min": basic_int,
    "quantmin": basic_int,
    "quantmax": basic_int,
    "cost": basic_int,
    "flags": lambda x: (x.tag, {kk: int(vv) for kk, vv in x.attrib.items()}),
    "category": basic_str,
    "usage": basic_str_list,
    "tag": basic_str,
}

if __name__ == '__main__':

    for child in root:
        OBJECT = {"name": child.attrib["name"]}

        for c in child:
            if c.tag == "value":
                OBJECT.setdefault("tiers", [])
                OBJECT["tiers"].append(int(c.attrib["name"].strip("Tier")))
            else:
                conv_func = CONVERT.get(c.tag)
                if conv_func:
                    k, v = conv_func(c)
                    if not OBJECT.get(k):
                        OBJECT[k] = v
                    else:
                        # assume it's a list
                        OBJECT[k].extend(v)
                        
        data.append(OBJECT)

    import json
    with open("data.json", "w") as f:
        json.dump(data, f)
