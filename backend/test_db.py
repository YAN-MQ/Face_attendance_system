import sys
import os
import traceback

# 添加当前目录到sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_config import SessionLocal, engine, Base
from models.database_models import Class, Student, FaceImage, AttendanceRecord
import db_utils
from sqlalchemy import text

def test_db_connection():
    """测试数据库连接"""
    try:
        print("正在测试数据库连接...")
        # 尝试连接数据库
        db = SessionLocal()
        # 执行简单查询，使用text()函数包装SQL字符串
        result = db.execute(text("SELECT 1")).fetchone()
        db.close()
        
        if result and result[0] == 1:
            print("数据库连接测试成功！")
            return True
        else:
            print("数据库连接测试失败：无法执行查询。")
            return False
    except Exception as e:
        print(f"数据库连接测试失败: {str(e)}")
        traceback.print_exc()
        return False

def ensure_default_classes():
    """确保默认班级数据存在"""
    try:
        print("确保默认班级数据存在...")
        db = SessionLocal()
        
        # 检查是否已经存在班级数据
        classes = db.query(Class).all()
        if classes:
            print(f"班级表中已有 {len(classes)} 条记录，跳过创建。")
            db.close()
            return True
        
        # 创建默认班级
        default_classes = [
            {"id": "class1", "name": "计算机科学与技术1班", "teacher": "张教授", "description": "本科2021级计算机科学与技术1班"},
            {"id": "class2", "name": "计算机科学与技术2班", "teacher": "李教授", "description": "本科2021级计算机科学与技术2班"},
            {"id": "class3", "name": "软件工程1班", "teacher": "王教授", "description": "本科2021级软件工程1班"},
            {"id": "class4", "name": "软件工程2班", "teacher": "赵教授", "description": "本科2021级软件工程2班"},
            {"id": "class5", "name": "网络工程1班", "teacher": "刘教授", "description": "本科2021级网络工程1班"}
        ]
        
        for class_data in default_classes:
            db_class = Class(
                id=class_data["id"],
                name=class_data["name"],
                teacher=class_data["teacher"],
                description=class_data["description"]
            )
            db.add(db_class)
        
        db.commit()
        print(f"成功创建默认班级数据！")
        db.close()
        return True
    except Exception as e:
        print(f"创建默认班级数据失败: {str(e)}")
        traceback.print_exc()
        if db:
            db.rollback()
            db.close()
        return False

def test_table_queries():
    """测试表查询"""
    try:
        print("正在测试表查询...")
        db = SessionLocal()
        
        # 查询班级表
        classes = db.query(Class).all()
        print(f"班级表中有 {len(classes)} 条记录")
        
        # 查询学生表
        students = db.query(Student).all()
        print(f"学生表中有 {len(students)} 条记录")
        
        # 查询人脸图像表
        face_images = db.query(FaceImage).all()
        print(f"人脸图像表中有 {len(face_images)} 条记录")
        
        # 查询考勤记录表
        attendance_records = db.query(AttendanceRecord).all()
        print(f"考勤记录表中有 {len(attendance_records)} 条记录")
        
        db.close()
        print("表查询测试成功！")
        return True
    except Exception as e:
        print(f"表查询测试失败: {str(e)}")
        traceback.print_exc()
        return False

def test_data_insertion():
    """测试数据插入"""
    try:
        print("正在测试数据插入...")
        db = SessionLocal()
        
        # 创建测试学生
        test_student_id = "test_student_001"
        test_student_name = "测试学生"
        test_class_id = "class1"
        
        # 检查学生是否已存在
        existing_student = db_utils.get_student_by_id(db, test_student_id)
        if existing_student:
            print(f"学生 {test_student_id} 已存在，跳过创建。")
        else:
            # 创建学生
            db_student = db_utils.create_student(db, test_student_id, test_student_name, test_class_id)
            print(f"成功创建学生: {db_student.name} (ID: {db_student.id})")
        
        # 添加测试人脸图像
        test_image_path = os.path.join(os.path.abspath("static/face_db"), f"{test_student_id}_test.jpg")
        
        # 创建空图像文件（仅用于测试）
        if not os.path.exists(os.path.dirname(test_image_path)):
            os.makedirs(os.path.dirname(test_image_path))
        
        if not os.path.exists(test_image_path):
            with open(test_image_path, "w") as f:
                f.write("测试图像文件")
        
        # 添加人脸图像记录
        db_face = db_utils.add_face_image(db, test_student_id, test_image_path)
        print(f"成功添加人脸图像记录: ID={db_face.id}, 路径={db_face.image_path}")
        
        # 添加考勤记录
        db_record = db_utils.record_attendance(
            db=db,
            student_id=test_student_id,
            recognition_confidence=0.95,
            liveness_method="test",
            liveness_confidence=0.9,
            status="normal"
        )
        print(f"成功添加考勤记录: ID={db_record.id}, 日期={db_record.date}")
        
        db.close()
        print("数据插入测试成功！")
        return True
    except Exception as e:
        print(f"数据插入测试失败: {str(e)}")
        traceback.print_exc()
        if db and db.is_active:
            db.rollback()
            db.close()
        return False

if __name__ == "__main__":
    print("开始数据库测试...")
    
    # 测试数据库连接
    connection_ok = test_db_connection()
    if not connection_ok:
        print("数据库连接测试失败，终止后续测试。")
        sys.exit(1)
    
    # 确保默认班级数据存在
    classes_ok = ensure_default_classes()
    if not classes_ok:
        print("创建默认班级数据失败，终止后续测试。")
        sys.exit(1)
    
    # 测试表查询
    queries_ok = test_table_queries()
    if not queries_ok:
        print("表查询测试失败，但将继续后续测试。")
    
    # 测试数据插入
    insertion_ok = test_data_insertion()
    if not insertion_ok:
        print("数据插入测试失败。")
    
    print("数据库测试完成！") 