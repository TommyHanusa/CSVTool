import csv
    
    
def processFile(filepath, exportpath, UniqueQueryIdentifier, JudgmentIdentifierKey):
    #functionality is here    
    with open(filepath)as csvfile: #'C:\\Users\\TommyHanusa\\Desktop\\LADCG Data Feedback i.csv'

        readCSV = csv.DictReader(csvfile, delimiter=',')# create dict reader
        
        
        with open(exportpath, 'w') as f:  # 'C:\\Users\\TommyHanusa\\Desktop\\output.csv'
                
        
            w = csv.DictWriter(f, readCSV.fieldnames ,lineterminator='\n')#readCSV.fieldnames 
            w.writeheader()
            
            # initialize lines for determining if 3 hits are the same
            line1 = None
            line2 = None
            line3 = None
            
            #old
            #UniqueQueryIdentifier = 'EntityGuid'#'HitGroupID'# what column is compared as a unique query?
            #JudgmentIdentifierKey = 'JudgmentDataIntName'# what column is compared as answers
           
            
            
            for line in readCSV:
                # shift lines by one
                line3 = line2
                line2 = line1
                line1 = line
                
                if line1 and line2 and line3:# only start once we have loaded up atleast 3 lines  
                    if line1[UniqueQueryIdentifier] == line2[UniqueQueryIdentifier] == line3[UniqueQueryIdentifier]:
                        if not (line1[JudgmentIdentifierKey]== line2[JudgmentIdentifierKey]): 
                            if not (line2[JudgmentIdentifierKey]== line3[JudgmentIdentifierKey]):
                                if not (line3[JudgmentIdentifierKey]== line1[JudgmentIdentifierKey]):
                                    w.writerow(line1)
                                    w.writerow(line2)
                                    w.writerow(line3)
                
                
#GUI
import sys
import PySide

from PySide import QtGui
from PySide import QtCore


# Create the application object
class CSVTool(QtGui.QWidget):


    def __init__(self):
        super(CSVTool, self).__init__()# 
        
        self.UIinit()
        
        
    def UIinit(self):
        self.setGeometry(500,400,550,300)
        self.setWindowTitle("CSV Tool")
        
        #filepath 
        #Maybe add filepath picker button
        self.filePathLabel = QtGui.QLabel("File Path:", self)
        self.filePathLabel.move(10, 20)
        self.filePathLabel.show()
        # maybe add a file picker button?
        self.filePathGui = QtGui.QLineEdit("C:\\Users\\TommyHanusa\\Desktop\\LADCG Data Feedback i.csv", self)
        self.filePathGui.resize (375, 20)
        self.filePathGui.move(150, 20)
        self.filePathGui.show()
        
        #export Path
        self.filePathLabel = QtGui.QLabel("Export Path:", self)
        self.filePathLabel.move(10, 60)
        self.filePathLabel.show()
        # maybe add exportPath picker button?
        self.exportPathGui = QtGui.QLineEdit("C:\\Users\\TommyHanusa\\Desktop\\output.csv", self)
        self.exportPathGui.resize (375, 20)
        self.exportPathGui.move(150, 60)
        self.exportPathGui.show()
        
        #Unique Query Identifier string
        self.filePathLabel = QtGui.QLabel("Unique Query Identifier:", self)
        self.filePathLabel.move(10, 100)
        self.filePathLabel.show()
        
        self.queryGui = QtGui.QLineEdit("HitGroupID", self)
        self.queryGui.resize (375, 20)
        self.queryGui.move(150, 100)
        self.queryGui.show()
        
        #Judgement Identifier key string
        self.filePathLabel = QtGui.QLabel("Judgement Identifier:", self)
        self.filePathLabel.move(10, 140)
        self.filePathLabel.show()
        
        self.judgementGui = QtGui.QLineEdit("JudgmentDataIntName", self)
        self.judgementGui.resize (375, 20)
        self.judgementGui.move(150, 140)
        self.judgementGui.show()
        
        #button to do the work
        
        self.button = QtGui.QPushButton("Process File", self)#should check for confirmation of destructive action!
        self.button.clicked.connect(self.processWrapper)
        self.button.move(10,200)
        self.button.show()
        
        self.show()
        
    def processWrapper(self):
        
        processFile(self.filePathGui.text(), self.exportPathGui.text(), self.queryGui.text(), self.judgementGui.text() )
        
# does the main work of the script
def main():
    app = QtGui.QApplication(sys.argv)
    tool = CSVTool()
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
    main()
    


