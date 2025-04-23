import sys
import os
import json
import requests
import base64
import traceback
import numpy as np
import cv2
from PIL import Image
import io

# 添加当前目录到sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_register_face():
    """测试人脸注册API"""
    try:
        print("开始测试人脸注册API...")
        
        # 服务器URL
        api_url = "http://localhost:5000/api/register_face"
        
        # 创建一个有效的测试图像
        # 方法1：使用OpenCV创建图像
        test_img = np.ones((100, 100, 3), dtype=np.uint8) * 255  # 创建100x100白色图像
        _, img_encoded = cv2.imencode('.jpg', test_img)
        test_image_base64 = base64.b64encode(img_encoded).decode('utf-8')
        
        # 测试数据
        test_data = {
            "image": f"data:image/jpeg;base64,{test_image_base64}",
            "student_id": "test_student_002",
            "student_name": "测试学生2",
            "class_id": "class1"
        }
        
        # 发送请求
        print(f"发送请求到 {api_url}...")
        response = requests.post(api_url, json=test_data)
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("测试成功: 人脸注册API工作正常")
                return True
            else:
                print(f"测试失败: API返回错误 - {result.get('error', '未知错误')}")
                return False
        else:
            print(f"测试失败: HTTP错误 {response.status_code}")
            return False
            
    except Exception as e:
        print(f"测试异常: {str(e)}")
        traceback.print_exc()
        return False

def test_register_face_with_real_image():
    """使用本地真实图像测试人脸注册API"""
    try:
        print("使用实际图像测试人脸注册API...")
        
        # 服务器URL
        api_url = "http://localhost:5000/api/register_face"
        
        # 从本地文件读取图像（如果有）
        test_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_face.jpg")
        
        if not os.path.exists(test_image_path):
            print(f"测试图像文件不存在: {test_image_path}，创建测试图像...")
            # 创建一个简单的测试图像并保存
            test_img = np.ones((200, 200, 3), dtype=np.uint8) * 200  # 灰色图像
            
            # 添加一些图案，让它看起来像脸（非常简单的模拟）
            cv2.circle(test_img, (100, 100), 70, (150, 150, 150), -1)  # 脸轮廓
            cv2.circle(test_img, (70, 80), 10, (0, 0, 0), -1)  # 左眼
            cv2.circle(test_img, (130, 80), 10, (0, 0, 0), -1)  # 右眼
            cv2.ellipse(test_img, (100, 130), (30, 10), 0, 0, 180, (0, 0, 0), -1)  # 嘴巴
            
            cv2.imwrite(test_image_path, test_img)
            print(f"测试图像已保存到: {test_image_path}")
        
        # 读取图像并转换为base64
        with open(test_image_path, "rb") as img_file:
            test_image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        
        # 测试数据
        test_data = {
            "image": f"data:image/jpeg;base64,{test_image_base64}",
            "student_id": "test_student_003",
            "student_name": "测试学生3",
            "class_id": "class1"
        }
        
        # 发送请求
        print(f"发送请求到 {api_url}...")
        response = requests.post(api_url, json=test_data)
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("测试成功: 人脸注册API工作正常")
                return True
            else:
                print(f"测试失败: API返回错误 - {result.get('error', '未知错误')}")
                return False
        else:
            print(f"测试失败: HTTP错误 {response.status_code}")
            return False
            
    except Exception as e:
        print(f"测试异常: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("开始API测试...")
    
    # 测试人脸注册API（简单白色图像）
    register_ok = test_register_face()
    
    if not register_ok:
        print("使用简单图像测试失败，尝试使用真实图像...")
        # 如果简单图像测试失败，尝试使用真实图像测试
        register_ok = test_register_face_with_real_image()
    
    if register_ok:
        print("API测试成功!")
        sys.exit(0)
    else:
        print("API测试失败!")
        sys.exit(1) 