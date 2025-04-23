<template>
  <v-dialog
    v-model="dialog"
    max-width="600px"
    transition="scale-transition"
    overlay-opacity="0.8"
    @click:outside="closeDialog"
  >
    <v-card class="attendance-card glassmorphism">
      <!-- 成功时显示彩屑效果 -->
      <div class="confetti-container" v-if="showConfetti">
        <div 
          v-for="(confetti, index) in confettiItems" 
          :key="index"
          class="confetti-item"
          :style="getRandomConfettiStyle()"
        ></div>
      </div>

      <!-- 对话框标题 -->
      <v-card-title class="d-flex justify-space-between align-center pa-4">
        <span class="text-h5 font-weight-bold primary--text">
          {{ dialogTitle }}
        </span>
        <v-btn icon @click="closeDialog" class="btn-pulse">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <!-- 处理中状态 -->
      <v-card-text v-if="isProcessing" class="processing-container text-center py-5">
        <v-avatar size="100" color="primary" class="mb-4 pulse-animation">
          <v-icon size="64" color="white">mdi-account-check</v-icon>
        </v-avatar>
        <h2 class="text-h5 mb-3">{{ processingMessage }}</h2>
        <p class="text-body-1 text-medium-emphasis mb-4">{{ processingDescription }}</p>
        
        <!-- 波浪加载动画 -->
        <div class="loading-wave">
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
        </div>
      </v-card-text>

      <!-- 认证结果 -->
      <v-card-text v-else>
        <div class="flip-card" :class="{ 'flipped': showDetails }">
          <div class="flip-card-inner">
            <!-- 正面 - 学生基本信息 -->
            <div class="flip-card-front">
              <v-row align="center" justify="center">
                <v-col cols="12" sm="5" class="text-center">
                  <v-avatar size="120" class="mb-3">
                    <v-img
                      :src="attendanceInfo.student.avatar || 'https://cdn.vuetifyjs.com/images/john.jpg'"
                      alt="学生头像"
                      :class="{ 'pulse-animation': attendanceInfo.status === 'success' }"
                    ></v-img>
                  </v-avatar>
                  <div class="text-center">
                    <h3 class="student-name text-h5">{{ attendanceInfo.student.name }}</h3>
                    <p class="student-id text-body-2">学号: {{ attendanceInfo.student.id }}</p>
                  </div>
                </v-col>
                
                <v-col cols="12" sm="7">
                  <!-- 签到状态卡片 -->
                  <v-card 
                    flat 
                    :class="[
                      'pa-4 mb-4', 
                      attendanceInfo.status === 'success' ? 'success' : 
                      attendanceInfo.status === 'failure' ? 'error' : 
                      attendanceInfo.status === 'warning' ? 'warning' : 'info',
                      attendanceInfo.status === 'success' ? 'pulse-animation' : 
                      attendanceInfo.status === 'failure' ? 'shake-animation' : ''
                    ]"
                  >
                    <div class="d-flex align-center">
                      <v-icon left size="28" :color="statusColor">{{ statusIcon }}</v-icon>
                      <div>
                        <div class="text-h6">{{ statusMessage }}</div>
                        <div class="text-body-2">{{ statusDescription }}</div>
                      </div>
                    </div>
                  </v-card>
                  
                  <!-- 签到详情 -->
                  <div class="text-body-2 mb-2">
                    <v-icon small class="mr-1" color="primary">mdi-clock-outline</v-icon>
                    签到时间: {{ formattedTimestamp }}
                  </div>
                  <div class="text-body-2 mb-2">
                    <v-icon small class="mr-1" color="primary">mdi-map-marker-outline</v-icon>
                    签到位置: {{ attendanceInfo.location || '校内' }}
                  </div>
                  <div class="text-body-2 mb-2">
                    <v-icon small class="mr-1" color="primary">mdi-school-outline</v-icon>
                    课程: {{ attendanceInfo.course || '未知课程' }}
                  </div>
                  
                  <!-- 显示详情按钮 -->
                  <v-btn 
                    color="primary" 
                    text 
                    @click="toggleDetails" 
                    class="mt-2 btn-pulse"
                  >
                    查看技术详情
                    <v-icon right>mdi-arrow-right</v-icon>
                  </v-btn>
                </v-col>
              </v-row>
            </div>
            
            <!-- 背面 - 技术详情 -->
            <div class="flip-card-back">
              <div class="d-flex justify-space-between align-center mb-4">
                <h3 class="text-h6">技术详情</h3>
                <v-btn icon @click="toggleDetails" class="btn-pulse">
                  <v-icon>mdi-arrow-left</v-icon>
                </v-btn>
              </div>
              
              <v-list dense class="transparent">
                <v-list-item v-for="(score, key) in scoreDetails" :key="key" class="px-0">
                  <v-list-item-content>
                    <v-list-item-title>{{ getScoreLabel(key) }}</v-list-item-title>
                    <v-list-item-subtitle>
                      <v-progress-linear
                        :value="score * 100"
                        height="8"
                        rounded
                        :color="getConfidenceColor(score)"
                      ></v-progress-linear>
                      <span class="mt-1 d-inline-block">{{ (score * 100).toFixed(1) }}%</span>
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
              
              <v-divider class="my-3"></v-divider>
              
              <div class="text-body-2 mb-2">
                <span class="font-weight-medium">检测方法:</span> 
                {{ attendanceInfo.detectionMethod || '多模态活体检测' }}
              </div>
              <div class="text-body-2 mb-2">
                <span class="font-weight-medium">识别算法:</span> 
                {{ attendanceInfo.recognitionMethod || 'FaceNet' }}
              </div>
              <div class="text-body-2 mb-2">
                <span class="font-weight-medium">处理时间:</span> 
                {{ attendanceInfo.processingTime || '1.2' }}s
              </div>
            </div>
          </div>
        </div>
      </v-card-text>

      <!-- 操作按钮 -->
      <v-card-actions class="pa-4 pt-0">
        <v-spacer></v-spacer>
        <v-btn 
          color="grey darken-1" 
          text 
          @click="closeDialog" 
          class="btn-pulse"
        >
          关闭
        </v-btn>
        <v-btn 
          color="primary" 
          :disabled="attendanceInfo.status === 'processing'"
          @click="closeDialog" 
          class="btn-pulse"
        >
          确认
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { SoundManager } from '../utils/SoundManager';
import { mapState, mapActions } from 'vuex'

export default {
  name: 'AttendanceDialog',
  props: {
    attendanceInfo: {
      type: Object,
      default: () => ({
        student: {
          name: '',
          id: '',
          avatar: ''
        },
        status: 'processing',
        course: '',
        location: '',
        detectionMethod: '',
        recognitionMethod: '',
        processingTime: '',
        confidenceScore: 0,
        timestamp: '',
        livenessVerified: false
      })
    },
    dialog: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      showDetails: false,
      showConfetti: false,
      confettiItems: Array.from({ length: 50 }, (_, i) => i), // 50个彩屑元素
      confettiColors: [
        '#f44336', '#e91e63', '#9c27b0', 
        '#673ab7', '#3f51b5', '#2196f3', 
        '#03a9f4', '#00bcd4', '#009688', 
        '#4caf50', '#8bc34a', '#cddc39', 
        '#ffeb3b', '#ffc107', '#ff9800', 
        '#ff5722'
      ],
      processingMessage: '正在处理',
      processingDescription: '请稍等，正在验证您的身份...',
      showFront: true,
      soundManager: null
    }
  },
  computed: {
    isProcessing() {
      return this.attendanceInfo.status === 'processing';
    },
    dialogTitle() {
      switch(this.attendanceInfo.status) {
        case 'success': return '考勤成功';
        case 'failure': return '考勤失败';
        case 'warning': return '需要确认';
        default: return '正在处理';
      }
    },
    statusColor() {
      switch(this.attendanceInfo.status) {
        case 'success': return 'success';
        case 'failure': return 'error';
        case 'warning': return 'warning';
        default: return 'info';
      }
    },
    statusIcon() {
      switch(this.attendanceInfo.status) {
        case 'success': return 'mdi-check-circle';
        case 'failure': return 'mdi-alert-circle';
        case 'warning': return 'mdi-alert';
        default: return 'mdi-sync';
      }
    },
    statusMessage() {
      switch(this.attendanceInfo.status) {
        case 'success': return '考勤记录成功';
        case 'failure': return '考勤记录失败';
        case 'warning': return '需要人工确认';
        default: return '正在处理中...';
      }
    },
    statusDescription() {
      switch(this.attendanceInfo.status) {
        case 'success': return '已成功记录您的出勤';
        case 'failure': return '未能识别您的身份，请重试';
        case 'warning': return '系统无法确定，请联系管理员';
        default: return '请保持姿势，系统正在分析...';
      }
    },
    formattedTimestamp() {
      return this.attendanceInfo.timestamp ? new Date(this.attendanceInfo.timestamp).toLocaleString() : '未记录';
    },
    scoreDetails() {
      return {
        confidence: this.attendanceInfo.confidenceScore,
        liveness: this.attendanceInfo.livenessVerified ? 1 : 0,
        detection: this.attendanceInfo.detectionMethod ? 1 : 0,
        recognition: this.attendanceInfo.recognitionMethod ? 1 : 0
      };
    }
  },
  methods: {
    ...mapActions(['closeAttendanceDialog']),
    close() {
      this.showFront = true
      this.showDetails = false
      this.closeAttendanceDialog()
    },
    toggleDetails() {
      this.playSound('info');
      this.showDetails = !this.showDetails;
    },
    toggleCard() {
      this.playSound('info');
      this.showFront = !this.showFront;
    },
    closeDialog() {
      this.$emit('update:dialog', false);
    },
    playSound(type) {
      SoundManager.getInstance().play(type);
    },
    getRandomConfettiStyle() {
      const size = Math.random() * 10 + 5 + 'px';
      const color = this.confettiColors[Math.floor(Math.random() * this.confettiColors.length)];
      const rotation = Math.random() * 360 + 'deg';
      const left = Math.random() * 100 + '%';
      const fallDuration = Math.random() * 3 + 2 + 's';
      const fallDelay = Math.random() * 2 + 's';
      
      return {
        '--size': size,
        '--color': color,
        '--rotation': rotation,
        '--left': left,
        '--fall-duration': fallDuration,
        '--fall-delay': fallDelay
      };
    },
    getConfidenceColor(score) {
      if (score > 0.8) return 'success';
      if (score > 0.6) return 'primary';
      if (score > 0.4) return 'warning';
      return 'error';
    },
    getScoreLabel(key) {
      switch(key) {
        case 'confidence': return '识别置信度';
        case 'liveness': return '活体验证';
        case 'detection': return '检测方法';
        case 'recognition': return '识别算法';
        default: return key.charAt(0).toUpperCase() + key.slice(1);
      }
    }
  },
  watch: {
    dialog(newVal) {
      if (newVal) {
        // 播放考勤完成的音效
        if (this.attendanceInfo.status === 'success') {
          setTimeout(() => {
            this.showConfetti = true;
            this.playSound('success');
          }, 300);
        } else if (this.attendanceInfo.status === 'failure') {
          this.playSound('error');
        }
      }
    }
  },
  created() {
    // 初始化音效管理器
    this.soundManager = SoundManager.getInstance();
  }
}
</script>

<style scoped>
/* 基础样式 */
.attendance-card {
  position: relative;
  overflow: hidden;
  border-radius: 16px !important;
  transition: all 0.3s ease;
}

/* 状态颜色 */
.success {
  border-left: 4px solid #4CAF50;
}

.error {
  border-left: 4px solid #F44336;
}

.warning {
  border-left: 4px solid #FF9800;
}

.info {
  border-left: 4px solid #2196F3;
}

/* 学生信息样式 */
.student-name {
  font-weight: 600;
  margin: 12px 0 4px;
  letter-spacing: 0.5px;
}

.student-id {
  font-size: 0.9rem;
  opacity: 0.7;
  margin-bottom: 16px;
}

/* 翻转卡片效果 */
.flip-card {
  perspective: 1000px;
  width: 100%;
  min-height: 360px;
}

.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  transform-style: preserve-3d;
}

.flip-card-front,
.flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  padding: 20px;
}

.flip-card-front {
  transform: rotateY(0deg);
  z-index: 2;
}

.flip-card-back {
  transform: rotateY(180deg);
  z-index: 1;
}

.flipped .flip-card-inner {
  transform: rotateY(180deg);
}

/* 加载动画 */
.loading-wave {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  height: 50px;
  margin: 20px auto;
}

.loading-wave > div {
  background-color: var(--v-primary-base);
  height: 100%;
  width: 8px;
  margin: 0 3px;
  border-radius: 4px;
  animation: wave 1.2s infinite ease-in-out;
}

.loading-wave > div:nth-child(2) {
  animation-delay: -1.1s;
}

.loading-wave > div:nth-child(3) {
  animation-delay: -1.0s;
}

.loading-wave > div:nth-child(4) {
  animation-delay: -0.9s;
}

.loading-wave > div:nth-child(5) {
  animation-delay: -0.8s;
}

@keyframes wave {
  0%, 40%, 100% { 
    transform: scaleY(0.4);
  }
  20% { 
    transform: scaleY(1.0);
  }
}

/* 彩屑效果 */
.confetti-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 10;
  pointer-events: none;
}

.confetti-item {
  position: absolute;
  top: -20px;
  width: var(--size);
  height: var(--size);
  background-color: var(--color);
  border-radius: 2px;
  transform: rotate(var(--rotation));
  left: var(--left);
  animation: fall var(--fall-duration) var(--fall-delay) linear forwards;
}

@keyframes fall {
  0% {
    top: -20px;
    transform: translateY(0) rotate(var(--rotation));
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    top: 100%;
    transform: translateY(0) rotate(calc(var(--rotation) + 360deg));
    opacity: 0;
  }
}

/* 状态动画 */
.pulse-animation {
  animation: pulse 1.5s infinite;
}

.shake-animation {
  animation: shake 0.82s cubic-bezier(.36,.07,.19,.97) both;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.15);
    opacity: 0.8;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-3px, 0, 0); }
  40%, 60% { transform: translate3d(3px, 0, 0); }
}

/* 按钮效果 */
.btn-pulse {
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.btn-pulse:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.btn-pulse:before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.3s, height 0.3s;
}

.btn-pulse:hover:before {
  width: 200%;
  height: 200%;
}

.pulse-on-hover:hover {
  animation: pulse 1s;
}

/* 半透明列表 */
.transparent {
  background-color: transparent !important;
}

/* 处理容器 */
.processing-container {
  min-height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style> 