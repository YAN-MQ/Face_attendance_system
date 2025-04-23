<template>
  <div class="attendance">
    <v-row>
      <v-col cols="12">
        <v-card elevation="2">
          <v-card-title class="headline">
            <v-icon left>mdi-account-check</v-icon>
            考勤打卡
          </v-card-title>
          
          <v-card-text>
            <v-row>
              <v-col cols="12" md="8">
                <div class="camera-container">
                  <video ref="video" width="100%" autoplay playsinline></video>
                  <canvas ref="canvas" style="display: none;"></canvas>
                  
                  <div class="camera-overlay" v-if="!cameraStarted">
                    <v-btn color="primary" @click="startCamera">
                      <v-icon left>mdi-camera</v-icon>
                      启动摄像头
                    </v-btn>
                  </div>
                  
                  <div v-if="isLoading" class="loading-overlay">
                    <v-progress-circular indeterminate color="primary"></v-progress-circular>
                    <div class="mt-2">处理中...</div>
                  </div>
                </div>
                
                <div class="mt-4 text-center">
                  <v-btn color="primary" large @click="captureAndRecognize" :disabled="!cameraStarted || isLoading">
                    <v-icon left>mdi-account-check</v-icon>
                    考勤打卡
                  </v-btn>
                  
                  <v-btn class="ml-4" color="warning" @click="testLiveness" :disabled="!cameraStarted || isLoading">
                    <v-icon left>mdi-shield-account</v-icon>
                    仅测试活体
                  </v-btn>
                </div>
              </v-col>
              
              <v-col cols="12" md="4">
                <v-card outlined class="mb-4">
                  <v-card-title>
                    <v-icon left>mdi-cog</v-icon>
                    活体检测方式
                  </v-card-title>
                  <v-card-text>
                    <v-radio-group v-model="livenessMethod" @change="updateLivenessMethod">
                      <v-radio label="眨眼检测" value="blink"></v-radio>
                      <v-radio label="深度学习" value="deep_learning"></v-radio>
                      <v-radio label="API检测" value="api"></v-radio>
                    </v-radio-group>
                  </v-card-text>
                </v-card>
                
                <v-card outlined v-if="detectionResult">
                  <v-card-title :class="detectionResult.is_live ? 'success white--text' : 'error white--text'">
                    检测结果
                  </v-card-title>
                  <v-card-text>
                    <p><strong>状态:</strong> {{ detectionResult.is_live ? '真实人脸' : '非真实人脸' }}</p>
                    <p><strong>置信度:</strong> {{ (detectionResult.confidence * 100).toFixed(2) }}%</p>
                    <p><strong>消息:</strong> {{ detectionResult.message }}</p>
                  </v-card-text>
                </v-card>
                
                <v-card outlined v-if="recognitionResult" class="mt-4">
                  <v-card-title :class="recognitionResult.success ? 'success white--text' : 'error white--text'">
                    识别结果
                  </v-card-title>
                  <v-card-text>
                    <p><strong>学号:</strong> {{ recognitionResult.student_id }}</p>
                    <p><strong>姓名:</strong> {{ recognitionResult.student_name }}</p>
                    <p><strong>相似度:</strong> {{ (recognitionResult.similarity * 100).toFixed(2) }}%</p>
                    <p><strong>时间:</strong> {{ recognitionResult.timestamp }}</p>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Attendance',
  data: () => ({
    cameraStarted: false,
    stream: null,
    detectionResult: null,
    recognitionResult: null,
    livenessMethod: 'blink', // 默认使用眨眼检测
  }),
  computed: {
    ...mapGetters([
      'isLoading',
      'error',
      'lastDetectionResult'
    ])
  },
  methods: {
    ...mapActions([
      'detectLiveness',
      'recognizeFace',
      'setLivenessMethod'
    ]),
    async startCamera() {
      try {
        // 请求摄像头权限
        this.stream = await navigator.mediaDevices.getUserMedia({ 
          video: { facingMode: "user" }, // 使用前置摄像头
          audio: false 
        });
        
        // 将视频流绑定到video元素
        this.$refs.video.srcObject = this.stream;
        this.cameraStarted = true;
      } catch (error) {
        console.error('无法访问摄像头:', error);
        this.$store.commit('SET_ERROR', '无法访问摄像头:' + error.message);
      }
    },
    stopCamera() {
      if (this.stream) {
        this.stream.getTracks().forEach(track => track.stop());
        this.cameraStarted = false;
        this.stream = null;
      }
    },
    captureImage() {
      const video = this.$refs.video;
      const canvas = this.$refs.canvas;
      
      // 设置canvas尺寸与视频一致
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      // 在canvas上绘制当前视频帧
      const context = canvas.getContext('2d');
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      
      // 获取图像的base64编码
      return canvas.toDataURL('image/jpeg');
    },
    async testLiveness() {
      // 清除之前的结果
      this.detectionResult = null;
      this.recognitionResult = null;
      
      if (!this.cameraStarted) {
        this.$store.commit('SET_ERROR', '请先启动摄像头');
        return;
      }
      
      const imageData = this.captureImage();
      const result = await this.detectLiveness(imageData);
      this.detectionResult = result;
    },
    async captureAndRecognize() {
      // 清除之前的结果
      this.detectionResult = null;
      this.recognitionResult = null;
      
      if (!this.cameraStarted) {
        this.$store.commit('SET_ERROR', '请先启动摄像头');
        return;
      }
      
      const imageData = this.captureImage();
      
      // 先进行活体检测
      const livenessResult = await this.detectLiveness(imageData);
      this.detectionResult = livenessResult;
      
      if (!livenessResult.is_live) {
        this.$store.commit('SET_ERROR', '活体检测失败，无法进行考勤');
        return;
      }
      
      // 通过活体检测后进行人脸识别
      const recognitionResult = await this.recognizeFace(imageData);
      this.recognitionResult = recognitionResult;
    },
    updateLivenessMethod(method) {
      this.setLivenessMethod(method);
    }
  },
  mounted() {
    // 初始化时从store获取活体检测方法
    this.livenessMethod = this.$store.getters.livenessMethod;
  },
  beforeDestroy() {
    // 组件销毁前关闭摄像头
    this.stopCamera();
  }
}
</script>

<style scoped>
.camera-container {
  position: relative;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  height: 400px;
  background-color: #000;
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
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.7);
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
}
</style> 