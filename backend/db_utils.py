from sqlalchemy.orm import Session
import sys
import os

# 添加父目录到sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models.database_models import Student, FaceImage, AttendanceRecord, Class
from datetime import datetime, date, time
from typing import List, Dict, Any, Optional

def get_student_by_id(db: Session, student_id: str) -> Optional[Student]:
    """根据学生ID获取学生信息"""
    return db.query(Student).filter(Student.id == student_id).first()

def create_student(db: Session, student_id: str, student_name: str, class_id: Optional[str] = None) -> Student:
    """创建新学生"""
    db_student = Student(
        id=student_id,
        name=student_name,
        class_id=class_id,
        register_time=datetime.now()
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def add_face_image(db: Session, student_id: str, image_path: str) -> FaceImage:
    """添加人脸图像"""
    db_face = FaceImage(
        student_id=student_id,
        image_path=image_path,
        capture_time=datetime.now(),
        is_active=True
    )
    db.add(db_face)
    db.commit()
    db.refresh(db_face)
    return db_face

def get_all_face_images(db: Session) -> List[FaceImage]:
    """获取所有人脸图像"""
    return db.query(FaceImage).filter(FaceImage.is_active == True).all()

def record_attendance(db: Session, 
                     student_id: str, 
                     recognition_confidence: float = None,
                     liveness_method: str = None,
                     liveness_confidence: float = None,
                     status: str = "normal") -> AttendanceRecord:
    """记录考勤"""
    # 检查今天是否已经考勤
    today = date.today()
    existing_record = db.query(AttendanceRecord).filter(
        AttendanceRecord.student_id == student_id,
        AttendanceRecord.date == today
    ).first()
    
    if existing_record:
        return existing_record  # 今天已经考勤过了
    
    # 添加新的考勤记录
    db_record = AttendanceRecord(
        student_id=student_id,
        date=today,
        time=datetime.now().time(),
        status=status,
        recognition_confidence=recognition_confidence,
        liveness_method=liveness_method,
        liveness_confidence=liveness_confidence
    )
    
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_all_attendance_records(db: Session) -> List[AttendanceRecord]:
    """获取所有考勤记录"""
    return db.query(AttendanceRecord).all()

def get_class_by_id(db: Session, class_id: str) -> Optional[Class]:
    """根据ID获取班级信息"""
    return db.query(Class).filter(Class.id == class_id).first()

def create_class(db: Session, class_id: str, name: str, teacher: str = None, description: str = None) -> Class:
    """创建班级"""
    db_class = Class(
        id=class_id,
        name=name,
        teacher=teacher,
        description=description
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

def get_all_classes(db: Session) -> List[Class]:
    """获取所有班级"""
    return db.query(Class).all() 