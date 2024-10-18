from interface import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
import os
from xml.dom.minidom import parse
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkVolumeProperty
)
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction




class vtk_parameter(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(vtk_parameter, self).__init__(parent)
        self.setupUi(self)



    # 修改窗口5的三维重建参数
    def readXML(self):

        cur_dir = os.path.dirname(os.path.abspath(__file__))
        domtree = parse(os.path.join(cur_dir, "parameter/preset.xml"))
        data = domtree.documentElement
        propertys = data.getElementsByTagName('VolumeProperty')
        for pro in propertys:
            name = pro.getAttribute('name')
            go = pro.getAttribute('gradientOpacity')
            global so
            so = pro.getAttribute('scalarOpacity')
            ctrans = pro.getAttribute('colorTransfer')
            vtkpro = self.buildProperty(go, so, ctrans)
            self.vtkpros[name] = vtkpro
            self.comboBox.addItem(name)

    def buildProperty(self, go, so, ctrans):

        vtkcoltrans = vtkColorTransferFunction()
        data = ctrans.split()
        data = [float(x) for x in data]
        for i in range(int(data[0] / 4)):
            base = 1 + i * 4

            vtkcoltrans.AddRGBPoint(data[base], data[base + 1], data[base + 2], data[base + 3])

        vtkgo = vtkPiecewiseFunction()
        data = go.split()
        data = [float(x) for x in data]
        for i in range(int(data[0] / 2)):
            base = 1 + i * 2
            vtkgo.AddPoint(data[base], data[base + 1])

        vtkso = vtkPiecewiseFunction()
        data = so.split()
        data = [float(x) for x in data]
        for i in range(int(data[0] / 2)):
            base = 1 + i * 2
            vtkso.AddPoint(data[base], data[base + 1])

        vtkpro = vtkVolumeProperty()
        vtkpro.SetColor(vtkcoltrans)
        vtkpro.SetScalarOpacity(vtkso)
        # vtkpro.SetGradientOpacity(vtkgo)
        vtkpro.SetInterpolationTypeToLinear()
        vtkpro.ShadeOn()
        vtkpro.SetAmbient(0.4)
        vtkpro.SetDiffuse(0.6)
        vtkpro.SetSpecular(0.2)
        return vtkpro


    def changeBtn(self):
        curVol = self.RenList.currentItem()
        if not curVol:
            curVol = self.RenList.itemAt(0, 0)
        curVol = curVol.text()
        if curVol in self.volumes.keys():
            self.volumes[curVol].SetProperty(self.vtkpros[self.comboBox.currentText()])
        # self.widget_5.Initialize()
        self.widget_5.Render()