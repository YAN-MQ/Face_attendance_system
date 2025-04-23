import os
import cv2
import numpy as np
import dlib
import time
import logging
from typing import Dict, Any, List, Tuple, Optional
import tensorflow as tf
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout, GlobalAveragePooling2D

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('liveness_detection')

class ImprovedLivenessDetection:
    """改进的活体检测类，集成多种检测方法"""
    
    def __init__(self, models_dir: str = "models"):
        """
        初始化活体检测器
        
        Args:
            models_dir: 模型目录
        """
        self.models_dir = models_dir
        os.makedirs(models_dir, exist_ok=True)
        
        # 人脸检测器
        self.face_detector = dlib.get_frontal_face_detector()
        
        # 面部特征点检测器
        landmarks_model_path = os.path.join(models_dir, "shape_predictor_68_face_landmarks.dat")
        if os.path.exists(landmarks_model_path):
            self.landmarks_detector = dlib.shape_predictor(landmarks_model_path)
        else:
            logger.warning(f"面部特征点检测模型文件不存在: {landmarks_model_path}")
            self.landmarks_detector = None
        
        # 深度学习模型
        self.dl_model_path = os.path.join(models_dir, "liveness_model.h5")
        if os.path.exists(self.dl_model_path):
            try:
                self.dl_model = load_model(self.dl_model_path)
                logger.info("已加载活体检测深度学习模型")
            except Exception as e:
                logger.error(f"加载深度学习模型失败: {str(e)}")
                self.dl_model = self._create_improved_model()
        else:
            logger.info("未找到预训练的活体检测模型，创建新模型")
            self.dl_model = self._create_improved_model()
        
        # 活体检测参数
        self.EYE_AR_THRESH = 0.2  # 眨眼检测阈值
        self.EYE_AR_CONSEC_FRAMES = 2  # 眨眼连续帧数
        self.blink_counter = 0
        self.blink_total = 0
        self.last_blink_time = 0
        
        # 眼睛关键点索引
        self.LEFT_EYE_INDICES = [36, 37, 38, 39, 40, 41]
        self.RIGHT_EYE_INDICES = [42, 43, 44, 45, 46, 47]
        
        # 图像预处理参数
        self.input_shape = (96, 96)
        self.mean = np.array([0.485, 0.456, 0.406])
        self.std = np.array([0.229, 0.224, 0.225])
        
        # 历史数据（用于防抖动）
        self.history_buffer = []
        self.buffer_size = 5
    
    def _create_improved_model(self) -> Model:
        """创建改进的活体检测模型"""
        try:
            # 使用MobileNetV2的架构设计
            from tensorflow.keras.applications import MobileNetV2
            
            # 创建基础模型
            base_model = MobileNetV2(
                input_shape=(96, 96, 3),
                include_top=False,
                weights=None  # 不使用预训练权重
            )
            
            # 构建分类头
            inputs = Input(shape=(96, 96, 3))
            x = base_model(inputs, training=False)
            x = GlobalAveragePooling2D()(x)
            x = Dense(128, activation='relu')(x)
            x = Dropout(0.5)(x)
            outputs = Dense(1, activation='sigmoid')(x)
            
            # 构建完整模型
            model = Model(inputs, outputs)
            model.compile(
                optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy']
            )
            
            # 保存模型
            model.save(self.dl_model_path)
            logger.info("已创建并保存改进的活体检测模型")
            
            return model
            
        except Exception as e:
            logger.error(f"创建改进模型失败: {str(e)}")
            
            # 创建一个简单的备选模型
            logger.info("创建简单备选模型")
            input_layer = Input(shape=(96, 96, 3))
            x = Conv2D(32, (3, 3), activation='relu', padding='same')(input_layer)
            x = MaxPooling2D(pool_size=(2, 2))(x)
            x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
            x = MaxPooling2D(pool_size=(2, 2))(x)
            x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
            x = MaxPooling2D(pool_size=(2, 2))(x)
            x = Flatten()(x)
            x = Dense(128, activation='relu')(x)
            x = Dropout(0.5)(x)
            output_layer = Dense(1, activation='sigmoid')(x)
            
            model = Model(inputs=input_layer, outputs=output_layer)
            model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
            
            # 保存简单模型
            model.save(self.dl_model_path)
            
            return model
    
    def detect_faces(self, frame: np.ndarray) -> List[dlib.rectangle]:
        """检测图像中的人脸"""
        # 转为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 使用dlib检测器
        faces = self.face_detector(gray, 0)
        
        return faces
    
    def get_landmarks(self, frame: np.ndarray) -> List[np.ndarray]:
        """获取图像中所有人脸的特征点"""
        if self.landmarks_detector is None:
            logger.warning("面部特征点检测器未初始化")
            return []
            
        # 转为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 检测人脸
        faces = self.face_detector(gray, 0)
        
        landmarks = []
        for face in faces:
            # 检测面部特征点
            shape = self.landmarks_detector(gray, face)
            
            # 将特征点坐标转换为numpy数组
            coords = np.zeros((68, 2), dtype=int)
            for i in range(0, 68):
                coords[i] = (shape.part(i).x, shape.part(i).y)
            
            landmarks.append(coords)
        
        return landmarks
    
    def eye_aspect_ratio(self, eye: np.ndarray) -> float:
        """计算眼睛纵横比（EAR）"""
        # 计算垂直眼点之间的距离
        A = np.linalg.norm(eye[1] - eye[5])
        B = np.linalg.norm(eye[2] - eye[4])
        
        # 计算水平眼点之间的距离
        C = np.linalg.norm(eye[0] - eye[3])
        
        # 计算眼睛长宽比 (EAR)
        ear = (A + B) / (2.0 * C) if C > 0 else 0
        return ear
    
    def extract_face(self, frame: np.ndarray, face: dlib.rectangle) -> np.ndarray:
        """从图像中提取人脸区域"""
        x, y = face.left(), face.top()
        w, h = face.width(), face.height()
        
        # 确保面部区域不超出图像范围
        x1 = max(0, x - int(w * 0.1))
        y1 = max(0, y - int(h * 0.1))
        x2 = min(frame.shape[1], x + w + int(w * 0.1))
        y2 = min(frame.shape[0], y + h + int(h * 0.1))
        
        # 提取人脸区域
        face_img = frame[y1:y2, x1:x2]
        
        return face_img
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """预处理图像用于深度学习模型输入"""
        # 调整图像大小
        image = cv2.resize(image, self.input_shape)
        
        # 转换为浮点数并归一化
        image = image.astype(np.float32) / 255.0
        
        # 标准化
        image = (image - self.mean) / self.std
        
        # 扩展批次维度
        image = np.expand_dims(image, axis=0)
        
        return image
    
    def analyze_texture(self, face_img: np.ndarray) -> float:
        """分析面部纹理特征"""
        # 转换为灰度图
        gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        
        # 计算局部二值模式(LBP)特征
        lbp = np.zeros_like(gray)
        for i in range(1, gray.shape[0] - 1):
            for j in range(1, gray.shape[1] - 1):
                center = gray[i, j]
                neighbors = [gray[i-1, j-1], gray[i-1, j], gray[i-1, j+1],
                            gray[i, j+1], gray[i+1, j+1], gray[i+1, j],
                            gray[i+1, j-1], gray[i, j-1]]
                binary = [1 if n >= center else 0 for n in neighbors]
                lbp[i, j] = sum([b * (2 ** idx) for idx, b in enumerate(binary)])
        
        # 计算LBP直方图
        hist, _ = np.histogram(lbp, bins=256, range=(0, 256))
        
        # 归一化直方图
        hist = hist.astype(np.float32) / (lbp.shape[0] * lbp.shape[1])
        
        # 使用高频纹理比例作为评分
        high_freq_ratio = np.sum(hist[128:]) / np.sum(hist)
        
        return high_freq_ratio
    
    def analyze_image_quality(self, face_img: np.ndarray) -> Dict[str, float]:
        """分析图像质量"""
        # 转换为灰度图
        gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        
        # 计算拉普拉斯变换（评估清晰度）
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # 计算亮度
        brightness = np.mean(gray)
        
        # 计算对比度
        contrast = np.std(gray)
        
        return {
            "sharpness": float(laplacian_var),
            "brightness": float(brightness),
            "contrast": float(contrast)
        }
    
    def check_blink(self, landmarks: np.ndarray) -> Dict[str, Any]:
        """检查是否眨眼"""
        # 提取左右眼的特征点
        left_eye = landmarks[self.LEFT_EYE_INDICES]
        right_eye = landmarks[self.RIGHT_EYE_INDICES]
        
        # 计算双眼的EAR
        left_ear = self.eye_aspect_ratio(left_eye)
        right_ear = self.eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0
        
        # 检查是否眨眼
        is_blinking = ear < self.EYE_AR_THRESH
        
        if is_blinking:
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
        
        # 如果5秒内有眨眼，就认为是活体
        is_live_blink = self.blink_total > 0 and time_since_last_blink < 5.0
        
        return {
            "is_blinking": is_blinking,
            "ear": ear,
            "blink_count": self.blink_total,
            "is_live": is_live_blink,
            "time_since_last_blink": time_since_last_blink,
            "confidence": 1.0 - time_since_last_blink / 5.0 if is_live_blink else 0.0
        }
    
    def detect_with_dl_model(self, face_img: np.ndarray) -> Dict[str, Any]:
        """使用深度学习模型进行活体检测"""
        if self.dl_model is None:
            return {"is_live": False, "confidence": 0.0, "message": "未加载深度学习模型"}
        
        try:
            # 预处理图像
            processed_img = self.preprocess_image(face_img)
            
            # 使用模型进行预测
            prediction = self.dl_model.predict(processed_img)[0][0]
            
            # 纹理分析作为辅助特征
            texture_score = self.analyze_texture(face_img)
            
            # 结合深度学习预测和纹理分析
            combined_score = prediction * 0.7 + texture_score * 0.3
            
            # 设置阈值
            is_live = combined_score > 0.5
            
            return {
                "is_live": bool(is_live),
                "confidence": float(combined_score),
                "dl_score": float(prediction),
                "texture_score": float(texture_score)
            }
            
        except Exception as e:
            logger.error(f"深度学习模型预测出错: {str(e)}")
            return {"is_live": False, "confidence": 0.0, "error": str(e)}
    
    def apply_smoothing(self, current_result: Dict[str, Any]) -> Dict[str, Any]:
        """应用平滑处理，防止结果抖动"""
        # 添加当前结果到历史缓冲区
        self.history_buffer.append(current_result)
        
        # 保持缓冲区大小
        if len(self.history_buffer) > self.buffer_size:
            self.history_buffer.pop(0)
        
        # 如果缓冲区为空，直接返回当前结果
        if len(self.history_buffer) <= 1:
            return current_result
        
        # 计算平滑后的结果
        smoothed_result = current_result.copy()
        
        # 计算平均置信度
        confidences = [r["confidence"] for r in self.history_buffer if "confidence" in r]
        if confidences:
            smoothed_result["confidence"] = sum(confidences) / len(confidences)
        
        # 多数投票决定是否为活体
        live_votes = sum(1 for r in self.history_buffer if r.get("is_live", False))
        smoothed_result["is_live"] = live_votes > len(self.history_buffer) / 2
        
        return smoothed_result
    
    def detect(self, frame: np.ndarray) -> Dict[str, Any]:
        """综合多种方法进行活体检测"""
        result = {
            "is_live": False,
            "message": "活体检测失败",
            "confidence": 0.0,
            "method": "improved",
            "details": {}
        }
        
        # 检测人脸
        faces = self.detect_faces(frame)
        
        if len(faces) == 0:
            result["message"] = "未检测到人脸"
            return result
        
        # 提取第一个检测到的人脸
        face = faces[0]
        face_img = self.extract_face(frame, face)
        
        # 获取面部特征点
        landmarks = self.get_landmarks(frame)
        
        # 图像质量分析
        quality_metrics = self.analyze_image_quality(face_img)
        result["details"]["quality"] = quality_metrics
        
        # 眨眼检测
        blink_result = None
        if landmarks and len(landmarks) > 0:
            blink_result = self.check_blink(landmarks[0])
            result["details"]["blink"] = blink_result
        
        # 深度学习检测
        dl_result = self.detect_with_dl_model(face_img)
        result["details"]["deep_learning"] = dl_result
        
        # 综合多种方法
        combined_result = {}
        
        # 权重分配
        weights = {
            "blink": 0.3,
            "deep_learning": 0.7
        }
        
        # 默认深度学习结果
        combined_result["is_live"] = dl_result.get("is_live", False)
        combined_result["confidence"] = dl_result.get("confidence", 0.0)
        
        # 如果有眨眼检测结果，则综合考虑
        if blink_result:
            is_live_combined = (
                dl_result.get("is_live", False) and weights["deep_learning"] >= 0.5
            ) or (
                blink_result.get("is_live", False) and weights["blink"] >= 0.5
            )
            
            confidence_combined = (
                dl_result.get("confidence", 0.0) * weights["deep_learning"] +
                blink_result.get("confidence", 0.0) * weights["blink"]
            )
            
            combined_result["is_live"] = is_live_combined
            combined_result["confidence"] = confidence_combined
        
        # 应用平滑处理
        smoothed_result = self.apply_smoothing(combined_result)
        
        # 设置最终结果
        result["is_live"] = smoothed_result["is_live"]
        result["confidence"] = smoothed_result["confidence"]
        
        if result["is_live"]:
            result["message"] = "检测为真实人脸"
        else:
            result["message"] = "检测为欺骗攻击"
        
        # 添加可视化结果
        visualized_frame = frame.copy()
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        color = (0, 255, 0) if result["is_live"] else (0, 0, 255)
        cv2.rectangle(visualized_frame, (x, y), (x+w, y+h), color, 2)
        
        # 添加结果标签
        label = f"Live: {result['is_live']}, Conf: {result['confidence']:.2f}"
        cv2.putText(
            visualized_frame, 
            label, 
            (x, y-10), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.5, 
            color, 
            2
        )
        
        # 如果有眨眼检测结果，在图像上标注
        if landmarks and len(landmarks) > 0:
            for eye_points in [self.LEFT_EYE_INDICES, self.RIGHT_EYE_INDICES]:
                for i in eye_points:
                    cv2.circle(visualized_frame, tuple(landmarks[0][i]), 2, (0, 255, 255), -1)
        
        result["visualized_frame"] = visualized_frame
        
        return result 