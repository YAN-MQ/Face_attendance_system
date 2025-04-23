import mysql.connector
import sys
import os
import traceback

# 添加当前目录到sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_config import engine, Base, SessionLocal
from models.database_models import Class, Student, FaceImage, AttendanceRecord

def create_database():
    """创建MySQL数据库"""
    try:
        print("正在连接MySQL服务器...")
        # 连接MySQL服务器
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456'
        )
        
        cursor = conn.cursor()
        
        # 创建数据库
        print("正在创建数据库face_attendance...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS face_attendance")
        
        print("数据库 'face_attendance' 创建成功！")
        
        # 关闭连接
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"创建数据库时出错: {str(e)}")
        traceback.print_exc()
        return False
    
    return True

def create_tables():
    """创建数据库表"""
    try:
        print("正在创建数据库表...")
        # 创建定义的表
        Base.metadata.create_all(bind=engine)
        print("数据库表创建成功！")
        return True
    except Exception as e:
        print(f"创建表时出错: {str(e)}")
        traceback.print_exc()
        return False

def create_default_classes():
    """创建默认班级数据"""
    try:
        print("正在创建默认班级数据...")
        db = SessionLocal()
        
        # 默认班级列表
        default_classes = [
            {"id": "class1", "name": "计算机科学与技术1班", "teacher": "张教授", "description": "本科2021级计算机科学与技术1班"},
            {"id": "class2", "name": "计算机科学与技术2班", "teacher": "李教授", "description": "本科2021级计算机科学与技术2班"},
            {"id": "class3", "name": "软件工程1班", "teacher": "王教授", "description": "本科2021级软件工程1班"},
            {"id": "class4", "name": "软件工程2班", "teacher": "赵教授", "description": "本科2021级软件工程2班"},
            {"id": "class5", "name": "网络工程1班", "teacher": "刘教授", "description": "本科2021级网络工程1班"}
        ]
        
        # 检查是否已经存在班级数据
        existing_classes = db.query(Class).all()
        if existing_classes:
            print(f"已存在{len(existing_classes)}个班级数据，跳过默认班级创建。")
            db.close()
            return True
        
        # 添加默认班级
        for class_data in default_classes:
            db_class = Class(
                id=class_data["id"],
                name=class_data["name"],
                teacher=class_data["teacher"],
                description=class_data["description"]
            )
            db.add(db_class)
        
        db.commit()
        db.close()
        print(f"成功创建{len(default_classes)}个默认班级！")
        return True
    except Exception as e:
        print(f"创建默认班级数据时出错: {str(e)}")
        traceback.print_exc()
        return False

def import_existing_data():
    """导入现有JSON数据到数据库（如果需要）"""
    # 此功能可以稍后实现
    pass

if __name__ == "__main__":
    print("开始初始化数据库...")
    db_created = create_database()
    
    if db_created:
        tables_created = create_tables()
        
        if tables_created:
            classes_created = create_default_classes()
            
            if classes_created:
                print("数据库初始化完成！")
            else:
                print("警告：数据库表创建成功，但默认班级创建失败。")
        else:
            print("数据库初始化失败：无法创建表。")
    else:
        print("数据库初始化失败：无法创建数据库。") 