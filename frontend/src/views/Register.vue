<template>
  <div class="container">
    <h1>人脸注册</h1>
    <div class="video-container">
      <video ref="video" width="640" height="480" autoplay></video>
      <canvas ref="canvas" width="640" height="480" style="display: none;"></canvas>
      <div class="captured-container" v-if="capturedImage">
        <img :src="capturedImage" alt="Captured Image" class="captured-image" />
        <button @click="clearCapturedImage" class="clear-btn">重拍</button>
                  </div>
      <button @click="captureImage" v-if="!capturedImage" class="capture-btn">拍照</button>
                  </div>
                  
    <div class="form-container">
      <form @submit.prevent="registerFace">
        <div class="form-group">
          <label for="studentId">学号</label>
          <input
            type="text"
            id="studentId"
                        v-model="studentId"
                        required
            class="form-control"
          />
        </div>
        <div class="form-group">
          <label for="studentName">姓名</label>
          <input
            type="text"
            id="studentName"
                        v-model="studentName"
                        required
            class="form-control"
          />
        </div>
        <div class="form-group">
          <label for="classId">班级</label>
          <select id="classId" v-model="classId" required class="form-control">
            <option value="">请选择班级</option>
            <option v-for="cls in classes" :key="cls.id" :value="cls.id">
              {{ cls.name }}
            </option>
          </select>
        </div>
        <button 
          type="submit" 
          class="submit-btn" 
          :disabled="isSubmitting || !capturedImage || !studentId || !studentName || !classId"
                      >
          {{ isSubmitting ? '保存中...' : '保存注册信息' }}
        </button>
        <div v-if="registrationStatus" class="status-message" :class="registrationStatus.type">
          {{ registrationStatus.message }}
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "Register",
  data() {
    return {
      videoStream: null,
    capturedImage: null,
      studentId: "",
      studentName: "",
      classId: "",
      classes: [
        { id: "class1", name: "计算机科学与技术1班" },
        { id: "class2", name: "软件工程1班" },
        { id: "class3", name: "人工智能1班" }
      ],
      isSubmitting: false,
      registrationStatus: null
    };
  },
  mounted() {
    this.startCamera();
  },
  beforeUnmount() {
    this.stopCamera();
  },
  methods: {
    startCamera() {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices
          .getUserMedia({ video: true })
          .then(stream => {
            this.videoStream = stream;
            this.$refs.video.srcObject = stream;
          })
          .catch(err => {
            console.error("无法访问摄像头:", err);
            alert("无法访问摄像头，请确保您的设备有摄像头并且已授权使用。");
          });
      } else {
        console.error("浏览器不支持getUserMedia");
        alert("您的浏览器不支持访问摄像头功能，请更换浏览器后重试。");
      }
    },
    stopCamera() {
      if (this.videoStream) {
        this.videoStream.getTracks().forEach(track => track.stop());
      }
    },
    captureImage() {
      const video = this.$refs.video;
      const canvas = this.$refs.canvas;
      const context = canvas.getContext("2d");
      
      // 设置canvas尺寸与视频一致
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      // 在canvas上绘制当前视频帧
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      
      // 获取图像数据并转换为URL (高质量JPEG)
      this.capturedImage = canvas.toDataURL("image/jpeg", 0.95);
      
      console.log("图像已捕获");
      console.log(`图像数据长度: ${this.capturedImage.length} 字符`);
      console.log(`图像数据前缀: ${this.capturedImage.substring(0, 50)}...`);
    },
    clearCapturedImage() {
      this.capturedImage = null;
    },
    async registerFace() {
      // 表单验证
      if (!this.capturedImage) {
        this.showStatus("请先拍照捕获人脸图像", "error");
        return;
      }
      
      if (!this.studentId || !this.studentName || !this.classId) {
        this.showStatus("请填写所有必要信息", "error");
        return;
      }
      
      this.isSubmitting = true; // 开始提交状态
      this.showStatus("正在处理图像和保存信息...", "pending");
      
      try {
        console.log("准备发送注册请求:");
        console.log(`学号: ${this.studentId}, 姓名: ${this.studentName}, 班级: ${this.classId}`);
        console.log(`图像数据长度: ${this.capturedImage.length} 字符`);
        
        const result = await this.$store.dispatch("registerFace", {
        imageData: this.capturedImage,
        studentId: this.studentId,
          studentName: this.studentName,
          classId: this.classId
      });
      
        console.log("注册请求响应:", result);
      
      if (result.success) {
          this.showStatus("注册成功！", "success");
          // 重置表单
          setTimeout(() => {
            this.studentId = "";
            this.studentName = "";
            this.classId = "";
            this.clearCapturedImage();
            this.registrationStatus = null;
          }, 2000);
        } else {
          this.showStatus(`注册失败: ${result.error || '未知错误'}`, "error");
        }
      } catch (error) {
        console.error("注册过程中发生错误:", error);
        this.showStatus(`注册错误: ${error.message || '未知错误'}`, "error");
      } finally {
        this.isSubmitting = false; // 结束提交状态
    }
  },
    showStatus(message, type) {
      this.registrationStatus = { message, type };
  }
}
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.video-container {
  position: relative;
  margin-bottom: 20px;
  text-align: center;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
}

.captured-container {
  position: relative;
  display: inline-block;
}

.captured-image {
  max-width: 100%;
  max-height: 480px;
  display: block;
  margin: 0 auto;
}

.capture-btn, .clear-btn, .submit-btn {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin: 10px 0;
}

.capture-btn:hover, .clear-btn:hover, .submit-btn:hover {
  background-color: #45a049;
}

.capture-btn:disabled, .clear-btn:disabled, .submit-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.clear-btn {
  background-color: #f44336;
  position: absolute;
  top: 10px;
  right: 10px;
}

.clear-btn:hover {
  background-color: #d32f2f;
}

.form-container {
  margin-top: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input, select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.status-message {
  margin-top: 15px;
  padding: 10px;
  border-radius: 4px;
  text-align: center;
}

.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.pending {
  background-color: #e2f3f5;
  color: #0c5460;
  border: 1px solid #bee5eb;
}
</style> 