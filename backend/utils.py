import numpy as np
import os

def to_serializable(obj):
    """将包含 NumPy 类型的对象转换为可 JSON 序列化的对象"""
    try:
        if isinstance(obj, dict):
            return {k: to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [to_serializable(i) for i in obj]
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.bool_, np.integer, np.floating, np.str_)):
            return obj.item()
        elif hasattr(obj, '__dict__'):  # 处理自定义类对象
            return to_serializable(obj.__dict__)
        else:
            return obj
    except Exception as e:
        print(f"序列化错误: {str(e)}")
        return str(obj)  # 转换为字符串作为后备选项

def ensure_directory(directory):
    """确保目录存在，如果不存在则创建"""
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory
