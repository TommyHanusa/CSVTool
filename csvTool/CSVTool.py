import csv
import math
    
    
def GetJudgeID(line):
    return line["JudgeID"]
    
    
def processFile(filepath, exportpath, UniqueQueryIdentifier, JudgmentIdentifierKey, dialog):#'process file (3)' button
    #functionality is here    
    with open(filepath)as csvfile: #'C:\\Users\\TommyHanusa\\Desktop\\LADCG Data Feedback i.csv'

        readCSV = csv.DictReader(csvfile, delimiter=',')# create dict reader
        
        
        with open(exportpath, 'w') as f:  # 'C:\\Users\\TommyHanusa\\Desktop\\output.csv'
                
            rowlist = []
            dialog.clear()#clear dialog box gui
            
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
                                    #w.writerow(line1)
                                    #w.writerow(line2)
                                    #w.writerow(line3)
                                    rowlist.append(line1)
                                    rowlist.append(line2)
                                    rowlist.append(line3)
                                    matches +=1

                                   
            if len(rowlist) > 0:
                dialog.append(repr(list(readCSV.fieldnames )))
                
            for i in range(len(rowlist)):
                temp = []
                for j in range(len(readCSV.fieldnames)):
                    temp.append(rowlist[i][readCSV.fieldnames[j]])#access dict element by key in order
                dialog.append(repr(temp))
                w.writerow( rowlist[i])
                
            """   #dicts are hash tables
            if len(rowlist) > 0:
                dialog.append(repr(list(rowlist[0].keys() )))
            
            for i in range(len(rowlist)):
               print(rowlist[i])
               dialog.append(repr(list(rowlist[i].values() )))
               w.writerow( rowlist[i])
               """
               

               
               
def processFile2(filepath, exportpath, UniqueQueryIdentifier, JudgmentIdentifierKey, dialog):#'process file (2)' button
    #functionality is here    
    with open(filepath)as csvfile: #'C:\\Users\\TommyHanusa\\Desktop\\LADCG Data Feedback i.csv'

        readCSV = csv.DictReader(csvfile, delimiter=',')# create dict reader
        
        
        with open(exportpath, 'w') as f:  # 'C:\\Users\\TommyHanusa\\Desktop\\output.csv'
                
            matches = 0
            disagreement = 0
            rowlist = []
            judges = None
            judgesHitCount = None
            lines = 0 # for population
            
            dialog.clear()#clear dialog box gui
            
            w = csv.DictWriter(f, readCSV.fieldnames ,lineterminator='\n')#readCSV.fieldnames 
            w.writeheader()
            
            # initialize lines for determining if 3 hits are the same
            line1 = None
            line2 = None
            
            
            for line in readCSV:
            
                lines+=1 # count every line
                # shift lines by one
                line2 = line1
                line1 = line
                
                if line1 and line2:# only start once we have loaded up atleast 2 lines  
                    if line1[UniqueQueryIdentifier] == line2[UniqueQueryIdentifier]: # same identifier
                        matches +=1
                        
                        if(not judgesHitCount):# intiialize judges
                            judgesHitCount = {GetJudgeID(line1): 1}
                            judgesHitCount.update({GetJudgeID(line2): 1})
                        else:
                            #update line 1 judge
                            id = GetJudgeID(line1)
                            if id in judgesHitCount:
                                judgesHitCount.update({id: judgesHitCount[id]+1})
                            else:
                                 judgesHitCount.update({GetJudgeID(line1): 1})#add new judge
                            # update line 2 judge
                            id = GetJudgeID(line2)
                            if id in judgesHitCount:
                                judgesHitCount.update({id: judgesHitCount[id]+1})
                            else:
                                judgesHitCount.update({GetJudgeID(line2): 1})#add new judge
                                
                        #DISAGREEMENT!
                        if not (line1[JudgmentIdentifierKey] == line2[JudgmentIdentifierKey]): #different value
                                    #w.writerow(line1)
                                    #w.writerow(line2)
                                    rowlist.append(line1)
                                    rowlist.append(line2)
                                    disagreement +=1
                                    
                                    if(not judges):# intiialize judges
                                        judges = {GetJudgeID(line1): 1}
                                        judges.update({GetJudgeID(line2): 1})
                                    else:
                                        #update line 1 judge
                                        id = GetJudgeID(line1)
                                        if id in judges:
                                            judges.update({id: judges[id]+1})
                                        else:
                                            judges.update({GetJudgeID(line1): 1})#add new judge
                                            
                                        # update line 2 judge
                                        id = GetJudgeID(line2)
                                        if id in judges:
                                            judges.update({id: judges[id]+1})
                                        else:
                                            judges.update({GetJudgeID(line2): 1})#add new judge
                                    
                                    
            if len(rowlist) > 0:
                dialog.append(repr(list(readCSV.fieldnames )))
                
            for i in range(len(rowlist)):
                temp = []
                for j in range(len(readCSV.fieldnames)):
                    temp.append(rowlist[i][readCSV.fieldnames[j]])#access dict element by key in order
                dialog.append(repr(temp))
                w.writerow( rowlist[i])
                
            dialog.append("")# line break
            #print judge disagreements
            for judge in judges.keys():
                dialog.append("judge # "+repr(judge)+" disagreements = "+repr(judges[judge]))
                dialog.append("hits = "+repr(judgesHitCount[judge]))
                
            dialog.append("")# line break
            dialog.append("Matches = "+repr(matches))
            dialog.append("Disagreement = "+repr(disagreement))
            dialog.append("ratio = "+repr(1.0-(disagreement/matches)) )
            
            sampleMean = (disagreement/matches)
            print("lines = "+repr(lines))
            print("STD=", math.sqrt(sampleMean*(abs(lines - sampleMean)**2)) )
            print("STD2=", math.sqrt(sampleMean*(abs(1.0 - sampleMean)**2)) )
            #conInt = Math.sqrt(zValC * (perc / 100) * (1 - perc / 100) / ss * pf) * 100 
            zValC=3.8416
            perc = 1.0-(disagreement/matches)
            ss = matches
            pop = lines
            pf = (pop - ss) / (pop - 1)
            
            temp = math.sqrt(zValC * (perc / 100) * (1 - perc / 100) / ss * pf) * 100 
            temp = (temp-pf)*100
            temp = pf+temp/100
            print ("std3 = "+repr(temp))
            
            """
            #mathmagic
            matches#sample size
            disagreement#
            
            alpha = 1 - (95 / 100)# 95% confidence
            p = 1 - alpha/2
            

            sampleMean = (disagreement/matches)
            sampleVariancetemp = disagreement(0-sampleMean)^2 + 1.0-(disagreement/matches)) ^2
            sampleDeviation = sqrt(sampleVariancetemp/(lines-1))
            
            critVal = 1.96# 95% confidence level
            standardError = 0 # SD/sqrt(sampleSize)
            """
            ####
            """ #dicts are hash tables
            if len(rowlist) > 0:
                dialog.append(repr(list(rowlist[0].keys() )))
            
            for i in range(len(rowlist)):
               print(rowlist[i])
               dialog.append(repr(list(rowlist[i].values() )))
               w.writerow( rowlist[i]) """
                
#GUI
import os # for file picker
import sys
import PySide

from PySide import QtGui
from PySide import QtCore


# Create the application object
class CSVTool(QtGui.QWidget):


    def __init__(self):
        super(CSVTool, self).__init__()# 
        
        #initialize filepath to the location of the exe
        self.filepathTemp1 = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.filepathTemp2 = os.path.abspath(os.path.dirname(sys.argv[0]))
        
        self.UIinit()
        
        
    def SetFileToOpen(self):
        filetest = PySide.QtGui.QFileDialog.getOpenFileName(self, 'Pick File', os.path.expanduser(r"~\Desktop"),"*.csv" )
        print(filetest)
        if(filetest[0]):
            self.filePathGui.setText(filetest[0])
            self.SetComboBoxOptions(filetest[0])
        
    def SetComboBoxOptions(self, filePath):#needs to be done on new file
        # set combo box options
        with open(filePath)as csvfile:
            readCSV = csv.DictReader(csvfile, delimiter=',')
            temp =  readCSV.fieldnames
            print(temp)
            self.queryGui.addItems(temp)                
            self.judgementGui.addItems(temp)

        pass
    def SetFileToExport(self):
        filetest = PySide.QtGui.QFileDialog.getOpenFileName(self, 'Pick Output File', os.path.expanduser(r"~\Desktop"),"*.csv" )
        print(filetest)
        if(filetest[0]):
            self.exportPathGui.setText(filetest[0])
        pass
        
    def UIinit(self):
        self.setGeometry(500,400,600,600)
        self.setWindowTitle("CSV Tool")
        
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
        self.exportPathGui = QtGui.QLineEdit( os.path.expanduser(r"~\Desktop")+r"\output.csv", self)#
        self.exportPathGui.resize (375, 20)
        self.exportPathGui.move(150, 60)
        self.exportPathGui.show()
        #
        self.button = QtGui.QPushButton(" ", self)#should check for confirmation of destructive action!
        self.button.clicked.connect(self.SetFileToExport)
        self.button.resize (20, 20)
        self.button.move(525,60)
        self.button.show()
        
        #Unique Query Identifier string
        self.filePathLabel = QtGui.QLabel("Unique Query Identifier:", self)
        self.filePathLabel.move(10, 100)
        self.filePathLabel.show()
        
        self.queryGui = QtGui.QComboBox(self) #QtGui.QLineEdit("HitGroupID", self)
        self.queryGui.resize (375, 20)
        self.queryGui.move(150, 100)
        self.queryGui.show()
        
        #Judgement Identifier key string
        self.filePathLabel = QtGui.QLabel("Judgement Identifier:", self)
        self.filePathLabel.move(10, 140)
        self.filePathLabel.show()
        
        self.judgementGui = QtGui.QComboBox(self) #QtGui.QLineEdit("JudgmentDataIntName", self)
        self.judgementGui.resize (375, 20)
        self.judgementGui.move(150, 140)
        self.judgementGui.show()
        
        #button to do the work
        
        self.button = QtGui.QPushButton("Process File(3)", self)#should check for confirmation of destructive action!
        self.button.clicked.connect(self.processWrapper)
        self.button.move(10,200)
        self.button.show()
        
        self.button = QtGui.QPushButton("Process File(2)", self)#should check for confirmation of destructive action!
        self.button.clicked.connect(self.processWrapper2)
        self.button.move(200,200)
        self.button.show()
        
        self.TextDialofBox = QtGui.QTextEdit(self)
        self.TextDialofBox.move(10,250)
        self.TextDialofBox.resize (500, 300)
        self.TextDialofBox.setReadOnly(True)
        self.TextDialofBox.setLineWrapMode(QtGui.QTextEdit.NoWrap)#remove line wrapping
        
        self.TextDialofBox.show()
        
        self.show()
        
        #self.SetComboBoxOptions(self.filePathGui.text())
        
        
    def processWrapper(self):
        print("process")
        processFile(self.filePathGui.text(), self.exportPathGui.text(), self.queryGui.currentText(), self.judgementGui.currentText(),self.TextDialofBox )
        
    def processWrapper2(self):
        print("process")
        processFile2(self.filePathGui.text(), self.exportPathGui.text(), self.queryGui.currentText(), self.judgementGui.currentText(),self.TextDialofBox )
        

#file_pick()
#file_save()
# does the main work of the script
def main():
    app = QtGui.QApplication(sys.argv)
    tool = CSVTool()
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
    main()
    


