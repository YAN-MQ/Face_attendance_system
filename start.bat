@echo off
:: filepath: e:\内容安全\final\start_system.bat
echo 启动人脸识别与活体检测班级考勤系统...
echo ======================================

:: 设置窗口标题
title 人脸识别与活体检测班级考勤系统

:: 创建必要的目录
echo 创建必要的目录...
if not exist "backend\static\face_db" mkdir "backend\static\face_db"
if not exist "backend\static\uploads" mkdir "backend\static\uploads"

:: 检查目录权限
echo 检查目录权限...
echo 测试写入权限... > "backend\static\face_db\test_write.txt"
if not exist "backend\static\face_db\test_write.txt" (
    echo 错误: 无法写入到 backend\static\face_db 目录，请检查权限设置。
    echo 您可能需要以管理员身份运行此脚本。
    goto end
) else (
    del "backend\static\face_db\test_write.txt"
    echo 目录权限正常。
)

:: 检查Python环境
echo 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未检测到Python环境，请确保已安装Python并添加到PATH中。
    goto end
)

:: 检查必要的Python包
echo 检查Python依赖包...
python -c "import cv2, numpy, flask, pillow" >nul 2>&1
if %errorlevel% neq 0 (
    echo 警告: 某些Python依赖包可能未安装。
    echo 尝试安装必要的依赖...
    cd backend
    pip install -r requirements.txt
    cd ..
)

:: 检查Node.js环境
echo 检查Node.js环境...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未检测到Node.js环境，请确保已安装Node.js并添加到PATH中。
    goto end
)

:: 测试图像保存功能
echo 测试图像保存功能...
cd backend
python test_register.py >nul 2>&1
if %errorlevel% neq 0 (
    echo 警告: 图像保存测试未通过，请检查目录权限和OpenCV配置。
    echo 系统将继续启动，但图像保存功能可能无法正常工作。
    timeout /t 5 /nobreak > nul
) else (
    echo 图像保存功能测试通过。
)

:: 检查MySQL
echo 检查MySQL环境...
echo 数据库信息: 用户名=root, 密码=123456
echo 正在初始化数据库...

python initialize_db.py
if %errorlevel% neq 0 (
    echo 警告: 数据库初始化可能未完成，请检查MySQL配置。
    echo 确保MySQL服务已启动，用户名为root，密码为123456。
    timeout /t 5 /nobreak > nul
    :: 继续执行，不中断程序
)

:: 测试数据库连接
echo 正在测试数据库连接...
python test_db.py
if %errorlevel% neq 0 (
    echo 警告: 数据库测试未通过，系统可能无法正常工作。
    echo 请确保MySQL服务已启动，并且数据库配置正确。
    timeout /t 5 /nobreak > nul
)
cd ..

:: 启动后端服务
echo 启动后端服务中...
start cmd /k "title 考勤系统后端 & cd backend & python app.py"

:: 等待2秒，确保后端服务已启动
timeout /t 2 /nobreak > nul

:: 启动前端服务
echo 启动前端服务中...
start cmd /k "title 考勤系统前端 & cd frontend & npm run serve"

:: 等待5秒
timeout /t 5 /nobreak > nul

:: 自动打开浏览器
echo 正在打开浏览器...
start http://localhost:8080

echo ======================================
echo 系统已启动！
echo 后端服务地址: http://localhost:5000
echo 前端服务地址: http://localhost:8080
echo 请勿关闭命令行窗口，关闭窗口将停止服务。

:end
pause