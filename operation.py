from interface import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QEvent, Qt
from initialization import Initialization
from PyQt5.QtGui import QWheelEvent
import vtk


a, b = 0, False

center_1 = (0, 0, 0)
center_2 = (0, 0, 0)
center_3 = (0, 0, 0)


class Operate(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Operate, self).__init__(parent)
        self.setupUi(self)








    def guangbiao_12(self):
        global center_1, center_2, center_3, point, actors
        center = self.center
        # 创建交点坐标列表
        points = [(center_3[1]-center[1], center[2] - center_2[2]), (center_1[0]-center[0], center_3[1]-center[1]),
                  (center_1[0]-center[0],  center[2] - center_2[2])]

        # 获取渲染器中的演员集合
        actor = self.renderer.GetActors()
        if actor.GetNumberOfItems() > 2:

            for i in range(len(points)):
                point = points[i]
                # 更新水平线
                self.lines[2 * i].SetPoint1(point[0] - center[0], point[1], 1)
                self.lines[2 * i].SetPoint2(point[0] + center[0], point[1], 1)

                # 更新垂直线
                self.lines[2 * i + 1].SetPoint1(point[0], point[1] - center[1], 1)
                self.lines[2 * i + 1].SetPoint2(point[0], point[1] + center[1], 1)

                self.lines[2 * i].Update()
                self.lines[2 * i + 1].Update()

            self.actor_4.SetPosition(center_1[0]-center[0], center_3[1]-center[1], center_2[2] - center[2])

        else:
            self.lines = []
            actors = []
            # 创建六条直线
            for point in points:
                # 创建水平线
                self.horizontalLine = vtk.vtkLineSource()
                self.horizontalLine.SetPoint1(point[0] - center[0], point[1], 1)
                self.horizontalLine.SetPoint2(point[0] + center[0], point[1], 1)
                # 创建垂直线
                self.verticalLine = vtk.vtkLineSource()
                self.verticalLine.SetPoint1(point[0], point[1] - center[1], 1)
                self.verticalLine.SetPoint2(point[0], point[1] + center[1], 1)

                self.lines.append(self.horizontalLine)
                self.lines.append(self.verticalLine)

                # 创建映射器和actor
                horizontalMapper = vtk.vtkPolyDataMapper()
                horizontalMapper.SetInputConnection(self.horizontalLine.GetOutputPort())

                verticalMapper = vtk.vtkPolyDataMapper()
                verticalMapper.SetInputConnection(self.verticalLine.GetOutputPort())

                horizontalActor = vtk.vtkActor()
                horizontalActor.SetMapper(horizontalMapper)

                verticalActor = vtk.vtkActor()
                verticalActor.SetMapper(verticalMapper)

                # 设置线段颜色和粗细
                lineProperty = vtk.vtkProperty()
                lineProperty.SetColor(0, 0, 1)  # 设置为蓝色
                lineProperty.SetLineWidth(0.2)  # 设置线宽

                horizontalActor.SetProperty(lineProperty)
                verticalActor.SetProperty(lineProperty)

                actors.append(horizontalActor)
                actors.append(verticalActor)

            self.renderer.AddActor(actors[0])
            self.renderer.AddActor(actors[1])
            self.renderer2.AddActor(actors[2])
            self.renderer2.AddActor(actors[3])
            self.renderer3.AddActor(actors[4])
            self.renderer3.AddActor(actors[5])

        self.widget_1.Render()
        self.widget_2.Render()
        self.widget_3.Render()
        self.widget_5.Render()








    def createpoint(self):
        global center_1, center_2, center_3
        point = center_1[0] - self.center[0], center_3[1] - self.center[1], center_2[2] - self.center[2]
        sphereSource = vtk.vtkSphereSource()
        # 创建4个小球分别放置在窗口中
        sphereSource.SetCenter(point)  # 设置球体中心位置
        sphereSource.SetRadius(2.5)  # 设置球体半径
        # 创建一个mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphereSource.GetOutputPort())

        # 创建一个actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        sphereSource1 = vtk.vtkSphereSource()
        # 创建4个小球分别放置在窗口中
        point1 = point[1], -point[2], 2
        sphereSource1.SetCenter(point1)  # 设置球体中心位置
        sphereSource1.SetRadius(2.5)  # 设置球体半径
        # 创建一个mapper
        mapper1 = vtk.vtkPolyDataMapper()
        mapper1.SetInputConnection(sphereSource1.GetOutputPort())

        # 创建一个actor
        actor1 = vtk.vtkActor()
        actor1.SetMapper(mapper1)

        sphereSource2 = vtk.vtkSphereSource()
        # 创建4个小球分别放置在窗口中
        point2 = point[0], point[1], 2
        sphereSource2.SetCenter(point2)  # 设置球体中心位置
        sphereSource2.SetRadius(2.5)  # 设置球体半径
        # 创建一个mapper
        mapper2 = vtk.vtkPolyDataMapper()
        mapper2.SetInputConnection(sphereSource2.GetOutputPort())

        # 创建一个actor
        actor2 = vtk.vtkActor()
        actor2.SetMapper(mapper2)

        sphereSource3 = vtk.vtkSphereSource()
        # 创建4个小球分别放置在窗口中
        point3 = point[0], -point[2], 2
        sphereSource3.SetCenter(point3)  # 设置球体中心位置
        sphereSource3.SetRadius(2.5)  # 设置球体半径
        # 创建一个mapper
        mapper3 = vtk.vtkPolyDataMapper()
        mapper3.SetInputConnection(sphereSource3.GetOutputPort())

        # 创建一个actor
        actor3 = vtk.vtkActor()
        actor3.SetMapper(mapper3)

        self.ren.AddActor(actor)
        self.renderer.AddActor(actor1)
        self.renderer2.AddActor(actor2)
        self.renderer3.AddActor(actor3)

        self.widget_5.Render()
        self.widget_1.Render()
        self.widget_2.Render()
        self.widget_3.Render()
        return point





    def update_point(self, point_index, x, y, z):
        self.pointdata[point_index][0] = x
        self.pointdata[point_index][1] = y
        self.pointdata[point_index][2] = z



    def bingzao_1(self):
        point = Operate.createpoint(self)
        x,y,z = point
        #需要记录点的坐标
        Operate.update_point(self, 0, x, y, z)



    def jinzhendian(self):
        point = Operate.createpoint(self)
        x,y,z = point
        #需要记录点的坐标
        Operate.update_point(self, 1, x, y, z)

        # 创建一个点的集合
        points = vtk.vtkPoints()
        for point in self.pointdata:
            points.InsertNextPoint(point)

        # 创建一个直线数据集
        line = vtk.vtkPolyLine()
        line.GetPointIds().SetNumberOfIds(len(self.pointdata))
        for i in range(len(self.pointdata)):
            line.GetPointIds().SetId(i, i)

        lines = vtk.vtkCellArray()
        lines.InsertNextCell(line)

        # 创建一个PolyData对象，并将点和线添加到其中
        polydata = vtk.vtkPolyData()
        polydata.SetPoints(points)
        polydata.SetLines(lines)

        # 创建一个Mapper对象和一个Actor对象，用于渲染直线
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(polydata)

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetLineWidth(0.5)  # 设置线段粗细为0.2

        # 创建一个LineSource对象，并设置起点和终点坐标
        line_source = vtk.vtkLineSource()
        line_source.SetPoint1(self.pointdata[0][1], -self.pointdata[0][2], 2)
        line_source.SetPoint2(self.pointdata[1][1], -self.pointdata[1][2], 2)

        # 创建一个Mapper对象，并将LineSource对象作为输入
        mapper1 = vtk.vtkPolyDataMapper()
        mapper1.SetInputConnection(line_source.GetOutputPort())

        # 创建一个Actor对象，并将Mapper对象作为输入
        self.actor1 = vtk.vtkActor()
        self.actor1.SetMapper(mapper1)
        self.actor1.GetProperty().SetLineWidth(0.5)  # 设置线段粗细为0.2

        # 创建一个LineSource对象，并设置起点和终点坐标
        line_source2 = vtk.vtkLineSource()
        line_source2.SetPoint1(self.pointdata[0][0], self.pointdata[0][1], 2)
        line_source2.SetPoint2(self.pointdata[1][0], self.pointdata[1][1], 2)

        # 创建一个Mapper对象，并将LineSource对象作为输入
        mapper2 = vtk.vtkPolyDataMapper()
        mapper2.SetInputConnection(line_source2.GetOutputPort())

        # 创建一个Actor对象，并将Mapper对象作为输入
        self.actor2 = vtk.vtkActor()
        self.actor2.SetMapper(mapper2)
        self.actor2.GetProperty().SetLineWidth(0.5)  # 设置线段粗细为0.2

        # 创建一个LineSource对象，并设置起点和终点坐标
        line_source3 = vtk.vtkLineSource()
        line_source3.SetPoint1(self.pointdata[0][0], -self.pointdata[0][2], 2)
        line_source3.SetPoint2(self.pointdata[1][0], -self.pointdata[1][2], 2)

        # 创建一个Mapper对象，并将LineSource对象作为输入
        mapper3 = vtk.vtkPolyDataMapper()
        mapper3.SetInputConnection(line_source3.GetOutputPort())

        # 创建一个Actor对象，并将Mapper对象作为输入
        self.actor3 = vtk.vtkActor()
        self.actor3.SetMapper(mapper3)
        self.actor3.GetProperty().SetLineWidth(0.2)  # 设置线段粗细为0.2

        self.renderer.AddActor(self.actor1)
        self.widget_1.Render()

        self.renderer2.AddActor(self.actor2)
        self.widget_2.Render()

        self.renderer3.AddActor(self.actor3)
        self.widget_3.Render()

        self.ren.AddActor(actor)
        self.widget_5.Render()

    def eventFilter(self, obj, event):
        global center_1, center_2, center_3
        center = self.center
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:

            self.actions["Slicing"] = 1

        elif event.type() == QEvent.MouseButtonPress and event.button() == Qt.RightButton:
            self.actions["Slicing"] = 2


        elif event.type() == QEvent.MouseButtonRelease:
            self.actions["Slicing"] = 0

        # 改用双击来更改视图
        elif event.type() == QEvent.MouseButtonDblClick:
            if obj.objectName() == "widget_1":
                picker = vtk.vtkPropPicker()
                picker.Pick(self.widget_1.GetRenderWindow().GetInteractor().GetEventPosition()[0],
                            self.widget_1.GetRenderWindow().GetInteractor().GetEventPosition()[1], 0,
                            self.widget_1.GetRenderWindow().GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer())
                picked = picker.GetPickPosition()
                print('窗口一中点击的坐标：', picked)
                picked = [center_1[0], center[2] - picked[1], picked[0]+center[1]]
                print('得到的三维坐标：', picked)
            elif obj.objectName() == "widget_2":
                picker = vtk.vtkPropPicker()
                picker.Pick(self.widget_2.GetRenderWindow().GetInteractor().GetEventPosition()[0],
                            self.widget_2.GetRenderWindow().GetInteractor().GetEventPosition()[1], 0,
                            self.widget_2.GetRenderWindow().GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer())
                picked = picker.GetPickPosition()
                print('窗口二中点击的坐标：', picked)
                picked = [picked[0]+center[0], center_2[2], picked[1]+center[1]]
                print('得到的三维坐标：', picked)
            elif obj.objectName() == "widget_3":
                picker = vtk.vtkPropPicker()
                picker.Pick(self.widget_3.GetRenderWindow().GetInteractor().GetEventPosition()[0],
                            self.widget_3.GetRenderWindow().GetInteractor().GetEventPosition()[1], 0,
                            self.widget_3.GetRenderWindow().GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer())
                picked = picker.GetPickPosition()
                print('窗口三中点击的坐标：', picked)
                picked = [picked[0]+center[1], center[2] - picked[1], center_3[1]]
                print('得到的三维坐标：', picked)

            list_center_1 = [picked[0], center_1[1], center_1[2]]
            list_center_2 = [center_2[0], center_2[1], picked[1]]
            list_center_3 = [center_3[0], picked[2], center_3[2]]

            Operate.change_slice(self, list_center_1, list_center_2, list_center_3)
            Operate.guangbiao_12(self)


        elif event.type() == QEvent.Wheel:
            # 鼠标滚轮事件处理
            wheel_event = QWheelEvent(event)
            # 获取滚轮滚动的角度
            angle = wheel_event.angleDelta().y() / 8
            print(angle)




    def change_slice(self, list_center_1, list_center_2, list_center_3):
        global center_1, center_2, center_3
        # self.reslice_1.Update()
        # 获取reslice对象的重新采样轴
        matrix = self.reslice_1.GetResliceAxes()
        matrix.SetElement(0, 3, list_center_1[0])
        matrix.SetElement(1, 3, list_center_1[1])
        matrix.SetElement(2, 3, list_center_1[2])
        self.reslice_1.Update()


        matrix_2 = self.reslice_2.GetResliceAxes()

        matrix_2.SetElement(0, 3, list_center_2[0])
        matrix_2.SetElement(1, 3, list_center_2[1])
        matrix_2.SetElement(2, 3, list_center_2[2])

        self.reslice_2.Update()

        matrix_3 = self.reslice_3.GetResliceAxes()
        matrix_3.SetElement(0, 3, list_center_3[0])
        matrix_3.SetElement(1, 3, list_center_3[1])
        matrix_3.SetElement(2, 3, list_center_3[2])
        self.reslice_3.Update()
        # 重新渲染widget_1、widget_2、widget_3以显示更新后的切片位置


        center_1 = matrix.MultiplyPoint((0, 0, 0, 1))
        center_2 = matrix_2.MultiplyPoint((0, 0, 0, 1))
        center_3 = matrix_3.MultiplyPoint((0, 0, 0, 1))

        self.widget_1.Render()
        self.widget_2.Render()
        self.widget_3.Render()

    def line_callback(self, obj, event):

        print("Point 1:", self.line_widget.GetPoint1())
        print("Point 2:", self.line_widget.GetPoint2())

    def line_callback_end(self, caller, event):
        # 获取 vtkLineWidget 的点坐标
        point1 = [0, 0, 0]
        self.line_widget.GetPoint1(point1)
        point2 = [0, 0, 0]
        self.line_widget.GetPoint2(point2)

        # 如果之前有直线被绘制过，先从渲染器中移除
        if self.previous_line_actor is not None:
            self.ren.RemoveActor(self.previous_line_actor)

        # 创建 vtkLineSource 对象
        lineSource = vtk.vtkLineSource()
        lineSource.SetPoint1(point1)
        lineSource.SetPoint2(point2)

        # 创建映射器
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(lineSource.GetOutputPort())

        # 创建 actor
        self.previous_line_actor = vtk.vtkActor()
        self.previous_line_actor.SetMapper(mapper)

        # 设置直线的颜色和宽度（可选）
        self.previous_line_actor.GetProperty().SetColor(1, 1, 1)  # 红色
        self.previous_line_actor.GetProperty().SetLineWidth(2)

        # 添加 actor 到渲染器中
        self.ren.AddActor(self.previous_line_actor)

        self.widget_5.Render()




    def right_button_callback(self, obj, event):
        if self.line_widget.GetEnabled():
            self.line_widget.SetEnabled(False)  # 右键点击时关闭vtkLineWidget的交互
        else:
            self.line_widget.SetEnabled(True)  # 再次右键点击时开启vtkLineWidget的交互









    def MouseMoveCallback(self, obj, event):

        if self.actions["Slicing"] == 1:
            # 获取widget_1上一次鼠标事件的位置
            (lastX, lastY) = self.widget_1.GetLastEventPosition()
            (mouseX, mouseY) = self.widget_1.GetEventPosition()
            # 获取widget_2上一次鼠标事件的位置
            (lastX_2, lastY_2) = self.widget_2.GetLastEventPosition()
            (mouseX_2, mouseY_2) = self.widget_2.GetEventPosition()
            # 获取widget_3上一次鼠标事件的位置
            (lastX_3, lastY_3) = self.widget_3.GetLastEventPosition()
            (mouseX_3, mouseY_3) = self.widget_3.GetEventPosition()

            # 计算鼠标在Y轴上的移动距离
            deltaY = mouseY - lastY
            deltaY_2 = mouseY_2 - lastY_2
            deltaY_3 = mouseY_3 - lastY_3


            global center_1,center_2,center_3


            global sliceSpacing, sliceSpacing_2, sliceSpacing_3

            # 获取切片间距(slice spacing)
            sliceSpacing = self.reslice_1.GetOutput().GetSpacing()[2]
            sliceSpacing_2 = self.reslice_2.GetOutput().GetSpacing()[2]
            sliceSpacing_3 = self.reslice_3.GetOutput().GetSpacing()[2]

            # 更新reslice对象
            self.reslice_1.Update()
            # 获取reslice对象的重新采样轴
            matrix = self.reslice_1.GetResliceAxes()
            # 根据鼠标移动调整图像切片中心点的位置
            center_1 = matrix.MultiplyPoint((0, 0, sliceSpacing * deltaY, 1))

            # 前三列分别表示X、Y和Z方向矢量，第四列为切面坐标系原点
            matrix.SetElement(0, 3, center_1[0])
            matrix.SetElement(1, 3, center_1[1])
            matrix.SetElement(2, 3, center_1[2])

            # 更新reslice_2对象
            self.reslice_2.Update()

            # 获取reslice_2对象的重新采样轴
            matrix_2 = self.reslice_2.GetResliceAxes()
            # 根据鼠标移动调整图像切片中心点的位置
            center_2 = matrix_2.MultiplyPoint((0, 0, sliceSpacing_2 * deltaY_2, 1))
            matrix_2.SetElement(0, 3, center_2[0])
            matrix_2.SetElement(1, 3, center_2[1])
            matrix_2.SetElement(2, 3, center_2[2])

            # 更新reslice_3对象
            self.reslice_3.Update()
            # 获取reslice_3对象的重新采样轴
            matrix_3 = self.reslice_3.GetResliceAxes()

            # 根据鼠标移动调整图像切片中心点的位置
            center_3 = matrix_3.MultiplyPoint((0, 0, sliceSpacing_3 * deltaY_3, 1))
            matrix_3.SetElement(0, 3, center_3[0])
            matrix_3.SetElement(1, 3, center_3[1])
            matrix_3.SetElement(2, 3, center_3[2])

            # 重新渲染widget_1、widget_2、widget_3以显示更新后的切片位置
            self.widget_1.Render()
            self.widget_2.Render()
            self.widget_3.Render()

            Operate.guangbiao_12(self)


        elif self.actions["Slicing"] == 2:

            (lastX1, lastY1) = self.widget_1.GetLastEventPosition()
            (mouseX1, mouseY1) = self.widget_1.GetEventPosition()
            (lastX2, lastY2) = self.widget_2.GetLastEventPosition()
            (mouseX2, mouseY2) = self.widget_2.GetEventPosition()
            (lastX3, lastY3) = self.widget_3.GetLastEventPosition()
            (mouseX3, mouseY3) = self.widget_3.GetEventPosition()



            # 根据鼠标事件的移动距离调整窗宽和窗位
            WW1 = mouseX1 - lastX1
            WL1 = mouseY1 - lastY1
            WW2 = mouseX2 - lastX2
            WL2 = mouseY2 - lastY2
            WW3 = mouseX3 - lastX3
            WL3 = mouseY3 - lastY3

            color_window = self.actor.GetProperty().GetColorWindow()
            color_level = self.actor.GetProperty().GetColorLevel()

            color_window += WW1
            color_level += WL1
            color_window += WW2
            color_level += WL2
            color_window += WW3
            color_level += WL3
            # 更新vtkImageActor的窗宽和窗位
            print('窗宽窗位：', color_window, color_level)
            self.actor.GetProperty().SetColorWindow(color_window)
            self.actor.GetProperty().SetColorLevel(color_level)
            # 更新vtkImageActor的窗宽和窗位
            self.actor2.GetProperty().SetColorWindow(color_window)
            self.actor2.GetProperty().SetColorLevel(color_level)
            # 更新vtkImageActor的窗宽和窗位
            self.actor3.GetProperty().SetColorWindow(color_window)
            self.actor3.GetProperty().SetColorLevel(color_level)

            self.widget_1.Render()
            self.widget_2.Render()
            self.widget_3.Render()

            print("调节完毕")











        # else:
        #     interactorStyle.OnMouseMove()


