<template>
  <v-app>
    <!-- 背景图案 -->
    <div class="bg-pattern"></div>
    
    <v-app-bar app color="primary" dark elevation="3" class="app-bar-solid" rounded="0">
      <v-app-bar-nav-icon @click="drawer = !drawer" class="btn-pulse"></v-app-bar-nav-icon>
      <v-toolbar-title class="font-weight-bold pl-1">
        <span class="title-animation">人脸识别考勤系统</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      
      <v-scale-transition>
        <v-badge 
          v-if="$store.state.error" 
          dot 
          color="error" 
          class="mx-3"
        >
          <v-btn icon @click="showErrorDialog = true" class="btn-pulse">
            <v-icon>mdi-alert-circle</v-icon>
          </v-btn>
        </v-badge>
      </v-scale-transition>
      
      <v-btn icon @click="toggleDarkMode" class="btn-pulse">
        <v-icon>{{ isDarkMode ? 'mdi-white-balance-sunny' : 'mdi-weather-night' }}</v-icon>
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer 
      v-model="drawer" 
      app 
      temporary 
      :class="isDarkMode ? 'solid-card-dark' : 'solid-card'"
      width="280"
      rounded="0 16px 16px 0"
    >
      <v-list-item class="my-4">
        <v-list-item-avatar class="avatar-circle" size="54">
          <v-img src="@/assets/logo.png"></v-img>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title class="text-h6">人脸识别考勤系统</v-list-item-title>
          <v-list-item-subtitle class="mt-1">班级考勤管理</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-divider class="mx-4 mb-2"></v-divider>

      <v-list dense nav rounded>
        <v-list-item 
          v-for="item in menuItems" 
          :key="item.title" 
          :to="item.path" 
          link
          class="my-2 menu-item mx-2"
          rounded="pill"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      
      <template v-slot:append>
        <div class="pa-4">
          <v-btn 
            block 
            color="primary" 
            class="btn-pulse" 
            rounded 
            elevation="2"
            @click="drawer = false"
          >
            <v-icon left>mdi-arrow-left</v-icon>
            关闭菜单
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <v-main class="main-content">
      <!-- 全局加载动画 -->
      <v-overlay :value="isLoading" :opacity="0.8" color="white">
        <div class="loading-container">
          <div class="loading-wave mb-2">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
          </div>
          <div class="loading-text">正在加载...</div>
        </div>
      </v-overlay>
      
      <!-- 错误提示对话框 -->
      <v-dialog v-model="showErrorDialog" max-width="400" rounded="lg">
        <v-card class="error-dialog rounded-lg" rounded="lg">
          <v-card-title class="headline">
            <v-icon color="error" class="mr-2">mdi-alert-circle</v-icon>
            出现错误
          </v-card-title>
          <v-card-text>
            {{ $store.state.error }}
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn 
              color="error" 
              text 
              @click="clearError" 
              class="btn-pulse"
              rounded
            >
              确定
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      
      <!-- 成功提示 -->
      <v-snackbar
        v-model="showSuccessSnackbar"
        :timeout="3000"
        color="success"
        top
        rounded="pill"
        class="success-snackbar"
      >
        <v-icon left>mdi-check-circle</v-icon>
        {{ $store.state.success }}
        <template v-slot:action="{ attrs }">
          <v-btn
            icon
            v-bind="attrs"
            @click="clearSuccess"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </template>
      </v-snackbar>
      
      <v-container fluid class="px-4 py-2">
        <transition name="page" mode="out-in">
          <router-view></router-view>
        </transition>
      </v-container>
    </v-main>

    <v-footer app :class="isDarkMode ? 'footer-solid-dark' : 'footer-solid'" class="px-4" rounded="0">
      <div>
        <span>&copy; {{ new Date().getFullYear() }} - 人脸识别考勤系统</span>
        <span class="ml-2 text-caption">版本 1.0.0</span>
      </div>
      <v-spacer></v-spacer>
      <div>
        <v-btn 
          icon 
          x-small 
          :color="isOnline ? 'success' : 'error'" 
          class="mr-2"
        >
          <v-icon>
            {{ isOnline ? 'mdi-cloud-check' : 'mdi-cloud-off-outline' }}
          </v-icon>
        </v-btn>
        <span class="text-caption">
          {{ isOnline ? '已连接' : '未连接' }}
        </span>
      </div>
    </v-footer>
  </v-app>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex';

export default {
  name: 'App',
  data: () => ({
    drawer: false,
    isDarkMode: false,
    showErrorDialog: false,
    showSuccessSnackbar: false,
    isOnline: true,
    menuItems: [
      { title: '首页', path: '/', icon: 'mdi-home' },
      { title: '考勤打卡', path: '/attendance', icon: 'mdi-account-check' },
      { title: '人脸注册', path: '/register', icon: 'mdi-account-plus' },
      { title: '考勤记录', path: '/records', icon: 'mdi-clipboard-text' },
      { title: '班级管理', path: '/classes', icon: 'mdi-account-group' },
      { title: '系统设置', path: '/settings', icon: 'mdi-cog' }
    ]
  }),
  computed: {
    ...mapGetters(['isLoading'])
  },
  methods: {
    ...mapMutations(['SET_ERROR', 'SET_SUCCESS']),
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      this.$vuetify.theme.dark = this.isDarkMode;
      // 保存设置到本地存储
      localStorage.setItem('darkMode', this.isDarkMode);
    },
    clearError() {
      this.showErrorDialog = false;
      this.SET_ERROR(null);
    },
    clearSuccess() {
      this.showSuccessSnackbar = false;
      this.SET_SUCCESS(null);
    },
    checkOnlineStatus() {
      this.isOnline = navigator.onLine;
    }
  },
  created() {
    // 从本地存储加载深色模式设置
    const savedDarkMode = localStorage.getItem('darkMode');
    if (savedDarkMode !== null) {
      this.isDarkMode = JSON.parse(savedDarkMode);
      this.$vuetify.theme.dark = this.isDarkMode;
    }
    
    // 监听在线状态变化
    window.addEventListener('online', this.checkOnlineStatus);
    window.addEventListener('offline', this.checkOnlineStatus);
    this.checkOnlineStatus();
  },
  beforeDestroy() {
    // 移除事件监听器
    window.removeEventListener('online', this.checkOnlineStatus);
    window.removeEventListener('offline', this.checkOnlineStatus);
  },
  watch: {
    '$store.state.error'(newVal) {
      if (newVal) {
        this.showErrorDialog = true;
      }
    },
    '$store.state.success'(newVal) {
      if (newVal) {
        this.showSuccessSnackbar = true;
      }
    }
  }
};
</script>

<style>
.bg-pattern {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: var(--v-background-base, #f5f5f5);
  background-image: 
    radial-gradient(circle at 25px 25px, rgba(0, 0, 0, 0.05) 2%, transparent 0%),
    radial-gradient(circle at 75px 75px, rgba(0, 0, 0, 0.05) 2%, transparent 0%);
  background-size: 100px 100px;
  z-index: -1;
}

.main-content {
  position: relative;
  background-color: transparent;
}

.v-application.theme--dark .bg-pattern {
  background-color: var(--v-background-base, #121212);
  background-image: 
    radial-gradient(circle at 25px 25px, rgba(255, 255, 255, 0.07) 2%, transparent 0%),
    radial-gradient(circle at 75px 75px, rgba(255, 255, 255, 0.07) 2%, transparent 0%);
}

.success-snackbar {
  font-weight: 500;
}

.menu-item {
  transition: all 0.3s ease;
  border-radius: 30px !important;
  margin: 4px 8px !important;
}

.menu-item:hover {
  background-color: rgba(33, 150, 243, 0.1);
  transform: translateX(5px);
}

.menu-item.v-item--active {
  background-color: rgba(33, 150, 243, 0.15);
  font-weight: bold;
}

.title-animation {
  background: linear-gradient(45deg, #ffffff, rgba(255, 255, 255, 0.7));
  background-size: 200% auto;
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shine 3s linear infinite;
}

@keyframes shine {
  to {
    background-position: 200% center;
  }
}

.error-dialog {
  overflow: hidden;
  border: 1px solid rgba(244, 67, 54, 0.2);
}

.loading-container {
  text-align: center;
  background-color: white;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.loading-text {
  margin-top: 16px;
  font-size: 16px;
  font-weight: 500;
  color: #1976d2;
}

/* 页面切换动画 */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* 纯色背景样式 */
.app-bar-solid {
  background-color: #1976d2 !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
}

.solid-card {
  background-color: white !important;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1) !important;
}

.solid-card-dark {
  background-color: #1E1E1E !important;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.3) !important;
}

.footer-solid {
  background-color: #f5f5f5 !important;
  border-top: 1px solid #e0e0e0 !important;
}

.footer-solid-dark {
  background-color: #1E1E1E !important;
  border-top: 1px solid #333333 !important;
}

/* 暗黑模式全局样式优化 */
.theme--dark.v-application {
  background-color: #121212;
  color: #e0e0e0;
}

.theme--dark .v-card {
  background-color: #1E1E1E !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
}

.theme--dark .v-card.detection-card {
  background-color: #2c2c2c !important;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.theme--dark .v-card.detection-card:hover {
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4) !important;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.theme--dark .v-list {
  background-color: #1E1E1E !important;
}

.theme--dark .v-tabs {
  background-color: #1E1E1E !important;
}

.theme--dark .custom-tag {
  background-color: rgba(33, 150, 243, 0.3);
  color: #90caf9;
}

.theme--dark .v-alert.result-alert {
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.theme--dark .loading-container {
  background-color: #1E1E1E;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.theme--dark .loading-text {
  color: #90caf9;
}
</style> 