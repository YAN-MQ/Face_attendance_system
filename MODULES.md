# 模块代码位置

## 前端模块

- **Home.vue**: `frontend/src/views/Home.vue` - 主页视图，包含考勤系统的主要功能展示。
- **Attendance.vue**: `frontend/src/views/Attendance.vue` - 考勤打卡页面，负责处理人脸识别和活体检测。
- **Register.vue**: `frontend/src/views/Register.vue` - 人脸注册页面，用于新学生的人脸信息录入。
- **Records.vue**: `frontend/src/views/Records.vue` - 考勤记录页面，提供考勤数据的查看和导出功能。

## 后端模块

- **server.js**: `backend/server.js` - 后端服务器入口文件，负责API请求的处理。
- **auth.js**: `backend/routes/auth.js` - 认证相关的API路由，处理用户登录和注册。
- **attendance.js**: `backend/routes/attendance.js` - 考勤相关的API路由，处理考勤数据的存储和查询。

## 数据库配置

- **db.js**: `backend/config/db.js` - 数据库连接配置文件，负责连接MongoDB数据库。

## 配置文件

- **.env**: `backend/.env` - 环境变量配置文件，存储敏感信息如数据库连接字符串。

## 样式文件

- **styles.css**: `frontend/src/assets/styles.css` - 全局样式文件，定义项目的基本样式和主题。 