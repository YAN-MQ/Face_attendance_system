import cv2
import numpy as np
import dlib
from collections import deque
import time
import os

class BlinkDetector:
    def __init__(self):
        print("初始化眨眼检测模块...")
        # 初始化人脸检测器和人脸关键点检测器
        self.detector = dlib.get_frontal_face_detector()
        # 加载预训练的面部特征点检测器（68个点）
       
        model_path = os.path.join("models/shape_predictor_68_face_landmarks.dat")
        print(f"加载人脸特征点模型: {model_path}")
        
        # 加载预训练的面部特征点检测器（68个点）
        self.predictor = dlib.shape_predictor(model_path)
        # 用于检测眨眼的参数 - 进一步降低阈值
        self.EYE_AR_THRESH = 0.25  # 眼睛长宽比阈值 - 设置更高使检测更灵敏
        self.EYE_AR_CONSEC_FRAMES = 1  # 眼睛闭合的连续帧数 - 降为1帧使检测更灵敏
        
        # 保存最近的EAR值历史
        self.ear_history = deque(maxlen=10)
        self.baseline_ear = None  # 基线EAR值
        
        # 用于存储眨眼状态的队列
        self.blink_counter = 0
        self.blink_total = 0
        self.last_blink_time = time.time()
        
        # 每次调用detect方法时重置检测状态
        self.reset_on_each_call = True
        
        # 用于计算EAR的眼睛点索引
        self.LEFT_EYE_INDICES = [36, 37, 38, 39, 40, 41]
        self.RIGHT_EYE_INDICES = [42, 43, 44, 45, 46, 47]
        
        print("眨眼检测模块初始化完成")
    
    def eye_aspect_ratio(self, eye):
        # 计算垂直眼点之间的距离
        A = np.linalg.norm(eye[1] - eye[5])
        B = np.linalg.norm(eye[2] - eye[4])
        
        # 计算水平眼点之间的距离
        C = np.linalg.norm(eye[0] - eye[3])
        
        # 避免除零错误
        if C < 0.1:  # 如果分母接近于0
            return 1.0  # 返回一个较大的值
        
        # 计算眼睛长宽比 (EAR)
        ear = (A + B) / (2.0 * C)
        return ear
    
    def get_landmarks(self, frame):
        # 转换为灰度图像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 检测人脸
        faces = self.detector(gray, 0)
        print(f"检测到 {len(faces)} 个人脸")
        
        landmarks = []
        for face in faces:
            # 检测面部特征点
            shape = self.predictor(gray, face)
            
            # 将特征点坐标转换为numpy数组
            coords = np.zeros((68, 2), dtype=int)
            for i in range(0, 68):
                coords[i] = (shape.part(i).x, shape.part(i).y)
            
            landmarks.append(coords)
        
        return landmarks
    
    def detect(self, frame):
        # 如果设置了每次调用重置状态
        if self.reset_on_each_call:
            print("重置眨眼检测状态...")
            self.blink_counter = 0
            self.blink_total = 0
        
        landmarks = self.get_landmarks(frame)
        
        result = {
            "is_live": False,
            "message": "未检测到眨眼",
            "confidence": 0,
            "faces_detected": len(landmarks)
        }
        
        if not landmarks:
            result["message"] = "未检测到人脸"
            return result
        
        # 只处理第一个检测到的人脸
        landmarks = landmarks[0]
        
        # 提取左右眼的特征点
        left_eye = landmarks[self.LEFT_EYE_INDICES]
        right_eye = landmarks[self.RIGHT_EYE_INDICES]
        
        # 计算双眼的EAR
        left_ear = self.eye_aspect_ratio(left_eye)
        right_ear = self.eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0
        
        # 更新EAR历史
        self.ear_history.append(ear)
        
        # 计算EAR变化量
        if len(self.ear_history) >= 3:
            # 如果没有基线，使用最初几帧的平均值
            if self.baseline_ear is None and len(self.ear_history) >= 5:
                self.baseline_ear = sum(list(self.ear_history)[:5]) / 5
                print(f"设置基线EAR值: {self.baseline_ear:.4f}")
            
            # 计算EAR变化
            ear_change = abs(ear - self.ear_history[-2])
            print(f"眼睛长宽比(EAR): {ear:.4f}, 变化量: {ear_change:.4f}, 阈值: {self.EYE_AR_THRESH}")
            
            # 检测显著下降，这可能表示眨眼
            if (self.baseline_ear and ear < self.baseline_ear * 0.85) or ear_change > 0.04:
                self.blink_counter += 1
                print(f"检测到可能的眨眼动作: 眼睛变化明显")
                # 立即计为眨眼
                if self.blink_counter >= self.EYE_AR_CONSEC_FRAMES:
                    self.blink_total += 1
                    print(f"确认眨眼! 总数: {self.blink_total}")
                    self.last_blink_time = time.time()
        else:
            print(f"眼睛长宽比(EAR): {ear:.4f}, 初始化EAR历史数据...")
        
        # 判断活体检测结果
        if self.blink_total > 0:
            result["is_live"] = True
            result["message"] = f"检测到眨眼次数: {self.blink_total}"
            result["confidence"] = min(0.5 + self.blink_total * 0.1, 0.95)
            print(f"活体检测结果: 是, 置信度: {result['confidence']:.2f}")
        else:
            print("活体检测结果: 否，未检测到眨眼")
        
        # 可视化眨眼检测结果（用于调试）
        visualized_frame = frame.copy()
        for eye in [left_eye, right_eye]:
            hull = cv2.convexHull(eye)
            cv2.drawContours(visualized_frame, [hull], -1, (0, 255, 0), 1)
        
        result["visualized_frame"] = visualized_frame
        result["ear"] = ear
        
        return result 