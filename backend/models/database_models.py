from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import sys
import os

# 添加父目录到sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_config import Base

class Class(Base):
    """班级表"""
    __tablename__ = "classes"

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    teacher = Column(String(50))
    description = Column(String(200))
    
    # 关联学生
    students = relationship("Student", back_populates="class_info")

class Student(Base):
    """学生表"""
    __tablename__ = "students"

    id = Column(String(50), primary_key=True)  # 学号
    name = Column(String(50), nullable=False)  # 姓名
    class_id = Column(String(50), ForeignKey("classes.id"))  # 班级ID
    register_time = Column(DateTime, default=datetime.now)  # 注册时间
    
    # 关联
    class_info = relationship("Class", back_populates="students")
    face_images = relationship("FaceImage", back_populates="student")
    attendance_records = relationship("AttendanceRecord", back_populates="student")

class FaceImage(Base):
    """人脸图像表"""
    __tablename__ = "face_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(50), ForeignKey("students.id"), nullable=False)
    image_path = Column(String(200), nullable=False)  # 图像在磁盘上的存储路径
    capture_time = Column(DateTime, default=datetime.now)  # 采集时间
    is_active = Column(Boolean, default=True)  # 是否为当前使用的图像
    
    # 关联
    student = relationship("Student", back_populates="face_images")

class AttendanceRecord(Base):
    """考勤记录表"""
    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(50), ForeignKey("students.id"), nullable=False)
    date = Column(Date, default=func.current_date())  # 日期
    time = Column(Time, default=func.current_time())  # 时间
    status = Column(String(20), default="normal")  # 状态：normal(正常), late(迟到), leave(请假)
    recognition_confidence = Column(Float)  # 识别置信度
    liveness_method = Column(String(50))  # 使用的活体检测方法
    liveness_confidence = Column(Float)  # 活体检测置信度
    
    # 关联
    student = relationship("Student", back_populates="attendance_records") 