import coord
from interface import Ui_MainWindow
from PyQt5.QtWidgets import  QMainWindow
import vtk
import threading
import numpy as np




class Update(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Update, self).__init__(parent)
        self.setupUi(self)







    def set_gradient_color_line(self, render, line_source, point1, point2, actor_attribute_name):

        if actor_attribute_name =="actor_1":
            point1 = (point1[0], -point1[2], 5)
            point2 = (point2[0], -point2[2], 5)
        elif actor_attribute_name =="actor_2":
            point1 = (point1[1], point1[0], 5)
            point2 = (point2[1], point2[0], 5)
        elif actor_attribute_name =="actor_3":
            point1 = (point1[1], -point1[2], 5)
            point2 = (point2[1], -point2[2], 5)






        line_source.SetPoint1(point1)
        line_source.SetPoint2(point2)
        line_source.Update()

        # 创建颜色数组
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.InsertNextTuple3(255, 0, 0)  # 红色
        colors.InsertNextTuple3(0, 0, 255)  # 蓝色

        # 创建vtkPolyData并设置颜色
        polyData = vtk.vtkPolyData()
        polyData.ShallowCopy(line_source.GetOutput())
        polyData.GetPointData().SetScalars(colors)

        # 创建mapper并设置polyData为输入
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(polyData)

        # 创建actor并设置mapper
        new_actor = vtk.vtkActor()
        new_actor.SetMapper(mapper)

        # 如果之前的actor存在，则先移除
        old_actor = getattr(self, actor_attribute_name)
        if old_actor is not None:
            render.RemoveActor(old_actor)

        # 添加新的actor到渲染器
        render.AddActor(new_actor)

        # 更新actor引用
        setattr(self, actor_attribute_name, new_actor)







    def update_lines(self):
        # 设置三条线段的位置和颜色

        Update.set_gradient_color_line(self, self.renderer, self.line_source1, self.point1, self.point2, 'actor_1')
        Update.set_gradient_color_line(self, self.renderer2, self.line_source2, self.point1, self.point2, 'actor_2')
        Update.set_gradient_color_line(self, self.renderer3, self.line_source3, self.point1, self.point2, 'actor_3')




    def update_widget_5(self):       # 更新窗口5的线段位置

        self.point1 = coord.p_main_B
        self.point2 = coord.p_sub_B[:3]

        # 更新线段的位置
        self.lineSource.SetPoint1(self.point1)
        self.lineSource.SetPoint2(self.point2)

        #mpr窗口的线段
        Update.update_lines(self)



        self.lineSource.Update()
        self.line_source1.Update()
        self.line_source2.Update()
        self.line_source3.Update()
        self.tubeFilter.Update()
        self.widget_1.Render()
        self.widget_2.Render()
        self.widget_3.Render()
        self.widget_5.Render()


    def update_widget_7(self):  # 更新窗口7的相机位置

        extensionFactor = 0.5
        newEndPoint = [self.point2[i] + extensionFactor * (self.point2[i] - self.point1[i]) for i in range(3)]
        self.camera.SetPosition(self.point2)  # 设置相机位置为直线起点
        self.camera.SetFocalPoint(newEndPoint)  # 设置相机焦点为直线终点
        self.render_7.SetActiveCamera(self.camera)
        self.widget_7.Render()



    def distance(self):

        # 这是病灶点坐标，
        point_bingzao = self.line_widget.GetPoint1()
        point_jinzhendian = self.line_widget.GetPoint2()
        # 计算调整后的值
        self.instance = Update.distance_with_direction(self, self.point1, self.point2, point_bingzao)
        # print("调整后的值是:", self.instance)

        # 跟雷达显示有关
        # 对于self.lineSource的每个端点，计算到self.previous_line_actor直线的最短距离
        distance_point1 = Update.point_to_line_distance(self.point2, point_bingzao, point_jinzhendian)
        distance_point2 = Update.point_to_line_distance(self.point1, point_bingzao, point_jinzhendian)

        # print(distance_point1,distance_point2)





        # 更新矩形的长度
        # 确保矩形的宽度不超过窗口宽度
        newWidth =min(abs(480 - self.instance), self.windowSize[0])

        # 更新点集以改变矩形的长度
        self.rectangle_points.Reset()
        self.rectangle_points.InsertNextPoint(0, 0, 0)
        self.rectangle_points.InsertNextPoint(newWidth, 0, 0)
        self.rectangle_points.InsertNextPoint(newWidth, 20, 0)
        self.rectangle_points.InsertNextPoint(0, 20, 0)

        # 由于修改了矩形的大小，需要重新创建和设置CellArray
        # 重新构建CellArray
        self.quads = vtk.vtkCellArray()
        quad = vtk.vtkQuad()
        quad.GetPointIds().SetId(0, 0)
        quad.GetPointIds().SetId(1, 1)
        quad.GetPointIds().SetId(2, 2)
        quad.GetPointIds().SetId(3, 3)
        self.quads.InsertNextCell(quad)
        self.PolyData.SetPolys(self.quads)

        # 创建PolyData来存储矩形的数据
        self.PolyData.SetPoints(self.rectangle_points)

        # 可能需要重新设置mapper的输入数据
        self.rectangle_mapper.SetInputData(self.PolyData)










    def calculate_vector(a, b):
        """计算向量b到a"""
        return np.array(b) - np.array(a)
    def dot_product(v1, v2):
        """计算两个向量的点积"""
        return np.dot(v1, v2)


    def distance_with_direction(self,point1, point2, point_bingzao):
        """根据消融针的方向调整距离值"""
        v12 = Update.calculate_vector(point1, point2)  # 消融针尾端到尖端的向量
        v2B = Update.calculate_vector(point2, point_bingzao)  # 消融针尖端到病灶点的向量

        dp = Update.dot_product(v12, v2B)  # 计算点积
        distance = np.linalg.norm(v2B)  # 计算尖端到病灶点的距离

        if dp > 0:

            self.rectangle.GetProperty().SetColor(0, 1, 0)  # 设置actor的颜色为红色
            return distance  # 消融针朝向病灶点，距离为正

        else:
            self.rectangle.GetProperty().SetColor(1, 0, 0)  # 设置actor的颜色为红色
            return -distance  # 消融针远离病灶点，距离取负


    # 修改后的计算点到直线的最短距离的函数
    def point_to_line_distance(point, line_point1, line_point2):
        point = np.array(point)
        line_point1 = np.array(line_point1)
        line_point2 = np.array(line_point2)
        line_vec = line_point2 - line_point1
        point_vec = point - line_point1
        distance = np.linalg.norm(np.cross(line_vec, point_vec)) / np.linalg.norm(line_vec)
        return distance









    # 采用多线程，将窗口5和窗口7同时进行更新
    # 实时显示消融针和路径的位置关系，有增加了一个线程
    def update_line(self, obj,event):  # 更新窗口5的线段位置
        thread1 = threading.Thread(target=Update.update_widget_5(self))
        thread2 = threading.Thread(target=Update.update_widget_7(self))
        thread3 = threading.Thread(target=Update.distance(self))


        # 启动线程
        thread1.start()
        thread2.start()
        thread3.start()

