import numpy as np
import vtk


# 创建直线
def create_line_actor(p1, p2):
    lineSource = vtk.vtkLineSource()
    lineSource.SetPoint1(p1)
    lineSource.SetPoint2(p2)
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(lineSource.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor

# 创建垂直路径视角
def set_camera_for_parallel_view(renderer, p1, p2):
    mid_point = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, (p1[2] + p2[2]) / 2]
    direction = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
    camera = renderer.GetActiveCamera()
    camera.SetPosition(mid_point[0] - direction[0], mid_point[1] - direction[1], mid_point[2] - direction[2])
    camera.SetFocalPoint(mid_point)
    camera.SetViewUp(0, 0, 1)

# 创建水平路径视角
def set_camera_for_perpendicular_view(renderer, p1, p2):
    mid_point = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, (p1[2] + p2[2]) / 2]
    camera = renderer.GetActiveCamera()
    camera.SetPosition(mid_point[0], mid_point[1], mid_point[2] + 1)
    camera.SetFocalPoint(mid_point)
    camera.SetViewUp(0, 1, 0)



# 创建圆环
def create_concentric_circle_lines(center, max_radius, num_circles, num_points=100):
    actors = []
    for i in range(1, num_circles + 1):
        # 计算当前圆的半径
        radius = max_radius * i / num_circles

        # 创建点和线
        points = vtk.vtkPoints()
        polyLine = vtk.vtkPolyLine()
        polyLine.GetPointIds().SetNumberOfIds(num_points)

        for j in range(num_points):
            angle = 2.0 * np.pi * j / num_points
            x = center[0] + radius * np.cos(angle)
            y = center[1] + radius * np.sin(angle)
            z = center[2]
            points.InsertNextPoint(x, y, z)
            polyLine.GetPointIds().SetId(j, j)

        # 创建一个单元数组来存储polyline
        cells = vtk.vtkCellArray()
        cells.InsertNextCell(polyLine)

        # 创建polydata来存储点和线
        polyData = vtk.vtkPolyData()
        polyData.SetPoints(points)
        polyData.SetLines(cells)

        # 创建映射器和演员
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(polyData)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        actors.append(actor)
    return actors

# 改变圆环角度，使其垂直到圆环
def rotate_actor_to_vector(actor, center, target_vector):
    # 计算旋转的轴和角度
    target_vector = np.array(target_vector)
    source_vector = np.array([0, 0, 1])  # Z轴，即同心圆环默认朝向
    axis = np.cross(source_vector, target_vector)
    axis_length = np.linalg.norm(axis)
    if axis_length != 0:
        axis = axis / axis_length
    angle = np.arccos(np.dot(source_vector, target_vector) / np.linalg.norm(target_vector))

    # 将角度从弧度转换为度
    angle_degrees = np.degrees(angle)

    # 创建旋转矩阵
    transform = vtk.vtkTransform()
    transform.PostMultiply()  # 确保变换按正确的顺序应用
    transform.Translate(-center[0], -center[1], -center[2])  # 平移到原点
    transform.RotateWXYZ(angle_degrees, axis)  # 应用旋转
    transform.Translate(center[0], center[1], center[2])  # 平移回原来的中心

    # 应用变换
    actor.SetUserTransform(transform)

# 设置相机以使actor1保持在视图中心
def adjust_camera_focus(renderer, mid_point, direction):
    camera = renderer.GetActiveCamera()
    camera.SetFocalPoint(mid_point)
    camera_position = [mid_point[0] - direction[0], mid_point[1] - direction[1], mid_point[2] - direction[2]]
    camera.SetPosition(camera_position)
    camera.SetViewUp(0, 0, 1)











# Define points for actor1
p1 = [0.0, 0.0, 0.0]
p2 = [2, 2, 2]

actor1_direction = np.array(p2) - np.array(p1)
# 定义中心点和参数
center = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, (p1[2] + p2[2]) / 2]
max_radius = 0.5
num_circles = 5

# 创建同心圆线
concentric_circle_lines = create_concentric_circle_lines(center, max_radius, num_circles)
# 对每个同心圆演员应用旋转
for circle_actor in concentric_circle_lines:
    rotate_actor_to_vector(circle_actor, center, actor1_direction)




# 创建 actor1 and actor2
actor1 = create_line_actor(p1, p2)
actor1.GetProperty().SetColor(1, 0, 0)  # 设置颜色
actor2 = create_line_actor([0, 0, 0], [1, 1.5, 1.5])
actor2.GetProperty().SetColor(0, 1, 0)  # 设置颜色

# 创建第一个窗口
renderer1 = vtk.vtkRenderer()
set_camera_for_parallel_view(renderer1, p1, p2)
renderer1.AddActor(actor1)
renderer1.AddActor(actor2)
# 创建渲染器和添加演员
for actor in concentric_circle_lines:
    renderer1.AddActor(actor)
renderer1.SetBackground(0.1, 0.2, 0.4)

# Setup for the second window (Perpendicular View)
renderer2 = vtk.vtkRenderer()
set_camera_for_perpendicular_view(renderer2, p1, p2)
renderer2.AddActor(actor1)
renderer2.AddActor(actor2)
renderer2.SetBackground(0.1, 0.2, 0.4)

# Create two render windows
renderWindow1 = vtk.vtkRenderWindow()
renderWindow1.AddRenderer(renderer1)
renderWindow1.SetPosition(0, 200)  # Position the window
renderWindow1.SetSize(400, 400)

renderWindow2 = vtk.vtkRenderWindow()
renderWindow2.AddRenderer(renderer2)
renderWindow2.SetPosition(410, 200)  # Position the window
renderWindow2.SetSize(400, 400)

# Create two interactor
interactor1 = vtk.vtkRenderWindowInteractor()
interactor1.SetRenderWindow(renderWindow1)

interactor2 = vtk.vtkRenderWindowInteractor()
interactor2.SetRenderWindow(renderWindow2)

# Start the interaction
renderWindow1.Render()
renderWindow2.Render()
interactor1.Start()
interactor2.Start()



