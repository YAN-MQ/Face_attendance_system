# 基于人脸识别与活体检测的班级考勤系统

本系统是一个基于BS架构的班级考勤系统，采用人脸识别与活体检测技术，实现自动化考勤。

## 系统架构

- 前端：Vue.js
- 后端：Python Flask

## 主要功能

1. 人脸采集与识别
2. 活体检测（支持多种方案）
3. 考勤记录管理
4. 班级信息管理

## 活体检测方案

系统集成了三种不同的活体检测方案：
1. 基于眨眼检测的活体检测
2. 基于深度学习的纹理分析活体检测
3. 基于第三方API (腾讯云人脸识别API) 的活体检测

## 安装与使用

### 环境要求

- Python 3.8+
- Node.js 14+
- npm 6+
- 摄像头

### 后端环境配置

1. 安装Python依赖：

```bash
cd backend
pip install -r requirements.txt
```

2. 下载人脸关键点检测模型：

需要下载dlib的面部特征点检测器模型文件 `shape_predictor_68_face_landmarks.dat`，并放置在 `backend/models` 目录下。

可以从以下链接下载：
http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

下载后解压并放置在正确位置：

```bash
cd backend/models
# 解压下载的文件
bunzip2 shape_predictor_68_face_landmarks.dat.bz2
```

### 启动后端

```bash
cd backend
python app.py
```

服务器将在本地启动，默认端口为5000：http://localhost:5000

### 前端环境配置

```bash
cd frontend
npm install
```

### 启动前端开发服务器

```bash
cd frontend
npm run serve
```

前端开发服务器将启动，通常在：http://localhost:8080

### 常见问题解决

如果遇到 ESLint 配置错误，请确保项目根目录中包含 `.eslintrc.js` 文件。该文件已包含在代码库中，如果缺失，请参考文档重新创建。

## 系统使用

1. 首先在"人脸注册"页面为学生注册人脸信息
2. 在"考勤打卡"页面进行人脸识别考勤
3. 在"考勤记录"页面查看和管理考勤记录
4. 在"班级管理"页面管理班级信息
5. 在"系统设置"页面配置活体检测方案和其他系统设置

## 效果展示

[待添加系统截图和效果展示]

## 安全说明

本系统集成了多种活体检测技术，能够有效抵抗照片和视频攻击，提高考勤系统的安全性。