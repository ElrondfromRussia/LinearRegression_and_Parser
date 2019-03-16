import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import design
import numpy as np
import pandas as pd
import pyqtgraph as pg
import statsmodels.api as sm
import patsy as pt
import sklearn.linear_model as lm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

class MyApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):       
        super().__init__()
        self.setupUi(self)
        self.btn_go.clicked.connect(self.gogo)
        self.works = 0
        self.view1  = pg.PlotWidget()
        self.vl1.addWidget(self.view1)
        self.view2  = pg.PlotWidget()
        self.vl2.addWidget(self.view2)
        self.view3  = pg.PlotWidget()
        self.vl3.addWidget(self.view3)

    def gogo(self):
        self.view1.clear()
        self.view2.clear()
        self.view3.clear()
        self.statusbar.showMessage("Building model...")
        self.sphere = self.cb_obl.currentIndex()
        self.obrazov = self.cb_obr.currentIndex()
        self.opit = self.cb_opit.value()*12
        self.oldness = self.sb_old.value()
        self.build_model()
        self.statusbar.showMessage("Finished")
        
    def build_model(self):
        try:
            if self.sphere == 0:
                df = pd.DataFrame.from_csv("ExpertDoctors.csv")
            else:
                if self.sphere == 1:
                    df = pd.DataFrame.from_csv("Drivers.csv")
                else:
                    if self.sphere == 2:
                        df = pd.DataFrame.from_csv("Tourizm.csv")
                    else:
                        df = pd.DataFrame.from_csv("ITschnimi.csv")

            x = df.iloc[:,:-1]
            y = df.iloc[:, -1]
            x_ = sm.add_constant(x)
            smm = sm.OLS(y, x_)
            res = smm.fit()        

            pred_y1 = []
            pred_y2 = []
            pred_y3 = []
            x1 = np.array(x["#age"])
            x2 = np.array(x["#opit"])
            x3 = np.array(x["#obrazovan"])
        
            for i in range(len(y)):
                pred_y1.append(res.params[0] + res.params[1]*x1[i]+ res.params[2]*self.opit + res.params[3]*self.obrazov)
                pred_y2.append(res.params[0]+ res.params[1]*self.oldness + res.params[2]*x2[i] + res.params[3]*self.obrazov)
                pred_y3.append(res.params[0] + res.params[1]*self.oldness+ res.params[2]*self.opit + res.params[3]*x3[i])
        
            pw1 = pg.PlotCurveItem(x = x1, y = pred_y1, pen=pg.mkPen('b', width=2)) 
            s1 = pg.ScatterPlotItem(x["#age"],y, pen='r')
            self.view1.addItem(s1)
            self.view1.addItem(pw1)
            self.view1.replot()
            self.view1.setTitle('Заработная плата - Возраст')
            self.view1.setLabel("left", text="ЗП, руб")
            self.view1.setLabel("bottom", text="Возраст, лет")
            
            pw2 = pg.PlotCurveItem(x = x2, y = pred_y2, pen=pg.mkPen('#000', width=2)) 
            s2 = pg.ScatterPlotItem(x["#opit"],y, pen='g')
            self.view2.addItem(s2)
            self.view2.addItem(pw2)
            self.view2.replot()
            self.view2.setTitle('Заработная плата - Опыт')
            self.view2.setLabel("left", text="ЗП, руб")
            self.view2.setLabel("bottom", text="Опыт, мес")
        
            pw3 = pg.PlotCurveItem(x = x3, y = pred_y3, pen=pg.mkPen('r', width=2))
            s3 = pg.ScatterPlotItem(x["#obrazovan"],y, pen="#ccc")
            self.view3.addItem(s3)
            self.view3.addItem(pw3)
            self.view3.replot()
            self.view3.setTitle('Заработная плата - Образование')
            self.view3.setLabel("left", text="ЗП, руб")
            self.view3.setLabel("bottom", text="Образование, 0/1/2")

            res_string = "<hr><h4>Матрица корреляции</h4>"
            res_string += "<pre>" + str(df.corr()) + "</pre>"
            res_string += "<hr><h4>Параметры модели</h4>"
            res_string += "<pre>" + str(res.params ) + "</pre>"
            res_string += "<hr><h4>Средняя ЗП</h4>"
            Res_zp = res.params[0] + res.params[1]*self.oldness + res.params[2]*self.opit + res.params[3]*self.obrazov
            res_string += "<pre>" + str(Res_zp) + "</pre>"
            res_string += "<hr><h4>Статистика по параметрам</h4>"
            res_string += "<h5>Мин и Макс</h5>"
            res_string += "#age: <b>min</b>=" + str(min(x["#age"])) + " and <b>max</b>=" + str(max(x["#age"]))
            res_string += "<br>#opit: <b>min</b>=" + str(min(x["#opit"])/12.0) + " years and <b>max</b>=" + str(max(x["#opit"])/12.0) + " years"
            res_string += "<br>#obrazovan: <b>min</b>=" + str(min(x["#obrazovan"])) + " and <b>max</b>=" + str(max(x["#obrazovan"]))
            res_string += "<br>#zp: <b>min</b>=" + str(min(y)) + " and <b>max</b>=" + str(max(y))
            res_string += "<h5>Выборочное среднее</h5>" 
            res_string += "#age: " + str(np.mean(x["#age"]))
            res_string += "<br>#opit: " + str(np.mean(x["#opit"])/12) + " years"
            res_string += "<br>#obrazovan: "+ str(np.mean(x["#obrazovan"]))
            res_string += "<br>#zp: "+ str(np.mean(y))

            self.TXT.setHtml(res_string)
        except Exception:
            print("No data!")
            self.statusbar.showMessage("No data!")

def main():
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()
    
if __name__ == '__main__':
    main()
