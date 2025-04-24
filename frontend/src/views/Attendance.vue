<template>
  <div class="attendance">
    <v-row>
      <v-col cols="12" md="8">
        <v-card elevation="4" class="hover-card primary-gradient">
          <v-card-title class="headline white--text">
            <v-icon left large color="white">mdi-account-check</v-icon>
            考勤打卡
            <v-spacer></v-spacer>
            <v-chip 
              :color="cameraStarted ? 'success' : 'error'" 
              small
              class="animated-chip"
              pill
            >
              {{ cameraStarted ? '摄像头已启动' : '摄像头未启动' }}
            </v-chip>
          </v-card-title>
          
          <v-card-text>
            <div class="camera-container rounded-image">
              <video ref="video" width="100%" autoplay playsinline></video>
              <canvas ref="canvas" style="display: none;"></canvas>
              
              <div class="camera-overlay" v-if="!cameraStarted">
                <v-btn color="primary" @click="startCamera" class="btn-pulse" rounded elevation="8">
                  <v-icon left>mdi-camera</v-icon>
                  启动摄像头
                </v-btn>
              </div>
              
              <div v-if="isLoading" class="loading-overlay">
                <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
                <div class="mt-4 text-center">
                  <div class="loading-text">处理中</div>
                  <div class="loading-wave mt-2">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                  </div>
                </div>
              </div>
              
              <div v-if="recognitionResult && recognitionResult.success" class="success-overlay">
                <v-icon color="success" size="64">mdi-check-circle</v-icon>
                <div class="mt-2 text-h6">签到成功！</div>
              </div>
              
              <div class="face-frame" v-if="cameraStarted && !isLoading"></div>
            </div>
            
            <div class="mt-5 text-center action-buttons">
              <v-btn 
                color="primary" 
                large 
                @click="captureAndRecognize" 
                :disabled="!cameraStarted || isLoading"
                class="btn-pulse mx-2"
                rounded
                elevation="3"
              >
                <v-icon left>mdi-account-check</v-icon>
                考勤打卡
              </v-btn>
              
              <v-btn 
                color="warning" 
                @click="testLivenessDetection" 
                :disabled="!cameraStarted || isLoading"
                class="btn-pulse mx-2"
                rounded
                elevation="3"
              >
                <v-icon left>mdi-shield-account</v-icon>
                测试活体
              </v-btn>
              
              <v-menu offset-y rounded="lg">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    color="info"
                    text
                    v-bind="attrs"
                    v-on="on"
                    class="mx-2"
                    rounded
                  >
                    <v-icon left>mdi-cog</v-icon>
                    活体检测方法
                    <v-icon right>mdi-chevron-down</v-icon>
                  </v-btn>
                </template>
                <v-list rounded="lg" class="menu-list">
                  <v-list-item
                    v-for="(method, index) in livenessMethods"
                    :key="index"
                    @click="updateLivenessMethod(method.value)"
                    class="rounded-lg my-1"
                  >
                    <v-list-item-icon>
                      <v-icon v-if="livenessMethod === method.value" color="success">
                        mdi-check
                      </v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ method.text }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-menu>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card elevation="4" class="hover-card mb-4 result-card">
          <v-card-title class="headline primary--text">
            <v-icon left color="primary">mdi-information</v-icon>
            检测结果
          </v-card-title>
          
          <v-card-text>
            <v-alert
              v-if="detectionResult"
              :type="detectionResult.is_live ? 'success' : 'error'"
              class="result-alert"
              rounded="lg"
              elevation="2"
            >
              <strong>活体检测结果:</strong> {{ detectionResult.message }}
              <div class="mt-2">
                <v-progress-linear
                  :value="detectionResult.confidence * 100"
                  :color="detectionResult.is_live ? 'success' : 'error'"
                  height="8"
                  striped
                  rounded
                ></v-progress-linear>
                <div class="caption text-right">
                  置信度: {{ Math.round(detectionResult.confidence * 100) }}%
                </div>
              </div>
            </v-alert>
            
            <v-alert
              v-if="recognitionResult"
              :type="recognitionResult.success ? 'success' : 'error'"
              class="result-alert"
              rounded="lg"
              elevation="2"
            >
              <strong>人脸识别结果:</strong> 
              <div v-if="recognitionResult.success">
                识别到学生 <strong>{{ recognitionResult.student_name }}</strong> ({{ recognitionResult.student_id }})
              </div>
              <div v-else>
                未找到匹配的人脸
              </div>
              <div class="mt-2" v-if="recognitionResult.similarity">
                <v-progress-linear
                  :value="recognitionResult.similarity * 100"
                  :color="getSimilarityColor(recognitionResult.similarity)"
                  height="8"
                  striped
                  rounded
                ></v-progress-linear>
                <div class="caption text-right">
                  相似度: {{ Math.round(recognitionResult.similarity * 100) }}%
                </div>
              </div>
            </v-alert>
            
            <div class="text-center py-4 no-result-box rounded-lg pa-4" v-if="!detectionResult && !recognitionResult">
              <v-icon color="grey" size="64">mdi-camera-off</v-icon>
              <div class="mt-2 grey--text">尚未进行检测</div>
            </div>
          </v-card-text>
        </v-card>
        
        <v-card elevation="4" class="hover-card guide-card">
          <v-card-title class="headline primary--text">
            <v-icon left color="primary">mdi-help-circle</v-icon>
            操作指南
          </v-card-title>
          
          <v-card-text>
            <v-timeline dense>
              <v-timeline-item color="primary">
                <div class="font-weight-medium">第一步：启动摄像头</div>
                <div class="text-caption">点击"启动摄像头"按钮，允许浏览器访问摄像头</div>
              </v-timeline-item>
              
              <v-timeline-item color="warning">
                <div class="font-weight-medium">第二步：面对摄像头</div>
                <div class="text-caption">确保面部在摄像头中清晰可见，光线充足</div>
              </v-timeline-item>
              
              <v-timeline-item color="success">
                <div class="font-weight-medium">第三步：进行考勤</div>
                <div class="text-caption">点击"考勤打卡"按钮，系统将自动进行活体检测和人脸识别</div>
              </v-timeline-item>
            </v-timeline>
            
            <v-alert
              dense
              type="info"
              border="left"
              class="mt-3 rounded-lg"
              elevation="2"
            >
              <div class="font-weight-medium">当前活体检测方法</div>
              <div class="custom-tag mt-1">{{ getCurrentLivenessMethodName() }}</div>
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex';

export default {
  name: 'Attendance',
  data: () => ({
    cameraStarted: false,
    detectionResult: null,
    recognitionResult: null,
    livenessMethods: [
      { text: '眨眼检测', value: 'blink' },
      { text: '深度学习', value: 'deep_learning' },
      { text: '改进多模态', value: 'improved' },
      { text: '第三方API', value: 'api' }
    ]
  }),
  computed: {
    ...mapState(['livenessMethod']),
    ...mapGetters(['isLoading'])
  },
  methods: {
    ...mapMutations(['SET_ERROR']),
    ...mapActions(['detectLiveness', 'recognizeFace', 'setLivenessMethod']),
    
    startCamera() {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
          .then(stream => {
            this.$refs.video.srcObject = stream;
            this.cameraStarted = true;
            this.SET_ERROR(null);
          })
          .catch(err => {
            this.SET_ERROR(`启动摄像头失败: ${err.message}`);
            console.error('启动摄像头失败', err);
          });
      } else {
        this.SET_ERROR('您的浏览器不支持摄像头访问');
      }
    },
    
    stopCamera() {
      if (this.cameraStarted && this.$refs.video.srcObject) {
        const tracks = this.$refs.video.srcObject.getTracks();
        tracks.forEach(track => track.stop());
        this.$refs.video.srcObject = null;
        this.cameraStarted = false;
      }
    },
    
    captureImage() {
      // 在画布上绘制视频当前帧
      const video = this.$refs.video;
      const canvas = this.$refs.canvas;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      
      // 获取数据URL
      return canvas.toDataURL('image/jpeg');
    },
    
    async performLivenessCheck(imageData) {
      try {
        const result = await this.detectLiveness({
          image: imageData,
          method: this.livenessMethod
        });
        return result;
      } catch (error) {
        console.error("活体检测执行失败", error);
        this.SET_ERROR(`活体检测失败: ${error.message}`);
        return { is_live: false, message: "检测失败", confidence: 0 };
      }
    },
    
    async testLivenessDetection() {
      // 清除之前的结果
      this.detectionResult = null;
      this.recognitionResult = null;
      
      if (!this.cameraStarted) {
        this.SET_ERROR('请先启动摄像头');
        return;
      }
      
      try {
        const imageData = this.captureImage();
        console.log("开始活体检测测试");
        const result = await this.performLivenessCheck(imageData);
        console.log("活体检测结果:", result);
        this.detectionResult = result;
        
        // 添加成功动画效果，如果检测成功
        if (result.is_live) {
          this.playSuccessSound();
        } else {
          this.playErrorSound();
        }
      } catch (error) {
        console.error("活体检测测试失败", error);
        this.SET_ERROR(`活体检测测试失败: ${error.message}`);
      }
    },
    
    async captureAndRecognize() {
      // 清除之前的结果
      this.detectionResult = null;
      this.recognitionResult = null;
      
      if (!this.cameraStarted) {
        this.SET_ERROR('请先启动摄像头');
        return;
      }
      
      try {
        const imageData = this.captureImage();
        console.log("开始考勤打卡流程");
        
        // 先进行活体检测
        console.log("执行活体检测");
        const livenessResult = await this.performLivenessCheck(imageData);
        console.log("活体检测结果:", livenessResult);
        this.detectionResult = livenessResult;
        
        if (!livenessResult.is_live) {
          this.SET_ERROR('活体检测失败，无法进行考勤');
          this.playErrorSound();
          return;
        }
        
        // 通过活体检测后进行人脸识别
        console.log("开始人脸识别");
        const recognitionResult = await this.recognizeFace(imageData);
        console.log("人脸识别结果:", recognitionResult);
        this.recognitionResult = recognitionResult;
        
        // 添加成功动画效果，如果识别成功
        if (recognitionResult.success) {
          this.playSuccessSound();
        } else {
          this.playErrorSound();
        }
      } catch (error) {
        console.error("考勤打卡流程失败", error);
        this.SET_ERROR(`考勤打卡失败: ${error.message}`);
      }
    },
    
    updateLivenessMethod(method) {
      this.setLivenessMethod(method);
    },
    
    playSuccessSound() {
      try {
        // 添加成功音效
        const audio = new Audio();
        audio.src = require('@/assets/success.mp3');
        audio.play().catch(e => console.error('成功音频播放失败', e));
      } catch (error) {
        console.error("播放成功音效失败", error);
      }
    },
    
    playErrorSound() {
      try {
        // 添加失败音效
        const audio = new Audio();
        audio.src = require('@/assets/error.mp3');
        audio.play().catch(e => console.error('错误音频播放失败', e));
      } catch (error) {
        console.error("播放错误音效失败", error);
      }
    },
    
    getSimilarityColor(similarity) {
      if (similarity > 0.8) return 'success';
      if (similarity > 0.6) return 'warning';
      return 'error';
    },
    
    getCurrentLivenessMethodName() {
      const method = this.livenessMethods.find(m => m.value === this.livenessMethod);
      return method ? method.text : '未知方法';
    }
  },
  mounted() {
    // 初始化时从store获取活体检测方法
    console.log("Attendance组件加载，当前活体检测方法:", this.$store.state.livenessMethod);
  },
  beforeDestroy() {
    // 组件销毁前关闭摄像头
    this.stopCamera();
  }
}
</script>

<style scoped>
.attendance {
  animation: fadeIn 0.5s ease-out;
  position: relative;
  padding: 16px;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.primary-gradient {
  background: linear-gradient(135deg, #1976d2 0%, #2196f3 100%) !important;
  border-radius: 24px !important;
  overflow: hidden;
}

.result-card {
  background-color: rgba(255, 255, 255, 0.95) !important;
  border-radius: 24px !important;
}

.guide-card {
  background-color: rgba(255, 255, 255, 0.95) !important;
  border-radius: 24px !important;
}

.menu-list {
  background-color: white !important;
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
  overflow: hidden;
}

.no-result-box {
  background-color: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.camera-container {
  position: relative;
  border-radius: 24px !important;
  overflow: hidden;
  height: 400px;
  background-color: #000;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.camera-container:hover {
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25);
  transform: translateY(-5px);
}

.camera-container video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.camera-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 24px;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 24px;
}

.success-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  animation: fadeInOut 3s forwards;
  color: white;
  border-radius: 24px;
}

@keyframes fadeInOut {
  0% { opacity: 0; }
  20% { opacity: 1; }
  80% { opacity: 1; }
  100% { opacity: 0; display: none; }
}

.loading-text {
  font-size: 18px;
  color: white;
  margin-bottom: 8px;
}

.face-frame {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 250px;
  height: 250px;
  transform: translate(-50%, -50%);
  border: 2px dashed rgba(255, 255, 255, 0.7);
  border-radius: 50%;
  box-shadow: 0 0 0 2000px rgba(0, 0, 0, 0.3);
  animation: pulse-border 2s infinite;
}

@keyframes pulse-border {
  0% {
    box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.3);
    border-color: rgba(255, 255, 255, 0.5);
  }
  70% {
    box-shadow: 0 0 0 2000px rgba(0, 0, 0, 0.4);
    border-color: rgba(255, 255, 255, 0.9);
  }
  100% {
    box-shadow: 0 0 0 2000px rgba(0, 0, 0, 0.3);
    border-color: rgba(255, 255, 255, 0.5);
  }
}

.action-buttons {
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.result-alert {
  transition: all 0.3s ease;
  animation: slideInRight 0.5s ease-out;
  border-radius: 16px !important;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.animated-chip {
  animation: bounce 1s ease infinite;
  border-radius: 20px !important;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.loading-wave .dot {
  background-color: white;
  width: 8px;
  height: 8px;
  margin: 0 4px;
  border-radius: 50%;
  display: inline-block;
  animation: wave 1.3s linear infinite;
}

.custom-tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  background-color: rgba(33, 150, 243, 0.2);
  color: #1976d2;
  border-radius: 16px;
  font-weight: 500;
  font-size: 0.9rem;
  border: 1px solid rgba(33, 150, 243, 0.3);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.theme--dark .custom-tag {
  background-color: rgba(33, 150, 243, 0.3);
  color: #90caf9;
  border: 1px solid rgba(144, 202, 249, 0.3);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* 深色模式适配 */
.theme--dark .result-card,
.theme--dark .guide-card {
  background-color: #1E1E1E !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
}

.theme--dark .no-result-box {
  background-color: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.theme--dark .primary-gradient {
  background: linear-gradient(135deg, #0d47a1 0%, #1976d2 100%) !important;
}

.theme--dark .result-alert {
  background-color: rgba(0, 0, 0, 0.3) !important;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.theme--dark .loading-overlay,
.theme--dark .camera-overlay,
.theme--dark .success-overlay {
  background: rgba(0, 0, 0, 0.7);
}

.theme--dark .v-alert {
  border: 1px solid rgba(255, 255, 255, 0.05) !important;
}

.theme--dark .loading-wave .dot {
  background-color: #90caf9;
}

.theme--dark .menu-list {
  background-color: #1E1E1E !important;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
}
</style> 