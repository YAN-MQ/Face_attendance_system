import cv2
import numpy as np
import dlib
from collections import deque
import time
import os

class BlinkDetector:
    def __init__(self):
        # 初始化人脸检测器和人脸关键点检测器
        self.detector = dlib.get_frontal_face_detector()
        # 加载预训练的面部特征点检测器（68个点）
       
        model_path = os.path.join("models/shape_predictor_68_face_landmarks.dat")
        
        # 加载预训练的面部特征点检测器（68个点）
        self.predictor = dlib.shape_predictor(model_path)
        # 用于检测眨眼的参数
        self.EYE_AR_THRESH = 0.2  # 眼睛长宽比阈值
        self.EYE_AR_CONSEC_FRAMES = 3  # 眼睛闭合的连续帧数
        
        # 用于存储眨眼状态的队列
        self.blink_counter = 0
        self.blink_total = 0
        self.last_blink_time = time.time()
        
        # 用于计算EAR的眼睛点索引
        self.LEFT_EYE_INDICES = [36, 37, 38, 39, 40, 41]
        self.RIGHT_EYE_INDICES = [42, 43, 44, 45, 46, 47]
    
    def eye_aspect_ratio(self, eye):
        # 计算垂直眼点之间的距离
        A = np.linalg.norm(eye[1] - eye[5])
        B = np.linalg.norm(eye[2] - eye[4])
        
        # 计算水平眼点之间的距离
        C = np.linalg.norm(eye[0] - eye[3])
        
        # 计算眼睛长宽比 (EAR)
        ear = (A + B) / (2.0 * C)
        return ear
    
    def get_landmarks(self, frame):
        # 转换为灰度图像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 检测人脸
        faces = self.detector(gray, 0)
        
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
        
        # 检查是否眨眼
        if ear < self.EYE_AR_THRESH:
            self.blink_counter += 1
        else:
            # 如果连续几帧检测到眼睛闭合，则认为是眨眼
            if self.blink_counter >= self.EYE_AR_CONSEC_FRAMES:
                self.blink_total += 1
                self.last_blink_time = time.time()
            
            self.blink_counter = 0
        
        # 判断是否为活体（检测到眨眼且时间间隔合理）
        current_time = time.time()
        time_since_last_blink = current_time - self.last_blink_time
        
        if self.blink_total > 0 and time_since_last_blink < 3:
            result["is_live"] = True
            result["message"] = f"检测到眨眼次数: {self.blink_total}"
            result["confidence"] = min(0.5 + self.blink_total * 0.1, 0.95)
        
        # 可视化眨眼检测结果（用于调试）
        visualized_frame = frame.copy()
        for eye in [left_eye, right_eye]:
            hull = cv2.convexHull(eye)
            cv2.drawContours(visualized_frame, [hull], -1, (0, 255, 0), 1)
        
        result["visualized_frame"] = visualized_frame
        result["ear"] = ear
        
        return result 