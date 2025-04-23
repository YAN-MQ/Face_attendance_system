import sys
import os
import json
import cv2
import numpy as np
import argparse
import base64
import time
import requests
from PIL import Image
import io

# 添加当前目录到sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入本地模块
try:
    from models.face_recognition_utils import FaceRecognitionUtils
    from models.liveness_detection_improved import ImprovedLivenessDetection
    LOCAL_MODULES_AVAILABLE = True
except ImportError:
    print("警告: 无法导入本地模块，仅进行API测试")
    LOCAL_MODULES_AVAILABLE = False

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

def test_api_liveness(image_path, method="improved"):
    """测试活体检测API"""
    try:
        print(f"使用{method}方法测试活体检测API...")
        
        # 服务器URL
        api_url = "http://localhost:5000/api/detect_liveness"
        
        # 读取图像并转换为base64
        with open(image_path, "rb") as img_file:
            test_image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        
        # 测试数据
        test_data = {
            "image": f"data:image/jpeg;base64,{test_image_base64}",
            "method": method
        }
        
        # 发送请求
        print(f"发送请求到 {api_url}...")
        response = requests.post(api_url, json=test_data)
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("is_live", False):
                print(f"测试成功: 活体检测通过，置信度: {result.get('confidence', 0)}")
                return True
            else:
                print(f"测试结果: 活体检测未通过，可能是欺骗攻击或条件不足")
                return False
        else:
            print(f"测试失败: HTTP错误 {response.status_code}")
            return False
            
    except Exception as e:
        print(f"测试异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_api_face_recognition(image_path, method="improved"):
    """测试人脸识别API"""
    try:
        print(f"测试人脸识别API...")
        
        # 服务器URL
        api_url = "http://localhost:5000/api/recognize_face"
        
        # 读取图像并转换为base64
        with open(image_path, "rb") as img_file:
            test_image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        
        # 测试数据
        test_data = {
            "image": f"data:image/jpeg;base64,{test_image_base64}",
            "method": method
        }
        
        # 发送请求
        print(f"发送请求到 {api_url}...")
        response = requests.post(api_url, json=test_data)
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success", False):
                print(f"测试成功: 识别到学生 {result.get('student_name')}, 学号: {result.get('student_id')}, 相似度: {result.get('similarity')}")
                return True
            else:
                print(f"测试结果: 人脸识别未通过，未找到匹配的人脸")
                return False
        else:
            print(f"测试失败: HTTP错误 {response.status_code}")
            return False
            
    except Exception as e:
        print(f"测试异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_local_modules(image_path):
    """测试本地模块功能"""
    if not LOCAL_MODULES_AVAILABLE:
        print("本地模块不可用，跳过本地测试")
        return False
    
    try:
        print("测试本地模块功能...")
        
        # 读取图像
        img = cv2.imread(image_path)
        if img is None:
            print(f"无法读取图像: {image_path}")
            return False
        
        # 测试活体检测
        print("\n=== 测试改进的活体检测 ===")
        liveness_detector = ImprovedLivenessDetection()
        liveness_result = liveness_detector.detect(img)
        
        print(f"活体检测结果:")
        print(f"是否为活体: {liveness_result.get('is_live', False)}")
        print(f"置信度: {liveness_result.get('confidence', 0)}")
        print(f"消息: {liveness_result.get('message', '')}")
        
        # 输出详细信息
        if 'details' in liveness_result:
            print("\n详细信息:")
            for key, value in liveness_result['details'].items():
                if isinstance(value, dict):
                    print(f"- {key}:")
                    for k, v in value.items():
                        print(f"  - {k}: {v}")
                else:
                    print(f"- {key}: {value}")
        
        # 将可视化结果保存到文件
        if 'visualized_frame' in liveness_result:
            output_path = os.path.join(os.path.dirname(image_path), 'liveness_result.jpg')
            cv2.imwrite(output_path, liveness_result['visualized_frame'])
            print(f"可视化结果已保存到: {output_path}")
        
        # 测试人脸识别
        print("\n=== 测试人脸识别 ===")
        face_recognizer = FaceRecognitionUtils()
        recognition_result = face_recognizer.recognize_face(img)
        
        print(f"人脸识别结果:")
        print(f"是否成功: {recognition_result.get('success', False)}")
        print(f"学生ID: {recognition_result.get('student_id', '未识别')}")
        print(f"相似度: {recognition_result.get('similarity', 0)}")
        print(f"消息: {recognition_result.get('message', '')}")
        
        if recognition_result.get('face_location'):
            # 在图像上标注识别结果
            output_img = img.copy()
            top, right, bottom, left = recognition_result['face_location']
            cv2.rectangle(output_img, (left, top), (right, bottom), (0, 255, 0), 2)
            
            # 添加文本
            text = f"ID: {recognition_result.get('student_id', '?')}, Conf: {recognition_result.get('similarity', 0):.2f}"
            cv2.putText(output_img, text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # 保存结果
            output_path = os.path.join(os.path.dirname(image_path), 'recognition_result.jpg')
            cv2.imwrite(output_path, output_img)
            print(f"识别结果可视化已保存到: {output_path}")
        
        return True
            
    except Exception as e:
        print(f"本地测试异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def generate_test_image():
    """生成一个简单的测试人脸图像"""
    print("生成测试图像...")
    
    # 创建一个简单的测试图像
    img = np.ones((300, 300, 3), dtype=np.uint8) * 200  # 灰色背景
    
    # 添加一些简单的面部特征
    cv2.circle(img, (150, 150), 100, (150, 150, 150), -1)  # 脸轮廓
    cv2.circle(img, (120, 120), 15, (0, 0, 0), -1)  # 左眼
    cv2.circle(img, (180, 120), 15, (0, 0, 0), -1)  # 右眼
    cv2.ellipse(img, (150, 180), (40, 20), 0, 0, 180, (0, 0, 0), -1)  # 嘴巴
    
    # 保存图像（直接使用当前目录）
    test_image_path = "./test_face_new.jpg"
    try:
        success = cv2.imwrite(test_image_path, img)
        if success:
            print(f"成功保存测试图像到: {test_image_path}")
        else:
            print(f"保存测试图像失败!")
    except Exception as e:
        print(f"保存图像时发生错误: {str(e)}")
    
    return test_image_path

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='测试活体检测和人脸识别功能')
    parser.add_argument('--image', type=str, help='测试图像路径')
    parser.add_argument('--method', type=str, default='improved', choices=['blink', 'deep_learning', 'api', 'improved'], 
                        help='活体检测方法')
    parser.add_argument('--api-only', action='store_true', help='仅测试API接口')
    parser.add_argument('--local-only', action='store_true', help='仅测试本地模块')
    
    return parser.parse_args()

if __name__ == "__main__":
    print("开始测试活体检测和人脸识别功能...")
    
    args = parse_arguments()
    
    # 总是生成一个新的测试图像
    test_image_path = generate_test_image()
    
    if args.image:
        print(f"使用指定的测试图像而不是生成的图像: {args.image}")
        test_image_path = args.image
    
    # 本地模块测试
    if not args.api_only:
        test_local_modules(test_image_path)
    
    # API测试
    if not args.local_only:
        if ensure_backend_running():
            # 测试活体检测API
            test_api_liveness(test_image_path, args.method)
            
            # 测试人脸识别API
            test_api_face_recognition(test_image_path, args.method)
        else:
            print("后端服务未运行，无法进行API测试")
    
    print("测试完成") 