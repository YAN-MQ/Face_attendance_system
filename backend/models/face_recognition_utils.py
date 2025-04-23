import face_recognition
import cv2
import numpy as np
import os
import pickle
import time
from typing import Dict, List, Tuple, Optional, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('face_recognition_utils')

class FaceRecognitionUtils:
    def __init__(self, face_db_dir: str = "static/face_db", model_type: str = "hog", encoding_cache_file: str = "models/face_encodings_cache.pkl"):
        """
        初始化人脸识别工具类
        
        Args:
            face_db_dir: 人脸数据库目录
            model_type: 人脸检测模型类型，可选 'hog'(CPU) 或 'cnn'(GPU)
            encoding_cache_file: 人脸编码缓存文件
        """
        self.face_db_dir = face_db_dir
        self.model_type = model_type
        self.encoding_cache_file = encoding_cache_file
        self.encodings_cache = {}  # 学生ID -> 面部编码列表
        self.last_cache_update = 0
        self.cache_ttl = 60  # 缓存有效期（秒）
        
        # 加载缓存的面部编码
        self.load_encoding_cache()
    
    def load_encoding_cache(self) -> None:
        """加载缓存的面部编码"""
        if os.path.exists(self.encoding_cache_file):
            try:
                with open(self.encoding_cache_file, 'rb') as f:
                    cache_data = pickle.load(f)
                    self.encodings_cache = cache_data.get('encodings', {})
                    self.last_cache_update = cache_data.get('timestamp', 0)
                    
                    logger.info(f"已加载人脸编码缓存，包含 {len(self.encodings_cache)} 个学生")
            except Exception as e:
                logger.error(f"加载人脸编码缓存出错: {str(e)}")
                self.encodings_cache = {}
                self.last_cache_update = 0
    
    def save_encoding_cache(self) -> None:
        """保存面部编码到缓存文件"""
        try:
            os.makedirs(os.path.dirname(self.encoding_cache_file), exist_ok=True)
            
            with open(self.encoding_cache_file, 'wb') as f:
                cache_data = {
                    'encodings': self.encodings_cache,
                    'timestamp': time.time()
                }
                pickle.dump(cache_data, f)
                
            self.last_cache_update = time.time()
            logger.info(f"已保存人脸编码缓存，包含 {len(self.encodings_cache)} 个学生")
        except Exception as e:
            logger.error(f"保存人脸编码缓存出错: {str(e)}")
    
    def update_encodings_cache(self, force: bool = False) -> None:
        """
        更新人脸编码缓存
        
        Args:
            force: 是否强制更新缓存
        """
        current_time = time.time()
        
        # 检查缓存是否过期或强制更新
        if not force and current_time - self.last_cache_update < self.cache_ttl:
            return
        
        logger.info("开始更新人脸编码缓存...")
        
        # 扫描人脸数据库目录
        try:
            student_dirs = [d for d in os.listdir(self.face_db_dir) 
                          if os.path.isdir(os.path.join(self.face_db_dir, d))]
            
            updated_cache = {}
            
            for student_id in student_dirs:
                student_dir = os.path.join(self.face_db_dir, student_id)
                image_files = [f for f in os.listdir(student_dir) 
                             if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                
                if not image_files:
                    continue
                
                # 为每个学生计算面部编码
                student_encodings = []
                
                for img_file in image_files:
                    img_path = os.path.join(student_dir, img_file)
                    encoding = self.compute_face_encoding(img_path)
                    if encoding is not None:
                        student_encodings.append(encoding)
                
                if student_encodings:
                    updated_cache[student_id] = student_encodings
            
            # 更新缓存
            self.encodings_cache = updated_cache
            self.save_encoding_cache()
            
            logger.info(f"人脸编码缓存更新完成，包含 {len(self.encodings_cache)} 个学生")
        except Exception as e:
            logger.error(f"更新人脸编码缓存出错: {str(e)}")
    
    def compute_face_encoding(self, image_path: str) -> Optional[np.ndarray]:
        """
        计算图像中人脸的编码
        
        Args:
            image_path: 图像文件路径
            
        Returns:
            面部编码向量或None（如果未检测到人脸）
        """
        try:
            # 加载图像
            image = face_recognition.load_image_file(image_path)
            
            # 检测人脸位置
            face_locations = face_recognition.face_locations(image, model=self.model_type)
            
            if not face_locations:
                logger.warning(f"在图像 {image_path} 中未检测到人脸")
                return None
            
            # 使用第一个检测到的人脸
            face_encoding = face_recognition.face_encodings(image, [face_locations[0]])[0]
            return face_encoding
            
        except Exception as e:
            logger.error(f"计算面部编码出错 ({image_path}): {str(e)}")
            return None
    
    def compute_face_encoding_from_image(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        从图像数组计算人脸编码
        
        Args:
            image: 图像数组(BGR格式，OpenCV默认格式)
            
        Returns:
            面部编码向量或None（如果未检测到人脸）
        """
        try:
            # 转换BGR到RGB（face_recognition库需要RGB格式）
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # 检测人脸位置
            face_locations = face_recognition.face_locations(rgb_image, model=self.model_type)
            
            if not face_locations:
                logger.warning("在图像中未检测到人脸")
                return None
            
            # 使用第一个检测到的人脸
            face_encoding = face_recognition.face_encodings(rgb_image, [face_locations[0]])[0]
            return face_encoding
            
        except Exception as e:
            logger.error(f"从图像计算面部编码出错: {str(e)}")
            return None
    
    def recognize_face(self, image: np.ndarray, threshold: float = 0.6) -> Dict[str, Any]:
        """
        识别图像中的人脸
        
        Args:
            image: 图像数组(BGR格式)
            threshold: 匹配阈值，值越小越严格
            
        Returns:
            包含识别结果的字典
        """
        result = {
            "success": False,
            "student_id": None,
            "student_name": None,
            "similarity": 0.0,
            "face_location": None,
            "message": "未识别到人脸"
        }
        
        # 更新编码缓存
        self.update_encodings_cache()
        
        # 如果缓存为空，则无法识别
        if not self.encodings_cache:
            result["message"] = "人脸数据库为空"
            return result
        
        # 检测人脸并计算编码
        try:
            # 转换为RGB（face_recognition需要）
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # 检测人脸位置
            face_locations = face_recognition.face_locations(rgb_image, model=self.model_type)
            
            if not face_locations:
                return result
            
            # 使用最大的人脸（假设是最接近的）
            face_areas = [(loc[2]-loc[0])*(loc[3]-loc[1]) for loc in face_locations]
            largest_face_idx = face_areas.index(max(face_areas))
            face_location = face_locations[largest_face_idx]
            
            # 计算人脸编码
            face_encoding = face_recognition.face_encodings(rgb_image, [face_location])[0]
            
            # 与数据库中的人脸进行比对
            best_match = None
            highest_similarity = 0.0
            
            for student_id, encodings in self.encodings_cache.items():
                for encoding in encodings:
                    # 计算相似度（1 - 距离）
                    similarity = 1 - face_recognition.face_distance([encoding], face_encoding)[0]
                    
                    if similarity > highest_similarity:
                        highest_similarity = similarity
                        best_match = student_id
            
            # 检查是否达到阈值
            if highest_similarity >= threshold:
                result["success"] = True
                result["student_id"] = best_match
                result["student_name"] = best_match  # 这里可以从数据库获取实际姓名
                result["similarity"] = float(highest_similarity)
                result["face_location"] = face_location
                result["message"] = "人脸识别成功"
            else:
                result["message"] = "未找到匹配的人脸"
                result["similarity"] = float(highest_similarity)
                result["face_location"] = face_location
                
        except Exception as e:
            logger.error(f"人脸识别过程出错: {str(e)}")
            result["message"] = f"识别过程出错: {str(e)}"
            
        return result
    
    def add_face_encoding(self, student_id: str, image: np.ndarray) -> Dict[str, Any]:
        """
        添加新的人脸编码到缓存
        
        Args:
            student_id: 学生ID
            image: 图像数组(BGR格式)
            
        Returns:
            操作结果字典
        """
        result = {
            "success": False,
            "message": "添加人脸编码失败"
        }
        
        # 计算人脸编码
        face_encoding = self.compute_face_encoding_from_image(image)
        
        if face_encoding is None:
            result["message"] = "未检测到人脸，无法添加"
            return result
        
        # 更新缓存
        if student_id in self.encodings_cache:
            self.encodings_cache[student_id].append(face_encoding)
        else:
            self.encodings_cache[student_id] = [face_encoding]
        
        # 保存更新后的缓存
        self.save_encoding_cache()
        
        result["success"] = True
        result["message"] = "成功添加人脸编码"
        return result 