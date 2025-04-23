# 项目目录结构

本项目采用前后端分离的架构，分为backend和frontend两个主要目录。

## 根目录结构

```
├── README.md             # 项目说明文档
├── ARCHITECTURE.md       # 系统架构说明文档
├── STRUCTURE.md          # 目录结构说明文档（本文件）
├── backend/              # 后端代码目录
└── frontend/             # 前端代码目录
```

## 后端目录结构

```
backend/
├── app.py                # Flask应用主文件，包含路由和API接口定义
├── requirements.txt      # Python依赖列表
├── models/               # 活体检测模型目录
│   ├── blink_detection.py       # 基于眨眼的活体检测实现
│   ├── deep_learning_liveness.py # 基于深度学习的活体检测实现
│   ├── api_liveness.py          # 基于第三方API的活体检测实现
│   ├── api_config.json          # API配置文件（运行时生成）
│   └── shape_predictor_68_face_landmarks.dat # 人脸特征点检测模型（需要下载）
├── static/               # 静态资源目录
│   ├── face_db/          # 人脸数据库目录（运行时生成）
│   ├── attendance_records.json  # 考勤记录文件（运行时生成）
│   └── class_info.json          # 班级信息文件（运行时生成）
└── templates/            # HTML模板目录
    └── index.html        # 主页模板
```

## 前端目录结构

```
frontend/
├── public/               # 公共资源目录
│   ├── index.html        # HTML入口文件
│   └── favicon.ico       # 网站图标
├── src/                  # 源代码目录
│   ├── assets/           # 静态资源目录
│   │   └── logo.png      # 项目Logo
│   ├── components/       # Vue组件目录
│   ├── plugins/          # 插件目录
│   │   └── vuetify.js    # Vuetify配置文件
│   ├── router/           # 路由目录
│   │   └── index.js      # 路由配置文件
│   ├── store/            # Vuex状态管理目录
│   │   └── index.js      # Vuex配置文件
│   ├── views/            # 视图组件目录
│   │   ├── Home.vue      # 首页组件
│   │   ├── Attendance.vue # 考勤打卡组件
│   │   ├── Register.vue  # 人脸注册组件
│   │   ├── Records.vue   # 考勤记录组件
│   │   ├── Classes.vue   # 班级管理组件
│   │   └── Settings.vue  # 系统设置组件
│   ├── App.vue           # 根组件
│   └── main.js           # 应用入口文件
└── package.json          # 项目配置文件，包含依赖和命令
```

## 数据存储结构

### 人脸数据库
```
static/face_db/
├── student_id_1/        # 学生ID为目录名
│   ├── student_id_1_20230501123045.jpg  # 人脸图像，包含时间戳
│   ├── student_id_1_20230501123145.jpg  # 可以存储多张照片
│   └── info.json        # 学生基本信息
├── student_id_2/
│   ├── student_id_2_20230501124512.jpg
│   └── info.json
└── ...
```

### 考勤记录
```json
[
  {
    "student_id": "student_id_1",
    "student_name": "张三",
    "date": "2023-05-01",
    "time": "09:30:25",
    "status": "normal"
  },
  {
    "student_id": "student_id_2",
    "student_name": "李四",
    "date": "2023-05-01",
    "time": "09:45:10",
    "status": "late"
  }
]
```

### 班级信息
```json
{
  "classes": [
    {
      "id": "class1",
      "name": "计算机科学与技术1班",
      "teacher": "张教授",
      "description": "本科2021级计算机科学与技术1班",
      "student_count": 45
    },
    {
      "id": "class2",
      "name": "计算机科学与技术2班",
      "teacher": "李教授",
      "description": "本科2021级计算机科学与技术2班",
      "student_count": 42
    }
  ]
}
``` 