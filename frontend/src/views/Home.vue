<template>
  <div class="home">
    <v-row>
      <v-col cols="12">
        <v-card elevation="4" class="gradient-bg">
          <v-card-title class="headline white--text py-4">
            <v-icon large left color="white" class="mr-2">mdi-face-recognition</v-icon>
            基于人脸识别与活体检测的班级考勤系统
          </v-card-title>
          <v-card-text class="pa-5 white--text">
            <p class="text-h6 mb-3 animate-typing">欢迎使用班级考勤系统</p>
            <p>本系统采用先进的人脸识别与活体检测技术，能够准确识别学生身份并防止考勤作弊。</p>
            <div class="text-center mt-4">
              <v-btn 
                color="white" 
                class="btn-pulse primary--text" 
                large 
                to="/attendance"
                rounded
                elevation="2"
              >
                <v-icon left>mdi-account-check</v-icon>
                开始考勤
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-6">
      <v-col cols="12" md="4">
        <v-card height="100%" class="hover-card rounded-lg" elevation="4">
          <v-card-title class="secondary white--text rounded-t-lg">
            <v-icon left dark>mdi-account-check</v-icon>
            考勤打卡
          </v-card-title>
          <v-card-text class="pa-4 pt-6">
            <p>使用摄像头进行人脸识别考勤打卡，支持多种活体检测方式防止欺骗攻击。</p>
            <v-chip class="mt-2" color="primary" small outlined pill>安全可靠</v-chip>
            <v-chip class="mt-2 ml-2" color="success" small outlined pill>高效准确</v-chip>
          </v-card-text>
          <v-card-actions class="pa-4 pt-0">
            <v-spacer></v-spacer>
            <v-btn color="primary" rounded class="btn-pulse" to="/attendance" elevation="1">
              去打卡
              <v-icon right>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card height="100%" class="hover-card rounded-lg" elevation="4">
          <v-card-title class="secondary white--text rounded-t-lg">
            <v-icon left dark>mdi-account-plus</v-icon>
            人脸注册
          </v-card-title>
          <v-card-text class="pa-4 pt-6">
            <p>为新学生注册人脸信息，以便系统能够正确识别学生身份。</p>
            <v-chip class="mt-2" color="info" small outlined pill>简单便捷</v-chip>
            <v-chip class="mt-2 ml-2" color="warning" small outlined pill>快速注册</v-chip>
          </v-card-text>
          <v-card-actions class="pa-4 pt-0">
            <v-spacer></v-spacer>
            <v-btn color="primary" rounded class="btn-pulse" to="/register" elevation="1">
              去注册
              <v-icon right>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card height="100%" class="hover-card rounded-lg" elevation="4">
          <v-card-title class="secondary white--text rounded-t-lg">
            <v-icon left dark>mdi-clipboard-text</v-icon>
            考勤记录
          </v-card-title>
          <v-card-text class="pa-4 pt-6">
            <p>查看和导出考勤记录，掌握学生出勤情况，便于班级管理。</p>
            <v-chip class="mt-2" color="success" small outlined pill>可导出</v-chip>
            <v-chip class="mt-2 ml-2" color="primary" small outlined pill>易管理</v-chip>
          </v-card-text>
          <v-card-actions class="pa-4 pt-0">
            <v-spacer></v-spacer>
            <v-btn color="primary" rounded class="btn-pulse" to="/records" elevation="1">
              查看记录
              <v-icon right>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-6">
      <v-col cols="12">
        <v-card class="rounded-xl" elevation="4">
          <v-card-title class="primary--text">
            <v-icon left color="primary" class="mr-2">mdi-shield-account</v-icon>
            活体检测技术
          </v-card-title>
          <v-card-text class="pa-4">
            <p class="mb-4">本系统集成了多种不同的活体检测方案，有效防止照片和视频攻击：</p>
            
            <v-row>
              <v-col cols="12" md="4" v-for="(tech, index) in technologies" :key="index">
                <v-card class="rounded-lg detection-card" elevation="2">
                  <div class="detection-icon-wrapper">
                    <v-icon size="36" :color="tech.color">{{ tech.icon }}</v-icon>
                  </div>
                  <v-card-title class="py-2 justify-center">{{ tech.title }}</v-card-title>
                  <v-card-text class="py-2 text-center">
                    {{ tech.description }}
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-6 mb-6">
      <v-col cols="12">
        <v-card class="wave-border" elevation="4">
          <v-card-title class="primary--text">系统特点</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6" md="3" v-for="(feature, i) in features" :key="i">
                <div class="feature-item text-center pa-3">
                  <v-avatar size="64" :color="feature.color" class="white--text mb-4 elevation-2">
                    <v-icon large>{{ feature.icon }}</v-icon>
                  </v-avatar>
                  <h3 class="subtitle-1 font-weight-bold">{{ feature.title }}</h3>
                  <p class="caption mt-2">{{ feature.text }}</p>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data: () => ({
    technologies: [
      { 
        title: '眨眼检测', 
        description: '通过检测用户的眨眼动作来判断是否为真人，有效防止照片攻击', 
        icon: 'mdi-eye', 
        color: 'primary' 
      },
      { 
        title: '深度学习分析', 
        description: '基于深度学习的纹理分析，能够区分真实人脸与照片，防止欺骗', 
        icon: 'mdi-brain', 
        color: 'purple' 
      },
      { 
        title: '多模态活体检测', 
        description: '结合多种检测手段，提供更高精度的活体验证，全面防护安全', 
        icon: 'mdi-shield-check', 
        color: 'success' 
      }
    ],
    features: [
      { title: '快速识别', text: '亚秒级人脸识别', icon: 'mdi-clock-fast', color: 'primary' },
      { title: '多重安全', text: '防欺骗检测机制', icon: 'mdi-security', color: 'error' },
      { title: '便捷管理', text: '考勤数据可视化', icon: 'mdi-chart-bar', color: 'success' },
      { title: '易于部署', text: '简单快捷的配置', icon: 'mdi-cog', color: 'warning' }
    ]
  })
}
</script>

<style scoped>
.home {
  position: relative;
  animation: fadeIn 0.5s ease-out;
  padding: 8px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.gradient-bg {
  background: linear-gradient(135deg, #1976d2 0%, #6fa8dc 50%, #8e7cc3 100%) !important;
  border-radius: 24px !important;
  overflow: hidden;
}

.rounded-t-lg {
  border-top-left-radius: 16px !important;
  border-top-right-radius: 16px !important;
}

.rounded-xl {
  border-radius: 20px !important;
}

.animate-typing {
  overflow: hidden;
  white-space: nowrap;
  border-right: 3px solid white;
  animation: typing 3.5s steps(30) 1s 1 normal both,
             blinking 1s steps(1) infinite;
  width: fit-content;
}

@keyframes typing {
  from { width: 0; }
  to { width: 250px; }
}

@keyframes blinking {
  0%, 100% { border-color: transparent; }
  50% { border-color: white; }
}

.detection-card {
  transition: all 0.3s ease;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.95) !important;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.detection-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1) !important;
  border: 1px solid rgba(0, 0, 0, 0.09);
}

.detection-icon-wrapper {
  display: flex;
  justify-content: center;
  padding-top: 20px;
}

.feature-item {
  transition: all 0.3s ease;
  border-radius: 16px;
  padding: 16px;
  background-color: rgba(255, 255, 255, 0.6);
}

.feature-item:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
}

/* 自定义按钮悬停效果 */
.v-btn.theme--light.v-btn--outlined {
  border: thin solid currentColor;
}

.v-btn.theme--light.v-btn--outlined:hover {
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.2);
}

/* 增加卡片的阴影效果 */
.v-card {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.v-card:hover {
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.15), 0 10px 10px rgba(0, 0, 0, 0.10) !important;
}
</style> 