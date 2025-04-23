import requests
import base64
import json
import os
import cv2
import numpy as np
import time

class APILiveness:
    def __init__(self):
        # 腾讯云API相关配置
        self.api_config = {
            "enabled": False,  # 默认禁用API（需要用户自己配置密钥）
            "secret_id": os.environ.get("TENCENT_SECRET_ID", ""),
            "secret_key": os.environ.get("TENCENT_SECRET_KEY", ""),
            "endpoint": "iai.tencentcloudapi.com",
            "region": "ap-guangzhou"
        }
        
        # 加载配置文件（如果存在）
        config_path = "models/api_config.json"
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    saved_config = json.load(f)
                self.api_config.update(saved_config)
            except Exception as e:
                print(f"加载API配置文件失败: {str(e)}")
        
        # 人脸检测器（作为备选）
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # 上次API调用的时间戳（用于限制调用频率）
        self.last_api_call_time = 0
        self.api_call_interval = 3  # 秒
    
    def save_config(self, config):
        """保存API配置到文件"""
        config_path = "models/api_config.json"
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, "w") as f:
            json.dump(config, f)
        
        self.api_config.update(config)
    
    def detect_faces_local(self, frame):
        """使用本地方法检测人脸（备选方案）"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return faces
    
    def call_tencent_api(self, image_base64):
        """调用腾讯云人脸识别API进行活体检测"""
        try:
            from tencentcloud.common import credential
            from tencentcloud.common.profile.client_profile import ClientProfile
            from tencentcloud.common.profile.http_profile import HttpProfile
            from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
            from tencentcloud.iai.v20200303 import iai_client, models
            
            # 实例化一个认证对象
            cred = credential.Credential(self.api_config["secret_id"], self.api_config["secret_key"])
            
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = self.api_config["endpoint"]
            
            # 实例化一个client选项
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            
            # 实例化要请求产品的client对象
            client = iai_client.IaiClient(cred, self.api_config["region"], clientProfile)
            
            # 实例化一个请求对象
            req = models.DetectLiveFaceRequest()
            params = {
                "Image": image_base64
            }
            req.from_json_string(json.dumps(params))
            
            # 发起API请求
            resp = client.DetectLiveFace(req)
            
            # 解析结果
            response_dict = json.loads(resp.to_json_string())
            
            return {
                "success": True,
                "is_live": response_dict.get("Score", 0) > 80,  # 阈值设为80
                "score": response_dict.get("Score", 0),
                "response": response_dict
            }
            
        except TencentCloudSDKException as err:
            return {
                "success": False,
                "error": str(err),
                "is_live": False,
                "score": 0
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"API调用异常: {str(e)}",
                "is_live": False,
                "score": 0
            }
    
    def detect(self, frame):
        """检测输入帧是否为活体"""
        result = {
            "is_live": False,
            "message": "API活体检测失败",
            "confidence": 0.0,
            "method": "api"
        }
        
        # 检查API是否配置
        if not self.api_config["enabled"] or not self.api_config["secret_id"] or not self.api_config["secret_key"]:
            result["message"] = "API未配置或已禁用"
            return result
        
        # 检查API调用频率
        current_time = time.time()
        if current_time - self.last_api_call_time < self.api_call_interval:
            result["message"] = f"API调用过于频繁，请等待 {self.api_call_interval - (current_time - self.last_api_call_time):.1f} 秒"
            return result
        
        # 更新API调用时间
        self.last_api_call_time = current_time
        
        # 基本的人脸检测（确保图像中有人脸）
        faces = self.detect_faces_local(frame)
        
        if len(faces) == 0:
            result["message"] = "未检测到人脸"
            return result
        
        # 将图像编码为base64
        _, buffer = cv2.imencode('.jpg', frame)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # 调用第三方API进行活体检测
        api_result = self.call_tencent_api(image_base64)
        
        # 解析API返回结果
        if api_result["success"]:
            result["is_live"] = api_result["is_live"]
            result["confidence"] = api_result["score"] / 100.0  # 归一化为0-1
            result["api_response"] = api_result["response"]
            
            if result["is_live"]:
                result["message"] = "API检测为真实人脸"
            else:
                result["message"] = "API检测为欺骗攻击"
        else:
            result["message"] = f"API调用失败: {api_result.get('error', '未知错误')}"
            result["error"] = api_result.get("error", "未知错误")
        
        # 可视化结果
        visualized_frame = frame.copy()
        for (x, y, w, h) in faces:
            color = (0, 255, 0) if result["is_live"] else (0, 0, 255)
            cv2.rectangle(visualized_frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(
                visualized_frame, 
                f"API: {result['is_live']}, Conf: {result['confidence']:.2f}", 
                (x, y-10), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, 
                color, 
                2
            )
        
        result["visualized_frame"] = visualized_frame
        
        return result
        
    def configure(self, config):
        """更新API配置"""
        self.api_config.update(config)
        self.save_config(self.api_config)
        return {"success": True, "message": "API配置已更新"} 