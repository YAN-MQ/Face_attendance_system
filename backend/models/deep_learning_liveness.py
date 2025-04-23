import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import os

class DeepLearningLiveness:
    def __init__(self):
        # 模型路径
        self.model_path = 'models/liveness_model.h5'
        
        # 如果模型不存在，则创建一个简单的模型
        if not os.path.exists(self.model_path):
            self._create_simple_model()
        else:
            # 加载预训练模型
            self.model = load_model(self.model_path)
        
        # 图像预处理参数
        self.input_shape = (96, 96)
        self.mean = np.array([0.485, 0.456, 0.406])
        self.std = np.array([0.229, 0.224, 0.225])
        
        # 人脸检测器
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def _create_simple_model(self):
        """创建一个简单的活体检测模型（用于演示）"""
        from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout
        from tensorflow.keras.models import Model
        
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
        
        self.model = Model(inputs=input_layer, outputs=output_layer)
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        
        # 保存模型
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        self.model.save(self.model_path)
    
    def preprocess_image(self, image):
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
    
    def detect_faces(self, frame):
        """检测图像中的人脸"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return faces
    
    def extract_face(self, frame, face):
        """从图像中提取人脸区域"""
        x, y, w, h = face
        # 确保面部区域不超出图像范围
        x1 = max(0, x - int(w * 0.1))
        y1 = max(0, y - int(h * 0.1))
        x2 = min(frame.shape[1], x + w + int(w * 0.1))
        y2 = min(frame.shape[0], y + h + int(h * 0.1))
        
        # 提取人脸区域
        face_img = frame[y1:y2, x1:x2]
        
        # 一些附加的处理（例如，直方图均衡化等）可以在这里添加
        
        return face_img
    
    def analyze_texture(self, face_img):
        """分析面部纹理特征"""
        # 转换为灰度图
        gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        
        # 计算局部二值模式(LBP)特征（简化版本）
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
        
        # 使用简单的启发式方法：高频纹理比例
        high_freq_ratio = np.sum(hist[128:]) / np.sum(hist)
        
        return high_freq_ratio
    
    def detect(self, frame):
        """检测输入帧是否为活体"""
        result = {
            "is_live": False,
            "message": "深度学习活体检测失败",
            "confidence": 0.0,
            "method": "deep_learning"
        }
        
        # 检测人脸
        faces = self.detect_faces(frame)
        
        if len(faces) == 0:
            result["message"] = "未检测到人脸"
            return result
        
        # 提取第一个检测到的人脸
        face = faces[0]
        face_img = self.extract_face(frame, face)
        
        # 分析纹理特征（用于防止照片攻击）
        texture_score = self.analyze_texture(face_img)
        
        # 使用深度学习模型进行活体检测
        try:
            # 预处理图像
            processed_img = self.preprocess_image(cv2.resize(face_img, self.input_shape))
            
            # 模型预测
            prediction = self.model.predict(processed_img)[0][0]
            
            # 结合纹理分析和深度学习模型的结果
            combined_score = prediction * 0.7 + texture_score * 0.3
            
            # 设置阈值
            is_live = combined_score > 0.5
            
            result["is_live"] = is_live
            result["confidence"] = float(combined_score)
            result["texture_score"] = float(texture_score)
            result["prediction"] = float(prediction)
            
            if is_live:
                result["message"] = "检测为真实人脸"
            else:
                result["message"] = "检测为欺骗攻击"
            
            # 添加可视化信息
            visualized_frame = frame.copy()
            x, y, w, h = face
            color = (0, 255, 0) if is_live else (0, 0, 255)
            cv2.rectangle(visualized_frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(
                visualized_frame, 
                f"Live: {is_live}, Conf: {combined_score:.2f}", 
                (x, y-10), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, 
                color, 
                2
            )
            result["visualized_frame"] = visualized_frame
            
        except Exception as e:
            result["message"] = f"模型预测错误: {str(e)}"
            result["error"] = str(e)
        
        return result 