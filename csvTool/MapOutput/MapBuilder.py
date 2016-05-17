
import os # for file picker
import sys
import PySide
import csv

from PySide import QtGui
from PySide import QtCore






class MapBuilder(QtGui.QWidget):



    def __init__(self):
        super(MapBuilder, self).__init__()# 
        self.mydir = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.outputDir = self.mydir+"//MapOutput"
        
        self.OpenFile = None
        
        self.UIinit()#do the ui
        
    def SetFileToOpen(self):
        filetest = PySide.QtGui.QFileDialog.getOpenFileName(self, 'Pick File', os.path.expanduser(r"~\Desktop"),"*.csv" )
        print(filetest)
        if(filetest[0]):
            self.OpenFile = filetest[0]
            self.filePathGui.setText(filetest[0])
            
    def SetOutputDir(self):
        filetest = PySide.QtGui.QFileDialog.getExistingDirectory(self, 'output File', os.path.expanduser(r"~\Desktop") )
        print(filetest)
        if(filetest[0]):
            self.outputDir = filetest[0] 
            self.exportPathGui.setText(filetest)
            
    def UIinit(self):
        self.setGeometry(500,400,600,600)
        self.setWindowTitle("MapBuilder Tool")
        
 #filepath 

        #Maybe add filepath picker button
        self.filePathLabel = QtGui.QLabel("File Path:", self)
        self.filePathLabel.move(10, 20)
        self.filePathLabel.show()
        # maybe add a file picker button?
        self.filePathGui = QtGui.QLineEdit(os.path.expanduser(r"~\Desktop"), self)#"C:\\Users\\TommyHanusa\\Desktop\\LADCG Data Feedback i.csv"
        self.filePathGui.resize (375, 20)
        self.filePathGui.move(150, 20)
        self.filePathGui.show()
        #file picker
        self.button = QtGui.QPushButton(" ", self)#should check for confirmation of destructive action!
        self.button.clicked.connect(self.SetFileToOpen)
        self.button.resize (20, 20)
        self.button.move(525,20)
        self.button.show()
        
        #export Path
        self.filePathLabel = QtGui.QLabel("Export Path:", self)
        self.filePathLabel.move(10, 60)
        self.filePathLabel.show()
        # maybe add exportPath picker button?
        self.exportPathGui = QtGui.QLineEdit( os.path.expanduser(r"~\Desktop")+r"\MapOutput", self)#
        self.exportPathGui.resize (375, 20)
        self.exportPathGui.move(150, 60)
        self.exportPathGui.show()
        #
        self.button = QtGui.QPushButton(" ", self)#should check for confirmation of destructive action!
        self.button.clicked.connect(self.SetOutputDir)
        self.button.resize (20, 20)
        self.button.move(525,60)
        self.button.show()
          
        self.button = QtGui.QPushButton("build!", self)#should check for confirmation of destructive action!
        self.button.clicked.connect(self.BuildMapsWrapper)
        self.button.move(200,200)
        self.button.show()
        
        self.show()
    def BuildMapsWrapper(self):
        self.BuildMaps(self.filePathGui.text(), self.exportPathGui.text() )
        
    def BuildMaps(self, filepath, exportPath):
        print("buildMaps")
        with open(filepath)as csvfile: #'C:\\Users\\TommyHanusa\\Desktop\\LADCG Data Feedback i.csv'
            readCSV = csv.DictReader(csvfile, delimiter=',')# create dict reader
            
            for line in readCSV:
                ulat = line["UserLat"]
                ulong = line["UserLong"]
                
                print(ulat)
                print(ulong)
                print(ulat+ulong)
                
                north = line["UserBBNELat"]
                south = line["UserBBSWLat"]
                east = line["UserBBNELong"]
                west = line["UserBBSWLong"]
                
                print(north)
                print(south)
                #print(north-south)
                
                filename = line["HitID"]
                
                html = self.OutputHtml(ulat, ulong, north, south, east, west)
                
                with open(exportPath+r"/"+filename+r".html", 'w') as f:
                    f.write(html)
                    
                
        pass

    def OutputHtml(self, uLat, uLong, north, south, east, west):
        temp1 = ("""<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Rectangles</title>
    <style>
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #map {
        height: 100%;
      }
    </style>
    <script>

      // This example adds a black/grey rectangle to a map.

      function initMap() {
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 11,
          center: {lat: """)
        
        temp1 += str((float(south)+float(north))/2 )
        temp1 += (""", lng: """)
        temp1 += str((float(west)+float(east))/2 )
        temp1 += ("""},
          mapTypeId: google.maps.MapTypeId.TERRAIN
        });

        var rectangle = new google.maps.Rectangle({
          strokeColor: '#000000',
          strokeOpacity: 0.8,
          strokeWeight: 2,
          fillColor: '#000000',
          fillOpacity: 0.35,
          map: map,
          bounds: {
            north: """)
        temp1 += str(north)
        temp1 += (""",
            south: """)
        temp1 += str(south)
        temp1 += (""",
            east: """)
        temp1 += str(east)
        temp1 += (""",
            west: """)
        temp1 += str(west)
        temp1 += ("""
          }
        });
        var image = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
        var beachMarker = new google.maps.Marker({
          position: {lat: """)
        temp1 += str(uLat)
        temp1 += (""", lng: """)
        temp1 += str(uLong)
        temp1 += ("""},
          map: map,
          icon: image
        });
      }
    </script>
  </head>
  <body>
    <div id="map"></div>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAb8lAaQ6-41ADGEXHJ-MG2cpXnFweCaRU&callback=initMap">
    </script>
  </body>
</html> """)

        print(temp1)
        
        return temp1


# does the main work of the script
def main():
    app = QtGui.QApplication(sys.argv)
    tool = MapBuilder()
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
    main()















