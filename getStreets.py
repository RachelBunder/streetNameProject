import xml.sax as sx
import csv


class osmHandler(sx.ContentHandler):
    def __init__(self):
        self.inNode = False
        self.street = False


        self.name = None
        self.uid = None
        self.type = None

        self.streetFile = open('streetDataRaw.csv', 'w', newline = '')
        self.writer = csv.writer(self.streetFile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    def startElement(self, name, atrs):
        self.currentTag = name

        #If something that could be a street
        if name == 'way':
            self.name = None
            self.uid = None
            self.type = None
            self.inNode = True
            try:
                self.uid = atrs["uid"]
            except KeyError:
                return
        elif self.inNode and name == "tag":
            #I don't actually need the residential thing. Just anything labeled as a highway is what I want.
            try:
                if atrs['k'] == "highway":
                    self.street = True
                    self.type = atrs['v']
                elif atrs['k'] == "name":
                    self.name = atrs['v']
                    print(self.name)
            except UnicodeEncodeError:
                print("Unicode error")



    def endElement(self, name):
        if name == 'way':
            if self.street == True:
                self.writer.writerow([self.uid, self.name, self.type])
                self.street = False
            self.inNode = False


fileName = "AustraliaData.osm"

parser = sx.make_parser()

xml = osmHandler()

sx.parse(open(fileName, "r"), xml)

### Read back the csv file as a dataframe so I can clear up the data. Then clean it up later matching uid stuff

# parser.parse(open(fileName, 'r'))

# I want to be looking at the name tag k='Highway'. Not all of these though. Pedestrian refers to main pedestrian throughfairs
# like martin place. Do I want that or not? tag k="highway" v="residential"

# Perhaps start with residential streets and see what that gets me. Want to know what the most common street type is (st, road,ave) and
# what the most common name is. Then look at intersections of the
#
# <way id="290121126" version="1" timestamp="2014-06-28T06:59:15Z" changeset="23237855" uid="12434" user="nm7s9">
# 	<nd ref="2936523246"/>
# 	<nd ref="2936523239"/>
# 	<tag k="highway" v="residential"/>
# 	<tag k="maxspeed" v="50"/>
# 	<tag k="name" v="Redshaw Street"/>
# 	<tag k="source" v="survey"/>
# </way>
