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
        <v-card class="rounded-xl main-section-card" elevation="4">
          <v-card-title class="primary--text tech-section-title">
            <v-icon left color="primary" size="32" class="mr-2">mdi-shield-account</v-icon>
            <span class="text-h5 font-weight-bold">活体检测技术</span>
          </v-card-title>
          <v-card-text class="pa-5">
            <p class="mb-5 subtitle-1 text-center grey--text text--darken-2">本系统集成了多种不同的活体检测方案，有效防止照片和视频攻击：</p>
            
            <v-row>
              <v-col cols="12" md="3" v-for="(tech, index) in technologies" :key="index">
                <div class="tech-card-wrapper">
                  <div class="tech-icon-circle" :class="`tech-icon-${tech.color}`">
                    <v-icon size="36" color="white">{{ tech.icon }}</v-icon>
                  </div>
                  
                  <v-hover v-slot="{ hover }">
                    <v-card 
                      class="rounded-lg tech-card" 
                      :class="[`tech-card-${tech.color}`, {'on-hover': hover}]" 
                      elevation="4"
                    >
                      <v-fade-transition>
                        <v-overlay
                          v-if="hover"
                          absolute
                          color="#121212"
                          opacity="0.8"
                          class="d-flex justify-center align-center tech-overlay"
                        >
                          <div class="text-center pa-5">
                            <p class="white--text mb-3">{{ tech.description }}</p>
                            <v-btn
                              :color="tech.color"
                              small
                              outlined
                              rounded
                              class="animated-btn"
                              @click.stop="openTechDetails(tech)"
                            >
                              <v-icon small left>mdi-information-outline</v-icon>
                              了解更多
                            </v-btn>
                          </div>
                        </v-overlay>
                      </v-fade-transition>
                      
                      <div style="height: 45px"></div> <!-- 为图标预留空间 -->
                      
                      <v-card-title class="justify-center pb-2">{{ tech.title }}</v-card-title>
                      <v-divider class="mx-4"></v-divider>
                      <v-card-text class="pa-4 text-center tech-description">
                        {{ tech.description }}
                        <div class="mt-3 keyword-chips">
                          <v-chip 
                            v-for="(keyword, k) in tech.keywords" 
                            :key="k" 
                            x-small 
                            outlined 
                            :color="tech.color" 
                            class="ma-1"
                          >
                            {{ keyword }}
                          </v-chip>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-hover>
                </div>
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
    
    <!-- 技术详情对话框 -->
    <v-dialog
      v-model="techDetailsDialog"
      max-width="700"
      scrollable
      transition="dialog-bottom-transition"
    >
      <v-card v-if="selectedTech" class="tech-details-card">
        <v-toolbar :color="selectedTech.color" dark flat>
          <v-btn icon @click="techDetailsDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title class="font-weight-bold">
            <v-icon left>{{ selectedTech.icon }}</v-icon>
            {{ selectedTech.title }}技术详情
          </v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
        
        <v-card-text class="pa-5">
          <v-row>
            <v-col cols="12" md="6">
              <v-img
                :src="selectedTech.detailImage || require('@/assets/logo.png')"
                height="200"
                class="rounded-lg"
                contain
              ></v-img>
            </v-col>
            
            <v-col cols="12" md="6">
              <h3 class="text-h6 mb-3 primary--text">技术介绍</h3>
              <p class="mb-4">{{ selectedTech.detailDescription }}</p>
              
              <v-chip-group column>
                <v-chip
                  v-for="(keyword, k) in selectedTech.keywords"
                  :key="k"
                  :color="selectedTech.color"
                  small
                  outlined
                  class="mr-2 mb-2"
                >
                  {{ keyword }}
                </v-chip>
              </v-chip-group>
            </v-col>
          </v-row>
          
          <v-divider class="my-4"></v-divider>
          
          <h3 class="text-h6 mb-3 primary--text">工作原理</h3>
          <p class="mb-5">{{ selectedTech.principle }}</p>
          
          <v-row>
            <v-col cols="12" md="6" v-for="(feature, i) in selectedTech.features" :key="i">
              <v-card outlined class="feature-card mb-3">
                <v-card-text>
                  <div class="d-flex align-center">
                    <v-avatar :color="selectedTech.color" size="36" class="mr-3">
                      <v-icon dark>{{ feature.icon }}</v-icon>
                    </v-avatar>
                    <div>
                      <div class="font-weight-bold">{{ feature.title }}</div>
                      <div class="text-caption">{{ feature.text }}</div>
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
          
          <v-alert 
            border="left" 
            :color="selectedTech.color" 
            class="mt-5" 
            elevation="2" 
            dense
          >
            <div class="font-weight-bold">应用场景</div>
            <p class="mb-0">{{ selectedTech.scenario }}</p>
          </v-alert>
        </v-card-text>
        
        <v-divider></v-divider>
        
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn 
            color="grey darken-1" 
            text 
            @click="techDetailsDialog = false"
          >
            关闭
          </v-btn>
          <v-btn 
            :color="selectedTech.color" 
            @click="techDetailsDialog = false"
          >
            我知道了
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data: () => ({
    techDetailsDialog: false,
    selectedTech: null,
    technologies: [
      { 
        title: '眨眼检测', 
        description: '通过检测用户的眨眼动作来判断是否为真人，有效防止照片攻击', 
        icon: 'mdi-eye', 
        color: 'primary',
        keywords: ['动作识别', '防照片攻击'],
        detailDescription: '眨眼检测技术是一种基于动作分析的活体检测技术，通过捕捉用户面部的自然眨眼动作来判断被检测对象是否为真实人脸。系统会实时监测双眼区域像素变化，识别自然的眨眼频率和特征，从而有效防止使用静态照片进行欺骗。',
        principle: '该技术通过面部特征点定位算法精确定位人眼区域，然后监测眼睛开合状态的变化。系统会分析连续视频帧中眼睛区域的形态变化，识别完整的眨眼动作序列，并结合时间因素判断眨眼行为是否符合自然人的特征。',
        features: [
          { title: '实时分析', text: '毫秒级响应的眨眼动作识别', icon: 'mdi-clock-fast' },
          { title: '低资源占用', text: '无需专用硬件，普通摄像头即可', icon: 'mdi-memory' },
          { title: '非侵入式', text: '用户无需执行特定指令，体验自然', icon: 'mdi-account-check' },
          { title: '防欺骗能力', text: '有效防止照片和视频回放攻击', icon: 'mdi-shield-check' }
        ],
        scenario: '适用于需要非接触式身份验证的场景，如考勤系统、门禁系统、移动设备解锁等。特别适合对用户体验要求较高的应用场景。'
      },
      { 
        title: '深度学习分析', 
        description: '基于深度学习的纹理分析，能够区分真实人脸与照片，防止欺骗', 
        icon: 'mdi-brain', 
        color: 'purple',
        keywords: ['AI算法', '纹理识别'],
        detailDescription: '深度学习分析技术利用先进的人工智能算法，通过对人脸图像进行多维度特征提取和分析，识别真实人脸与欺骗媒介（如照片、视频、3D面具等）之间的细微差异。该技术无需用户执行特定动作，可以在单一图像帧上完成检测。',
        principle: '系统采用深度卷积神经网络(CNN)对人脸图像进行分析，提取微纹理特征、颜色空间特征、频率域特征等多维信息。通过大规模数据训练，模型能够辨别真实人脸特有的光反射特性、纹理细节和颜色分布，从而区分真实人脸与欺骗媒介。',
        features: [
          { title: '高精度识别', text: '99.7%以上的识别准确率', icon: 'mdi-check-decagram' },
          { title: '多模态分析', text: '综合光学、纹理、颜色等多维特征', icon: 'mdi-layers-triple' },
          { title: '快速响应', text: '单帧图像即可完成检测', icon: 'mdi-flash' },
          { title: '适应性强', text: '适应不同光线条件和摄像设备', icon: 'mdi-white-balance-auto' }
        ],
        scenario: '适用于安全等级要求较高的场景，如银行身份验证、重要设施门禁、高价值交易确认等。也适合需要快速验证而不便要求用户配合的场景。'
      },
      { 
        title: '改进多模态', 
        description: '结合多种检测手段，提供更高精度的活体验证，全面防护安全', 
        icon: 'mdi-shield-check', 
        color: 'success',
        keywords: ['多重检测', '高安全性'],
        detailDescription: '改进多模态活体检测技术是一种综合性解决方案，它融合了多种检测方法的优势，包括动作分析、深度学习特征提取、3D结构分析等。通过多种技术的协同工作，系统能够在各种环境条件下提供高度可靠的活体检测结果。',
        principle: '系统同时部署多个独立的检测模块，各模块并行工作并输出独立的判断结果。通过加权融合算法，综合考虑各模块的可信度，最终给出更准确的活体判断。当部分模块在特定条件下性能下降时，其他模块可以补充提供可靠判断，确保系统整体的鲁棒性。',
        features: [
          { title: '多因素验证', text: '至少三种独立技术共同判断', icon: 'mdi-check-all' },
          { title: '自适应调整', text: '根据环境条件动态调整检测策略', icon: 'mdi-tune' },
          { title: '抗攻击能力强', text: '防御各种已知欺骗手段', icon: 'mdi-security' },
          { title: '持续更新', text: '模块化设计便于升级和扩展', icon: 'mdi-update' }
        ],
        scenario: '适用于对安全性要求极高的关键应用场景，如重要金融交易授权、高级安保系统、政府敏感设施准入控制等。也适合需要在各种复杂环境中保持稳定性能的应用。'
      },
      { 
        title: '第三方API', 
        description: '利用专业第三方活体检测服务，提供更可靠的身份验证', 
        icon: 'mdi-cloud-check', 
        color: 'info',
        keywords: ['云服务', '稳定可靠'],
        detailDescription: '第三方API活体检测方案通过集成专业安全厂商提供的云端检测服务，利用其强大的算法能力和持续更新的安全数据库，为系统提供高可靠性的活体检测结果。这种方案无需本地部署复杂算法，维护成本低，且能够快速获取最新的安全更新。',
        principle: '系统将采集到的人脸图像或视频序列通过加密通道传输至第三方服务提供商的云端服务器。云端服务器使用最新的活体检测算法进行分析，并返回检测结果。服务提供商会持续更新算法以应对新出现的欺骗手段，确保系统安全性始终处于领先水平。',
        features: [
          { title: '专业防护', text: '由安全领域专家维护的检测系统', icon: 'mdi-account-supervisor' },
          { title: '自动更新', text: '无需手动升级即可获取最新防护', icon: 'mdi-cloud-sync' },
          { title: '高可靠性', text: '99.9%以上的服务可用性', icon: 'mdi-check-circle' },
          { title: '可扩展性', text: '根据需求弹性调整处理能力', icon: 'mdi-arrow-expand' }
        ],
        scenario: '适用于不便于部署和维护复杂本地算法的场景，如中小型企业的身份验证系统、需要快速部署的临时安全控制、移动应用中的身份验证功能等。也适合需要持续获取最新安全更新的应用场景。'
      }
    ],
    features: [
      { title: '快速识别', text: '亚秒级人脸识别', icon: 'mdi-clock-fast', color: 'primary' },
      { title: '多重安全', text: '防欺骗检测机制', icon: 'mdi-security', color: 'error' },
      { title: '便捷管理', text: '考勤数据可视化', icon: 'mdi-chart-bar', color: 'success' },
      { title: '易于部署', text: '简单快捷的配置', icon: 'mdi-cog', color: 'warning' }
    ]
  }),
  methods: {
    openTechDetails(tech) {
      this.selectedTech = tech;
      this.techDetailsDialog = true;
    }
  }
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

/* 美化后的活体检测技术卡片 */
.tech-card-wrapper {
  position: relative;
  margin-top: 35px; /* 增加顶部空间 */
}

.tech-card {
  position: relative;
  height: 100%;
  border-radius: 16px !important;
  transition: all 0.3s ease;
  overflow: hidden;
  transform: translateY(0);
  background-color: white !important;
  border: none !important;
}

.tech-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15) !important;
}

.tech-card.on-hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2) !important;
}

.tech-icon-circle {
  position: absolute;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  top: -30px; /* 调整位置，让图标更靠上 */
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  z-index: 2; /* 提高层级 */
  transition: all 0.3s ease;
}

.on-hover .tech-icon-circle {
  transform: translateX(-50%) scale(1.1);
}

.tech-card-primary {
  border-top: 3px solid #1976d2 !important;
}

.tech-icon-primary {
  background-color: #1976d2;
}

.tech-card-purple {
  border-top: 3px solid #9c27b0 !important;
}

.tech-icon-purple {
  background-color: #9c27b0;
}

.tech-card-success {
  border-top: 3px solid #4caf50 !important;
}

.tech-icon-success {
  background-color: #4caf50;
}

.tech-card-info {
  border-top: 3px solid #2196f3 !important;
}

.tech-icon-info {
  background-color: #2196f3;
}

.tech-description {
  font-size: 0.9rem;
  color: rgba(0, 0, 0, 0.6);
  line-height: 1.5;
}

.keyword-chips {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

/* 暗黑模式适配 */
.theme--dark .tech-card {
  background-color: #2c2c2c !important;
}

.theme--dark .tech-description {
  color: rgba(255, 255, 255, 0.7);
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

/* 深色模式适配 */
.theme--dark .detection-card {
  background-color: #2c2c2c !important;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.theme--dark .detection-card:hover {
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4) !important;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.theme--dark .feature-item {
  background-color: rgba(30, 30, 30, 0.6);
}

.theme--dark .feature-item:hover {
  background-color: rgba(40, 40, 40, 0.9);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.theme--dark .gradient-bg {
  background: linear-gradient(135deg, #0d47a1 0%, #2196f3 50%, #673ab7 100%) !important;
}

.theme--dark .v-card:hover {
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.4), 0 10px 10px rgba(0, 0, 0, 0.3) !important;
}

.theme--dark .animate-typing {
  border-right-color: #e0e0e0;
}

@keyframes typing {
  from { width: 0; }
  to { width: 250px; }
}

@keyframes blinking {
  0%, 100% { border-color: transparent; }
  50% { border-color: white; }
}

.theme--dark @keyframes blinking {
  0%, 100% { border-color: transparent; }
  50% { border-color: #e0e0e0; }
}

/* 主要卡片区域样式 */
.main-section-card {
  border-radius: 24px !important;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.95) 100%) !important;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  overflow: hidden;
}

.tech-section-title {
  padding-top: 24px;
  padding-bottom: 0;
  position: relative;
}

.tech-section-title::after {
  content: '';
  position: absolute;
  left: 24px;
  bottom: -5px;
  width: 60px;
  height: 3px;
  background-color: var(--v-primary-base, #1976d2);
  border-radius: 3px;
}

/* 暗黑模式适配 */
.theme--dark .main-section-card {
  background: linear-gradient(135deg, rgba(30, 30, 30, 0.9) 0%, rgba(40, 40, 40, 0.95) 100%) !important;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.theme--dark .subtitle-1 {
  color: rgba(255, 255, 255, 0.7) !important;
}

.animated-btn {
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(33, 150, 243, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(33, 150, 243, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(33, 150, 243, 0);
  }
}

.tech-overlay {
  z-index: 3; /* 确保覆盖层在图标上方 */
}

/* 技术详情对话框样式 */
.tech-details-card {
  border-radius: 16px;
  overflow: hidden;
}

.feature-card {
  transition: all 0.3s ease;
  border-radius: 12px !important;
}

.feature-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1) !important;
}

/* 深色模式适配 */
.theme--dark .tech-details-card {
  background-color: #1E1E1E !important;
}

.theme--dark .feature-card {
  background-color: #2c2c2c !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
}
</style> 