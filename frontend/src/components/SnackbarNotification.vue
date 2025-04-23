<template>
  <v-snackbar
    v-model="show"
    :color="color"
    :timeout="timeout"
    :position="position"
    class="notification-snackbar"
    elevation="6"
    rounded="pill"
  >
    <div class="d-flex align-center">
      <v-icon :icon="icon" class="mr-3" />
      <span>{{ message }}</span>
    </div>
    <template v-slot:actions>
      <v-btn
        variant="text"
        @click="closeSnackbar"
      >
        关闭
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
export default {
  name: 'SnackbarNotification',
  props: {
    value: {
      type: Boolean,
      default: false
    },
    message: {
      type: String,
      default: ''
    },
    color: {
      type: String,
      default: 'success'
    },
    timeout: {
      type: Number,
      default: 3000
    },
    position: {
      type: String,
      default: 'top'
    },
    playSound: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      show: false,
      audio: null
    }
  },
  computed: {
    icon() {
      switch(this.color) {
        case 'success':
          return 'mdi-check-circle'
        case 'error':
          return 'mdi-alert-circle'
        case 'info':
          return 'mdi-information'
        case 'warning':
          return 'mdi-alert'
        default:
          return 'mdi-bell'
      }
    }
  },
  watch: {
    value(newVal) {
      this.show = newVal
      if (newVal && this.playSound) {
        this.playNotificationSound()
      }
    },
    show(newVal) {
      if (!newVal) {
        this.$emit('input', false)
      }
    }
  },
  mounted() {
    this.initAudio()
  },
  methods: {
    closeSnackbar() {
      this.show = false
    },
    initAudio() {
      // 预加载音频文件
      try {
        this.audio = {
          success: new Audio('/src/assets/sounds/success.mp3'),
          error: new Audio('/src/assets/sounds/error.mp3'),
          info: new Audio('/src/assets/sounds/info.mp3')
        }
        
        // 预加载
        Object.values(this.audio).forEach(audio => {
          audio.load()
          audio.volume = 0.5 // 设置音量
        })
      } catch (error) {
        console.error('初始化音频失败:', error)
      }
    },
    playNotificationSound() {
      try {
        if (!this.audio) {
          return
        }
        
        const soundType = this.color in this.audio ? this.color : 'info'
        const sound = this.audio[soundType]
        
        if (sound) {
          sound.currentTime = 0 // 重置音频
          sound.play().catch(error => {
            console.warn('播放音频失败:', error)
          })
        }
      } catch (error) {
        console.error('播放音频失败:', error)
      }
    }
  }
}
</script>

<style scoped>
.notification-snackbar {
  border-radius: 8px;
  transition: all 0.3s ease;
}
</style> 