import sys
import os
import json
import requests
import base64
import cv2
import numpy as np
import traceback
import webbrowser
from PIL import Image
import io
import time
import imghdr

# 添加当前目录到sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_config import SessionLocal
from models.database_models import Class, Student, FaceImage, AttendanceRecord

def ensure_backend_running():
    """检查后端服务是否运行"""
    print("检查后端服务是否运行...")
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            print("后端服务正在运行")
            return True
        else:
            print(f"后端服务返回状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"无法连接到后端服务: {str(e)}")
        return False

def check_database_connection():
    """检查数据库连接是否正常"""
    print("检查数据库连接...")
    try:
        db = SessionLocal()
        classes = db.query(Class).all()
        students = db.query(Student).all()
        images = db.query(FaceImage).all()
        
        print(f"数据库连接成功:")
        print(f"  - 班级数量: {len(classes)}")
        print(f"  - 学生数量: {len(students)}")
        print(f"  - 人脸图像数量: {len(images)}")
        
        for cls in classes:
            print(f"班级: {cls.id} - {cls.name}")
        
        for student in students:
            print(f"学生: {student.id} - {student.name} (班级: {student.class_id})")
            # 检查学生的人脸图像
            student_images = db.query(FaceImage).filter(FaceImage.student_id == student.id).all()
            for img in student_images:
                print(f"  - 图像: {img.id} - {img.image_path}")
                # 检查文件是否存在
                if os.path.exists(img.image_path):
                    print(f"    文件存在，大小: {os.path.getsize(img.image_path)} 字节")
                    # 尝试读取图像
                    try:
                        test_img = cv2.imread(img.image_path)
                        if test_img is not None:
                            print(f"    图像读取成功，尺寸: {test_img.shape}")
                        else:
                            print(f"    图像读取失败")
                    except Exception as e:
                        print(f"    无法读取图像: {str(e)}")
                else:
                    print(f"    文件不存在")
        
        db.close()
        return True
    except Exception as e:
        print(f"数据库连接检查失败: {str(e)}")
        traceback.print_exc()
        return False

def test_manual_register():
    """手动创建测试数据进行注册测试"""
    print("执行手动注册测试...")
    try:
        # 创建测试图像
        test_img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "manual_test_image.jpg")
        
        # 创建一个简单的测试图像
        test_img = np.ones((300, 300, 3), dtype=np.uint8) * 200  # 灰色图像
        
        # 添加一些图案，让它看起来像脸
        cv2.circle(test_img, (150, 150), 100, (100, 100, 100), -1)  # 脸轮廓
        cv2.circle(test_img, (120, 120), 15, (0, 0, 0), -1)  # 左眼
        cv2.circle(test_img, (180, 120), 15, (0, 0, 0), -1)  # 右眼
        cv2.ellipse(test_img, (150, 180), (40, 20), 0, 0, 180, (0, 0, 0), -1)  # 嘴巴
        
        # 保存图像
        cv2.imwrite(test_img_path, test_img)
        print(f"测试图像已保存到: {test_img_path}")
        
        # 检查图像类型
        img_type = imghdr.what(test_img_path)
        print(f"图像类型: {img_type}")
        
        # 检查文件大小
        file_size = os.path.getsize(test_img_path)
        print(f"文件大小: {file_size} 字节")
        
        # 读取图像并转换为base64
        with open(test_img_path, "rb") as img_file:
            img_bytes = img_file.read()
            test_image_base64 = base64.b64encode(img_bytes).decode('utf-8')
        
        print(f"Base64编码长度: {len(test_image_base64)}")
        
        # 准备请求数据
        student_id = f"manual_test_{int(time.time())}"
        student_name = "手动测试学生"
        class_id = "class1"  # 确保这个班级ID存在
        
        request_data = {
            "image": f"data:image/jpeg;base64,{test_image_base64}",
            "student_id": student_id,
            "student_name": student_name,
            "class_id": class_id
        }
        
        # 发送请求
        print(f"发送注册请求...")
        response = requests.post("http://localhost:5000/api/register_face", json=request_data)
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        # 检查响应
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("注册成功!")
                # 检查数据库中是否有记录
                db = SessionLocal()
                student = db.query(Student).filter(Student.id == student_id).first()
                if student:
                    print(f"数据库中找到学生记录: {student.id} - {student.name}")
                    # 检查人脸图像记录
                    face_images = db.query(FaceImage).filter(FaceImage.student_id == student_id).all()
                    print(f"找到 {len(face_images)} 个人脸图像记录")
                    for img in face_images:
                        print(f"图像路径: {img.image_path}")
                        if os.path.exists(img.image_path):
                            print(f"图像文件存在，大小: {os.path.getsize(img.image_path)} 字节")
                        else:
                            print(f"图像文件不存在!")
                else:
                    print(f"数据库中未找到学生记录!")
                db.close()
                return True
            else:
                print(f"注册失败: {result.get('error', '未知错误')}")
                return False
        else:
            print(f"请求失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"手动注册测试失败: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("开始执行人脸注册功能检查...")
    
    # 检查后端服务是否运行
    if not ensure_backend_running():
        print("后端服务未运行，请先启动后端服务。")
        sys.exit(1)
    
    # 检查数据库连接
    if not check_database_connection():
        print("数据库连接异常，请检查数据库配置。")
    
    # 手动创建测试数据进行注册测试
    if test_manual_register():
        print("手动注册测试成功!")
    else:
        print("手动注册测试失败!")
    
    print("检查完成。") 