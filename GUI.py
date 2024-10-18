from operation import Operate
from initialization import Initialization
from vtk_para import vtk_parameter
from update import Update
from interface import Ui_MainWindow
import threading
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderer,
    vtkVolumeProperty
)
import coord


#
#
# index_sagittal = Initialization.index_sagittal
# index_axial = Initialization.index_axial
# index_coronal = Initialization.index_coronal

from PyQt5.QtCore import  QEvent, Qt


import vtk


a, b = 0, False



class My_MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(My_MainWindow, self).__init__(parent)
        self.setupUi(self)


        #创建三维
        self.reader = vtk.vtkDICOMImageReader()
        self.vtkpros = {}
        self.volumes = {}
        self.volume_property = vtkVolumeProperty()
        self.volume_color = vtkColorTransferFunction()
        self.volume_scalar_opacity = vtkPiecewiseFunction()
        self.volume_gradient_opacity = vtkPiecewiseFunction()
        self.tan_zhenSource = vtk.vtkLineSource()
        self.initialization = Initialization()

        # 按钮跳转到指定函数
        self.pushButton_3.clicked.connect(self.call_back_action_open_dir)   #选取文件夹及初始化
        self.pushButton.clicked.connect(self.changeBtn)
        self.pushButton_13.clicked.connect(self.bingzao_1)
        self.pushButton_10.clicked.connect(self.jinzhendian)
        self.pushButton_12.clicked.connect(self.guangbiao_12)
        self.pushButton_11.clicked.connect(self.remove)
        # self.pushButton_17.clicked.connect(self.guangbiao_12)
        # self.pushButton_18.clicked.connect(self.bingzao2)
        # self.pushButton_19.clicked.connect(self.jindaodian2)
        # self.pushButton_20.clicked.connect(self.remove2)


        self.actor_1 = None
        self.actor_2 = None
        self.actor_3 = None








        # 每隔15毫秒更新一下线段位置
        self.widget_5.AddObserver('TimerEvent', self.update_line)
        self.widget_5.CreateRepeatingTimer(20)








        self.reslice_1 = vtk.vtkImageReslice()
        self.reslice_2 = vtk.vtkImageReslice()
        self.reslice_3 = vtk.vtkImageReslice()



        # 定义路径直线
        self.previous_line_actor = None  # 用于保存上一条直线的actor引用

        #更改主窗口显示的参数
        self.readXML()
        self.volume_property = self.vtkpros["CT-AAA"]

        self.volume = vtk.vtkVolume()  #创建演员
        # Create callbacks for slicing the image
        self.actions = {}
        self.actions["Slicing"] = 0
        self.center = [0,0,0]

        self.info = {
            "name": "无",
            "id": "无",
            "sex": "无",
            "date": "无",
            "age": "无"
        }

        self.pointdata = [[0, 0, 0], [0, 0, 0]]
        self.axial = vtk.vtkMatrix4x4()
        self.coronal = vtk.vtkMatrix4x4()
        self.sagittal = vtk.vtkMatrix4x4()





        # 创建交互
        interactorStyle = vtk.vtkInteractorStyleImage()
        interactorStyle2 = vtk.vtkInteractorStyleImage()
        interactorStyle3 = vtk.vtkInteractorStyleImage()

        self.widget_1.SetInteractorStyle(interactorStyle)
        self.widget_2.SetInteractorStyle(interactorStyle2)
        self.widget_3.SetInteractorStyle(interactorStyle3)


        interactorStyle.AddObserver("MouseMoveEvent", self.MouseMoveCallback)
        interactorStyle2.AddObserver("MouseMoveEvent", self.MouseMoveCallback)
        interactorStyle3.AddObserver("MouseMoveEvent", self.MouseMoveCallback)



        # 创建新的交互方式
        self.widget_1.setObjectName("widget_1")
        self.widget_2.setObjectName("widget_2")
        self.widget_3.setObjectName("widget_3")

        self.widget_1.installEventFilter(self)
        self.widget_2.installEventFilter(self)
        self.widget_3.installEventFilter(self)



        # 调试阶段，现在直接启动打开文件夹按钮
        self.call_back_action_open_dir()


    def remove(self):
        self.renderer.RemoveActor(self.actor1)
        self.renderer2.RemoveActor(self.actor2)
        self.renderer3.RemoveActor(self.actor3)



    def guangbiao_12(self):
        Operate.guangbiao_12(self)
    def bingzao_1(self):
        Operate.bingzao_1(self)
    def jinzhendian(self):
        Operate.jinzhendian(self)




    # mpr操作
    def eventFilter(self, obj, event):
        Operate.eventFilter(self, obj, event)
        return super().eventFilter(obj, event)
    #
    def MouseMoveCallback(self, obj, event):
        Operate.MouseMoveCallback(self, obj, event)

    def ButtonCallback(self,obj, event):
        Operate.ButtonCallback(self, obj, event)






    # 修改窗口5的三维重建参数
    def readXML(self):
        vtk_parameter.readXML(self)
    def buildProperty(self, go, so, ctrans):
        vtkpro = vtk_parameter.buildProperty(self, go, so, ctrans)
        return vtkpro
    def changeBtn(self):
        vtk_parameter.changeBtn(self)





    def line_callback(self, obj, event):
        Operate.line_callback(self, obj, event)

    def line_callback_end(self, obj, event):
        Operate.line_callback_end(self, obj, event)


    def right_button_callback(self, obj, event):
        Operate.right_button_callback(self, obj, event)


    def update_line(self, obj,event):       # 更新窗口5的线段位置
        Update.update_line(self, obj,event)



    def call_back_action_open_dir(self):
        Initialization.call_back_action_open_dir(self)







    #取消在关闭时的警告信息
    def closeEvent(self, event):
        self.widget_5.Finalize()
        self.widget_7.Finalize()
        self.widget_1.Finalize()
        self.widget_2.Finalize()
        self.widget_3.Finalize()
        # self.widget_4.Finalize()


if __name__ == "__main__":
    added_thred = threading.Thread(target=coord.load_dll)
    added_thred.start()
    added_thread2 = threading.Thread(target=coord.process_output)
    added_thread2.start()

    app = QApplication([])
    widget = My_MainWindow()
    widget.showMaximized()
    sys.exit(app.exec_())
