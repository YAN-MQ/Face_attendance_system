<template>
  <div class="home">
    <v-row>
      <v-col cols="12">
        <v-card elevation="2">
          <v-card-title class="headline primary white--text">
            基于人脸识别与活体检测的班级考勤系统
          </v-card-title>
          <v-card-text class="pa-4">
            <p class="text-h6 mb-3">欢迎使用班级考勤系统</p>
            <p>本系统采用先进的人脸识别与活体检测技术，能够准确识别学生身份并防止考勤作弊。</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12" md="4">
        <v-card height="100%">
          <v-card-title class="secondary white--text">
            <v-icon left dark>mdi-account-check</v-icon>
            考勤打卡
          </v-card-title>
          <v-card-text>
            <p>使用摄像头进行人脸识别考勤打卡，支持多种活体检测方式防止欺骗攻击。</p>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" text to="/attendance">
              去打卡
              <v-icon right>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card height="100%">
          <v-card-title class="secondary white--text">
            <v-icon left dark>mdi-account-plus</v-icon>
            人脸注册
          </v-card-title>
          <v-card-text>
            <p>为新学生注册人脸信息，以便系统能够正确识别学生身份。</p>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" text to="/register">
              去注册
              <v-icon right>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card height="100%">
          <v-card-title class="secondary white--text">
            <v-icon left dark>mdi-clipboard-text</v-icon>
            考勤记录
          </v-card-title>
          <v-card-text>
            <p>查看和导出考勤记录，掌握学生出勤情况，便于班级管理。</p>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" text to="/records">
              查看记录
              <v-icon right>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <v-icon left>mdi-shield-account</v-icon>
            活体检测技术
          </v-card-title>
          <v-card-text>
            <p>本系统集成了三种不同的活体检测方案，有效防止照片和视频攻击：</p>
            
            <v-list two-line>
              <v-list-item>
                <v-list-item-icon>
                  <v-icon color="primary">mdi-eye</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>眨眼检测</v-list-item-title>
                  <v-list-item-subtitle>通过检测用户的眨眼动作来判断是否为真人</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-icon>
                  <v-icon color="primary">mdi-brain</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>深度学习纹理分析</v-list-item-title>
                  <v-list-item-subtitle>基于深度学习的纹理分析，能够区分真实人脸与照片</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-icon>
                  <v-icon color="primary">mdi-cloud</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>第三方API活体检测</v-list-item-title>
                  <v-list-item-subtitle>接入腾讯云人脸识别API，提供更高精度的活体检测</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: 'Home',
  components: {
  }
}
</script> 