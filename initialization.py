from interface import Ui_MainWindow
import vtk
import os
import SimpleITK
import pydicom
from vtkmodules.vtkRenderingVolume import vtkGPUVolumeRayCastMapper
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDiscretizableColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import numpy as np

from pydicom.tag import Tag



class DICOMTag:
    def __init__(self, group, element):
        self.group = group
        self.element = element

    def GetKey(self):
        return str(Tag(self.group, self.element))



class Initialization(QMainWindow, Ui_MainWindow):




    def dispatch_file(self,file_path):
        if file_path.endswith('.nii') or file_path.endswith('.nii.gz'):
            Initialization.process_nii_file(self,file_path)
        # elif file_path.endswith('.dcm') or file_path.endswith('.dicom'):
        #     Initialization.process_dicom_file(self,file_path)
        else:
            Initialization.process_dicom_file(self,file_path)



        # NII格式文件的处理逻辑
    def process_nii_file(self,file_path):

        self.reader = vtk.vtkNIFTIImageReader()
        self.reader.SetFileName(file_path)

        self.reader.SetDataOrigin(0.0, 0.0, 0.0)
        self.reader.SetDataScalarTypeToUnsignedShort()
        self.reader.UpdateWholeExtent()

        # self.reader.Update()

        # 后期将下面这段内容放到一段函数内部
        (xMin, xMax, yMin, yMax, zMin, zMax) = self.reader.GetExecutive().GetWholeExtent(
            self.reader.GetOutputInformation(0))
        (xSpacing, ySpacing, zSpacing) = self.reader.GetOutput().GetSpacing()
        (x0, y0, z0) = self.reader.GetOutput().GetOrigin()

        self.center = [x0 + xSpacing * 0.5 * (xMin + xMax),
                       y0 + ySpacing * 0.5 * (yMin + yMax),
                       z0 + zSpacing * 0.5 * (zMin + zMax)]
        print(self.center)


        # Matrices for axial, coronal, sagittal, oblique view orientations

        self.axial.DeepCopy((1, 0, 0, self.center[0],
                        0, 1, 0, self.center[1],
                        0, 0, 1, self.center[2],
                        0, 0, 0, 1))


        self.coronal.DeepCopy((1, 0, 0, self.center[0],
                          0, 0, -1, self.center[1],
                          0, 1, 0, self.center[2],
                          0, 0, 0, 1))


        self.sagittal.DeepCopy((0, 0, 1, self.center[0],
                           1, 0, 0, self.center[1],
                           0, 1, 0, self.center[2],
                           0, 0, 0, 1))



    def process_dicom_file(self,file_path):


        # 读取患者信息
        reader2 = SimpleITK.ImageSeriesReader()
        image_path = reader2.GetGDCMSeriesFileNames(file_path)

        series_0 = image_path[0]
        dcm = pydicom.dcmread(series_0)
        # 提取DICOM文件的患者信息
        self.info = {
            "name": getattr(dcm, "PatientName", "无"),
            "id": getattr(dcm, "PatientID", "无"),
            "sex": getattr(dcm, "PatientSex", "无"),
            "date": getattr(dcm, "StudyDate", "无"),
            "age": getattr(dcm, "PatientAge", "无")
        }



        self.reader.SetDirectoryName(file_path)
        # self.reader.SetDataExtent(0, 511, 0, 511, 0, 361)
        # self.reader.SetDataSpacing(3.2, 3.2, 1.5)
        self.reader.SetDataOrigin(0.0, 0.0, 0.0)
        self.reader.SetDataScalarTypeToUnsignedShort()
        self.reader.UpdateWholeExtent()

        # Calculate the center of the volume
        self.reader.Update()

        (xMin, xMax, yMin, yMax, zMin, zMax) = self.reader.GetExecutive().GetWholeExtent(
            self.reader.GetOutputInformation(0))
        (xSpacing, ySpacing, zSpacing) = self.reader.GetOutput().GetSpacing()
        (x0, y0, z0) = self.reader.GetOutput().GetOrigin()

        self.center = [x0 + xSpacing * 0.5 * (xMin + xMax),
                       y0 + ySpacing * 0.5 * (yMin + yMax),
                       z0 + zSpacing * 0.5 * (zMin + zMax)]
        print(self.center)

        # Matrices for axial, coronal, sagittal, oblique view orientations

        self.axial.DeepCopy((1, 0, 0, self.center[0],
                        0, 1, 0, self.center[1],
                        0, 0, 1, self.center[2],
                        0, 0, 0, 1))


        self.coronal.DeepCopy((1, 0, 0, self.center[0],
                          0, 0, -1, self.center[1],
                          0, -1, 0, self.center[2],
                          0, 0, 0, 1))


        self.sagittal.DeepCopy((0, 0, 1, self.center[0],
                           1, 0, 0, self.center[1],
                           0, -1, 0, self.center[2],
                           0, 0, 0, 1))



    def call_back_action_open_dir(self):


        file_path = r".\data\series-000001"
        Initialization.dispatch_file(self,file_path)

        self.label_5.setText("姓名：" + str(self.info["name"]))
        self.label_6.setText("性别: " + str(self.info["sex"]))
        self.label_7.setText("患者ID:" + str(self.info["id"]))
        self.label_8.setText("检查日期：" + str(self.info["date"]))
        self.label_9.setText("患者年龄: " + str(self.info["age"]))

        # 设置切片
        self.reslice_1 = vtk.vtkImageReslice()
        self.reslice_1.SetInputData(self.reader.GetOutput())
        # self.reslice_1.SetOutputSpacing(0.5, 0.5, 1)
        self.reslice_1.SetOutputDimensionality(2)
        self.reslice_1.SetResliceAxes(self.sagittal)
        self.reslice_1.SetInterpolationModeToLinear()

        self.reslice_1.Update()

        self.reslice_2 = vtk.vtkImageReslice()
        self.reslice_2.SetInputData(self.reader.GetOutput())
        # self.reslice_2.SetOutputSpacing(1.0, 1.0, 1.0)
        self.reslice_2.SetOutputDimensionality(2)
        self.reslice_2.SetResliceAxes(self.axial)
        self.reslice_2.SetInterpolationModeToLinear()
        self.reslice_2.Update()


        self.reslice_3 = vtk.vtkImageReslice()
        self.reslice_3.SetInputData(self.reader.GetOutput())
        # self.reslice_3.SetOutputSpacing(1.0, 1.0, 1.0)
        self.reslice_3.SetOutputDimensionality(2)
        self.reslice_3.SetResliceAxes(self.coronal)
        self.reslice_3.SetInterpolationModeToLinear()
        self.reslice_3.Update()




        # 获取vtkImageActor对象的窗宽和窗位
        self.actor = vtk.vtkImageActor()
        # actor.GetMapper().SetInputConnection(color.GetOutputPort())
        self.actor.SetInputData(self.reslice_1.GetOutput())
        global color_window, color_level
        color_window = self.actor.GetProperty().GetColorWindow()
        color_level = self.actor.GetProperty().GetColorLevel()

        self.actor.GetProperty().SetColorWindow(color_window)
        self.actor.GetProperty().SetColorLevel(color_level)

        # Display the image
        self.actor2 = vtk.vtkImageActor()
        # actor2.GetMapper().SetInputConnection(color2.GetOutputPort())
        self.actor2.SetInputData(self.reslice_2.GetOutput())
        self.actor2.GetProperty().SetColorWindow(color_window)
        self.actor2.GetProperty().SetColorLevel(color_level)

        # Display the image
        self.actor3 = vtk.vtkImageActor()
        # actor3.GetMapper().SetInputConnection(color3.GetOutputPort())
        self.actor3.SetInputData(self.reslice_3.GetOutput())
        self.actor3.GetProperty().SetColorWindow(color_window)
        self.actor3.GetProperty().SetColorLevel(color_level)


        # 创建一个vtkLineSource对象，表示直线的起点和终点
        self.line_source1 = vtk.vtkLineSource()
        self.line_source1.SetPoint1(0, 0, 0)
        self.line_source1.SetPoint2(0, 0, 0)


        # 创建mapper并设置polyData为输入
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.line_source1.GetOutputPort())

        # 创建一个vtkActor对象，表示渲染的实体
        line_actor1 = vtk.vtkActor()
        line_actor1.SetMapper(mapper)

        # 创建一个vtkLineSource对象，表示直线的起点和终点
        self.line_source2 = vtk.vtkLineSource()
        self.line_source2.SetPoint1(0, 0, 0)
        self.line_source2.SetPoint2(0, 0, 0)

        # 创建一个vtkPolyDataMapper对象，将数据转换为图形数据
        mapper2 = vtk.vtkPolyDataMapper()
        mapper2.SetInputConnection(self.line_source2.GetOutputPort())

        # 创建一个vtkActor对象，表示渲染的实体
        line_actor2 = vtk.vtkActor()
        line_actor2.SetMapper(mapper2)

        # 创建一个vtkLineSource对象，表示直线的起点和终点
        self.line_source3 = vtk.vtkLineSource()
        self.line_source3.SetPoint1(0, 0, 0)
        self.line_source3.SetPoint2(0, 0, 0)

        # 创建一个vtkPolyDataMapper对象，将数据转换为图形数据
        mapper3 = vtk.vtkPolyDataMapper()
        mapper3.SetInputConnection(self.line_source3.GetOutputPort())

        # 创建一个vtkActor对象，表示渲染的实体
        line_actor3 = vtk.vtkActor()
        line_actor3.SetMapper(mapper3)





        # 窗口添加场景
        self.renderer = vtk.vtkRenderer()
        self.renderer.AddActor(self.actor)
        self.renderer.AddActor(line_actor1)
        self.renderer2 = vtk.vtkRenderer()
        self.renderer2.AddActor(self.actor2)
        self.renderer2.AddActor(line_actor2)
        self.renderer3 = vtk.vtkRenderer()
        self.renderer3.AddActor(self.actor3)
        self.renderer3.AddActor(line_actor3)






        self.widget_1.GetRenderWindow().AddRenderer(self.renderer)
        self.widget_1.Initialize()
        self.widget_1.Start()

        self.widget_2.GetRenderWindow().AddRenderer(self.renderer2)
        self.widget_2.Initialize()
        self.widget_2.Start()

        self.widget_3.GetRenderWindow().AddRenderer(self.renderer3)
        self.widget_3.Initialize()
        self.widget_3.Start()









        point1 = (0,0,0)
        point2 = (100,200,300)




        # mpr窗口的线段
        self.line_source1.SetPoint1(point1[1], -point1[2], point1[0])
        self.line_source1.SetPoint2(point2[1], -point2[2], point2[0])
        self.line_source2.SetPoint1(point1[0], point1[1], point1[2])
        self.line_source2.SetPoint2(point2[0], point2[1], point2[2])
        self.line_source3.SetPoint1(point1[0], -point1[2], point1[1])
        self.line_source3.SetPoint2(point2[0], -point2[2], point2[1])









        # # 三维窗口
        file_name = r".\data\series-000001"
        self.RenList.addItem(file_name)
        #
        reader = vtk.vtkDICOMImageReader()
        reader.SetDirectoryName(file_name)


        # reader = vtk.vtkNIFTIImageReader()
        # reader.SetFileName(r"F:\jupyter notebook\data\data\imagesTr\img0037.nii.gz")

        # reader = vtk.vtkImageReader()
        # reader.SetFileName(r"C:\Users\lenovo\Desktop\3DV\data\Report.raw")
        # reader.SetDataScalarTypeToUnsignedChar()
        reader.SetFileDimensionality(3)
        # reader.SetDataExtent(0, 511, 0, 511, 0, 159)  # 根据实际数据尺寸进行设置
        # reader.SetDataSpacing(1, 1, 1)  # 根据实际数据尺寸进行设置
        reader.Update()

        flip_z = vtk.vtkImageFlip()
        flip_z.SetInputConnection(reader.GetOutputPort())
        flip_z.SetFilteredAxis(1)  # 设置x轴翻转

        flip_xz = vtk.vtkImageFlip()
        flip_xz.SetInputConnection(flip_z.GetOutputPort())
        flip_xz.SetFilteredAxis(2)  # 设置Z轴翻转


        volume_mapper = vtkGPUVolumeRayCastMapper()
        volume_mapper.SetInputConnection(reader.GetOutputPort())




        self.volume.SetMapper(volume_mapper)

        self.volume.SetProperty(self.volume_property)

        # # self.volume.RotateX(90.0)
        # self.volume.RotateZ(180.0)
        offset = [-x for x in self.center]
        print(offset)
        self.volume.SetPosition(offset)





        self.ren = vtkRenderer()  # 创建场景
        self.ren.AddViewProp(self.volume)  # 将演员添加到场景中
        self.volumes[file_name] = self.volume





        # 创建一个立方体数据源
        cubeSource = vtk.vtkCubeSource()
        # 创建一个提取边界线的过滤器
        outline = vtk.vtkOutlineFilter()
        outline.SetInputConnection(cubeSource.GetOutputPort())
        # 创建一个mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(outline.GetOutputPort())
        # 创建一个actor
        self.actor_4 = vtk.vtkActor()
        self.actor_4.SetMapper(mapper)
        # 创建一个属性对象，并设置边界线颜色为蓝色
        property = vtk.vtkProperty()
        property.SetColor(0, 0, 1)  # 设置为蓝色
        self.actor_4.SetProperty(property)
        # 设置立方体的位置和大小
        self.actor_4.SetPosition(50, 50, 50)
        self.actor_4.SetScale(10, 10, 10)
        self.ren.AddActor(self.actor_4)

        self.iren = self.widget_5.GetRenderWindow().GetInteractor()
        self.widget_5.GetRenderWindow().AddRenderer(self.ren)




        # #创建三维窗口的交互方式
        interactor_style = vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(interactor_style)




        # 添加路径拖动修改
        self.line_widget = vtk.vtkLineWidget()
        self.line_widget.SetInteractor(self.iren)
        self.line_widget.SetProp3D(self.volume)
        self.line_widget.SetPoint1(-20, -35, 62)
        self.line_widget.SetPoint2((110, 112, -125))
        # 左键实现交互操作
        self.line_widget.AddObserver("InteractionEvent", self.line_callback)
        # 监控左键交互结束事件
        self.line_widget.AddObserver("EndInteractionEvent", self.line_callback_end)
        # 添加观察者以捕获鼠标右键点击事件
        self.iren.AddObserver("RightButtonPressEvent", self.right_button_callback)





        # 创建圆柱体
        # 创建线源对象
        self.lineSource = vtk.vtkLineSource()
        self.lineSource.SetPoint1(point1)
        self.lineSource.SetPoint2(point2)

        # 创建管道滤波器对象
        self.tubeFilter = vtk.vtkTubeFilter()
        self.tubeFilter.SetInputConnection(self.lineSource.GetOutputPort())
        self.tubeFilter.SetRadius(1.5)
        self.tubeFilter.SetNumberOfSides(500)

        elevation_filter = vtk.vtkElevationFilter()
        bounds = self.tubeFilter.GetOutput().GetBounds()
        elevation_filter.SetLowPoint(0, bounds[2], 0)
        elevation_filter.SetHighPoint(0, bounds[3], 0)
        elevation_filter.SetInputConnection(self.tubeFilter.GetOutputPort())

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(elevation_filter.GetOutputPort())
        # mapper.SetLookupTable(ctf)
        mapper.SetColorModeToMapScalars()
        mapper.InterpolateScalarsBeforeMappingOn()
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)



        self.ren.AddActor(actor)         #添加探针
        self.iren.Initialize()
        self.line_widget.On()



        #
        #
        # # 创建一个轴对象
        # axes = vtk.vtkAxesActor()
        # # 将坐标轴的总长度设置为 200
        # axes.SetTotalLength(200, 200, 200)
        # # 添加轴对象到渲染器中
        # self.ren.AddActor(axes)
        # # self.renderer.AddActor(axes)
        # # self.renderer2.AddActor(axes)
        # # self.renderer3.AddActor(axes)



















        # 下面是窗口7的

        reader = vtk.vtkNIFTIImageReader()
        reader.SetFileName(r".\data\out3 (37).nii")


        # # 创建vtkImageFlip对象并设置翻转方向
        # flip_z = vtk.vtkImageFlip()
        # flip_z.SetInputConnection(reader.GetOutputPort())
        # flip_z.SetFilteredAxis(2)  # 设置Z轴翻转




        volume_mapper = vtk.vtkGPUVolumeRayCastMapper()
        volume_mapper.SetInputConnection(reader.GetOutputPort())



        self.render_7 = vtkRenderer()  # 创建场景
        self.render_7.AddActor(actor)


        volume_color = vtk.vtkColorTransferFunction()  # 颜色传递函数,是一个分段函数,RGB和下面的A都是一个0-1的值
        volume_color.AddRGBPoint(0, 0.0, 0, 0.0)  # 起点
        volume_color.AddRGBPoint(1, 1, 0, 0)  # 断点
        volume_color.AddRGBPoint(2, 0, 1, 0)  # 断点
        volume_color.AddRGBPoint(3, 0, 0, 1)  # 终点
        volume_color.AddRGBPoint(4, 1, 1, 0)  # 断点
        volume_color.AddRGBPoint(5, 0, 1, 1)  # 断点
        volume_color.AddRGBPoint(6, 1, 0, 1)  # 终点
        volume_color.AddRGBPoint(7, 255 / 255, 239 / 255, 213 / 255)  # 断点
        volume_color.AddRGBPoint(8, 0 / 255, 0 / 255, 205 / 255)  # 断点
        volume_color.AddRGBPoint(9, 205 / 255, 133 / 255, 63 / 255)  # 终点
        volume_color.AddRGBPoint(10, 210 / 255, 180 / 255, 140 / 255)  # 断点
        volume_color.AddRGBPoint(11, 102 / 255, 205 / 255, 170 / 255)  # 断点
        volume_color.AddRGBPoint(12, 0 / 255, 0 / 255, 128 / 255)  # 终点

        volume_scalar_opacity = vtk.vtkPiecewiseFunction()  # 不透明度传递函数，也是一个分段函数
        volume_scalar_opacity.AddPoint(0, 0.00)  # 起点
        volume_scalar_opacity.AddPoint(1, 0.05)  # 断点
        volume_scalar_opacity.AddPoint(10, 0.15)  # 断点
        volume_scalar_opacity.AddPoint(15, 0.85)  # 终点

        volume_property = vtk.vtkVolumeProperty()
        volume_property.SetColor(volume_color)  # 设置颜色函数用于映射数值到颜色
        volume_property.SetScalarOpacity(volume_scalar_opacity)  # 设置透明度函数用于映射数值到透明度



        volume = vtk.vtkVolume()
        volume.SetMapper(volume_mapper)
        volume.SetProperty(volume_property)
        volume.SetPosition(offset)
        self.camera = vtk.vtkCamera()

        # 将actor添加到渲染器中
        self.render_7.AddVolume(volume)
        # self.ren.AddVolume(volume)
        # self.ren.Render()
        self.render_7.ResetCamera()


        sphereSource = vtk.vtkSphereSource()
        sphereSource.SetCenter(-20, -35, 62)  # 设置球体中心位置
        sphereSource.SetRadius(10.0)  # 设置球体半径
        # 创建一个mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphereSource.GetOutputPort())
        # 创建一个actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        self.render_7.AddActor(actor)

        overlayRenderer = vtk.vtkRenderer() # 用于渲染overlay元素（如静态矩形）的渲染器
        self.widget_7.GetRenderWindow().AddRenderer(overlayRenderer) # 将overlay渲染器添加到渲染窗口




        # 设置overlay渲染器为不参与深度检测，确保其始终在最前面绘制
        overlayRenderer.SetInteractive(0)  # 禁用overlay渲染器的交互性
        overlayRenderer.SetLayer(1)  # 设置overlay渲染器在一个更高的层次，确保其绘制在顶层
        self.widget_7.GetRenderWindow().SetNumberOfLayers(2)  # 设置渲染窗口使用两个层次

        # 创建一个2D矩形的点
        self.rectangle_points = vtk.vtkPoints()
        self.rectangle_points.InsertNextPoint(0, 0, 0)
        self.rectangle_points.InsertNextPoint(200, 0, 0)  # 假设窗口宽度大约为100单位
        self.rectangle_points.InsertNextPoint(200, 20, 0)  # 矩形的高度为10单位
        self.rectangle_points.InsertNextPoint(0, 20, 0)

        # 创建四边形，并设置其顶点
        self.quad = vtk.vtkQuad()
        self.quad.GetPointIds().SetId(0, 0)
        self.quad.GetPointIds().SetId(1, 1)
        self.quad.GetPointIds().SetId(2, 2)
        self.quad.GetPointIds().SetId(3, 3)

        # 创建一个单元数组来存储四边形
        self.quads = vtk.vtkCellArray()
        self.quads.InsertNextCell(self.quad)

        # 创建PolyData来存储矩形的数据
        self.PolyData = vtk.vtkPolyData()
        self.PolyData.SetPoints(self.rectangle_points)
        self.PolyData.SetPolys(self.quads)

        # 使用PolyDataMapper2D来映射2D数据
        self.rectangle_mapper = vtk.vtkPolyDataMapper2D()
        self.rectangle_mapper.SetInputData(self.PolyData)

        # 创建一个Actor2D来显示矩形
        self.rectangle = vtk.vtkActor2D()
        self.rectangle.SetMapper(self.rectangle_mapper)
        self.rectangle.GetProperty().SetColor(1, 0, 0)  # 设置actor的颜色为红色

        self.windowSize = self.widget_7.GetRenderWindow().GetSize()
        self.rectangle.SetPosition(0, self.windowSize[1] - 480)  # 将矩形放置在窗口底部

        # 将actor添加到overlayRenderer
        overlayRenderer.AddActor(self.rectangle)  # 将定义的矩形块actor添加到overlay渲染器

        # 定义线的端点
        line_points = vtk.vtkPoints()
        line_points.InsertNextPoint(480, 0, 0)  # 线的起点，在矩形底部
        line_points.InsertNextPoint(480, 30, 0)  # 线的终点，与矩形等高

        # 创建一条线
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, 0)  # 线的起点
        line.GetPointIds().SetId(1, 1)  # 线的终点

        # 创建一个单元数组来存储线
        lines = vtk.vtkCellArray()
        lines.InsertNextCell(line)

        # 创建PolyData来存储线的数据
        line_poly_data = vtk.vtkPolyData()
        line_poly_data.SetPoints(line_points)
        line_poly_data.SetLines(lines)

        # 使用PolyDataMapper2D来映射线的2D数据
        line_mapper = vtk.vtkPolyDataMapper2D()
        line_mapper.SetInputData(line_poly_data)

        # 创建一个Actor2D来显示线
        line_actor = vtk.vtkActor2D()
        line_actor.SetMapper(line_mapper)
        line_actor.GetProperty().SetColor(1, 1, 1)  # 设置线的颜色为红色

        # 将线添加到overlay渲染器
        overlayRenderer.AddActor(line_actor)

        interactor_style = vtk.vtkInteractorStyleTrackballCamera()
        self.widget_7.SetInteractorStyle(interactor_style)


        self.widget_7.GetRenderWindow().AddRenderer(self.render_7)
        self.widget_7.Initialize()
        self.widget_7.Start()



