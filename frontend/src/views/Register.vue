<template>
  <div class="register-page">
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-card class="solid-card mt-3 mb-5" elevation="3">
            <v-card-title class="text-h4 font-weight-bold primary--text py-4">
              <v-icon large color="primary" class="mr-3">mdi-account-plus</v-icon>
              人脸注册
            </v-card-title>
          </v-card>
        </v-col>
      </v-row>
      
      <v-row>
        <v-col cols="12" md="7">
          <v-card class="solid-card hover-card mb-4" elevation="2">
            <v-card-title class="subtitle-1 font-weight-medium">
              <v-icon left color="primary">mdi-camera</v-icon>
              拍摄人脸照片
            </v-card-title>
            <v-card-text>
              <div class="video-container rounded-image">
                <video ref="video" width="640" height="480" autoplay class="rounded-lg"></video>
                <canvas ref="canvas" width="640" height="480" style="display: none;"></canvas>
                <transition name="fade">
                  <div class="captured-container" v-if="capturedImage">
                    <img :src="capturedImage" alt="Captured Image" class="captured-image rounded-lg" />
                    <v-btn fab small color="error" class="clear-btn btn-pulse" @click="clearCapturedImage">
                      <v-icon>mdi-refresh</v-icon>
                    </v-btn>
                  </div>
                </transition>
                <v-btn
                  color="primary"
                  large
                  rounded
                  class="capture-btn btn-pulse mt-3"
                  v-if="!capturedImage"
                  @click="captureImage"
                >
                  <v-icon left>mdi-camera</v-icon>
                  拍照
                </v-btn>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="12" md="5">
          <v-card class="solid-card hover-card" elevation="2">
            <v-card-title class="subtitle-1 font-weight-medium">
              <v-icon left color="primary">mdi-account-details</v-icon>
              学生信息
            </v-card-title>
            <v-card-text>
              <div class="form-container">
                <v-form @submit.prevent="registerFace">
                  <v-text-field
                    v-model="studentId"
                    label="学号"
                    prepend-icon="mdi-identifier"
                    outlined
                    dense
                    required
                    class="mb-3"
                  ></v-text-field>
                  
                  <v-text-field
                    v-model="studentName"
                    label="姓名"
                    prepend-icon="mdi-account"
                    outlined
                    dense
                    required
                    class="mb-3"
                  ></v-text-field>
                  
                  <v-select
                    v-model="classId"
                    :items="classes"
                    item-text="name"
                    item-value="id"
                    label="班级"
                    prepend-icon="mdi-account-group"
                    outlined
                    dense
                    required
                    class="mb-5"
                  ></v-select>
                  
                  <v-btn 
                    type="submit" 
                    color="primary" 
                    block 
                    large
                    rounded
                    class="btn-pulse" 
                    elevation="2"
                    :loading="isSubmitting"
                    :disabled="isSubmitting || !capturedImage || !studentId || !studentName || !classId"
                  >
                    <v-icon left>mdi-content-save</v-icon>
                    {{ isSubmitting ? '保存中...' : '保存注册信息' }}
                  </v-btn>
                  
                  <transition name="fade">
                    <v-alert
                      v-if="registrationStatus"
                      :type="registrationStatus.type === 'success' ? 'success' : 
                            registrationStatus.type === 'error' ? 'error' : 'info'"
                      dense
                      class="mt-4"
                      transition="scale-transition"
                    >
                      {{ registrationStatus.message }}
                    </v-alert>
                  </transition>
                </v-form>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      
      <v-row class="mt-4" v-if="capturedImage">
        <v-col cols="12">
          <v-card class="solid-card hover-card" elevation="2">
            <v-card-title class="subtitle-1 font-weight-medium">
              <v-icon left color="primary">mdi-information-outline</v-icon>
              注册须知
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12" md="6">
                  <div class="info-item">
                    <v-icon color="primary" class="mr-2">mdi-check-circle</v-icon>
                    <span>确保拍摄的照片光线充足，人脸清晰</span>
                  </div>
                </v-col>
                <v-col cols="12" md="6">
                  <div class="info-item">
                    <v-icon color="primary" class="mr-2">mdi-check-circle</v-icon>
                    <span>请填写真实准确的个人信息</span>
                  </div>
                </v-col>
                <v-col cols="12" md="6">
                  <div class="info-item">
                    <v-icon color="warning" class="mr-2">mdi-alert-circle</v-icon>
                    <span>人脸数据会安全加密存储</span>
                  </div>
                </v-col>
                <v-col cols="12" md="6">
                  <div class="info-item">
                    <v-icon color="warning" class="mr-2">mdi-alert-circle</v-icon>
                    <span>注册成功后，可直接进行考勤打卡</span>
                  </div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
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
.register-page {
  min-height: calc(100vh - 145px);
  position: relative;
}

.video-container {
  position: relative;
  margin-bottom: 20px;
  text-align: center;
  overflow: hidden;
  border-radius: 16px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

.video-container video,
.captured-image {
  width: 100%;
  max-height: 500px;
  object-fit: cover;
  border-radius: 12px;
}

.captured-container {
  position: relative;
  display: inline-block;
  width: 100%;
}

.capture-btn {
  margin: 20px auto;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.clear-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 5;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  padding: 10px;
  border-radius: 8px;
  background-color: rgba(0, 0, 0, 0.03);
  transition: all 0.3s ease;
}

.info-item:hover {
  background-color: rgba(0, 0, 0, 0.06);
  transform: translateX(5px);
}

/* 动画效果 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

.pulse {
  animation: pulse 1.5s infinite;
}

@media (max-width: 600px) {
  .video-container video,
  .captured-image {
    max-height: 350px;
  }
}
</style> 