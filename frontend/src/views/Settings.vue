<template>
  <div class="settings">
    <v-row>
      <v-col cols="12" md="6">
        <v-card elevation="2">
          <v-card-title class="headline">
            <v-icon left>mdi-shield-account</v-icon>
            活体检测设置
          </v-card-title>
          
          <v-card-text>
            <p class="subtitle-1">选择默认的活体检测方案</p>
            <p class="body-2 mb-4">系统集成了三种不同的活体检测方案，您可以根据安全级别需求选择合适的方案。</p>
            
            <v-radio-group v-model="livenessMethod" @change="updateLivenessMethod">
              <v-radio
                label="眨眼检测"
                value="blink"
              >
                <template v-slot:label>
                  <div>
                    <strong>眨眼检测</strong>
                    <div class="text-caption">通过检测用户的眨眼动作来判断是否为真人，能有效防止照片攻击。</div>
                  </div>
                </template>
              </v-radio>
              
              <v-radio
                label="深度学习"
                value="deep_learning"
              >
                <template v-slot:label>
                  <div>
                    <strong>深度学习纹理分析</strong>
                    <div class="text-caption">基于深度学习的纹理分析，能够区分真实人脸与照片/视频，精度更高。</div>
                  </div>
                </template>
              </v-radio>
              
              <v-radio
                label="API检测"
                value="api"
                :disabled="!apiConfigured"
              >
                <template v-slot:label>
                  <div>
                    <strong>第三方API活体检测</strong>
                    <div class="text-caption">
                      接入腾讯云人脸识别API，提供高精度的活体检测，需要配置API密钥。
                      <v-btn
                        x-small
                        text
                        color="primary"
                        @click.stop="openConfigDialog"
                      >
                        配置API
                      </v-btn>
                    </div>
                  </div>
                </template>
              </v-radio>
            </v-radio-group>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="6">
        <v-card elevation="2">
          <v-card-title class="headline">
            <v-icon left>mdi-cog</v-icon>
            系统设置
          </v-card-title>
          
          <v-card-text>
            <v-form ref="form">
              <v-switch
                v-model="settings.enableNotifications"
                label="启用通知"
                hint="打卡成功后显示通知"
                persistent-hint
                color="primary"
                @change="saveSettings"
              ></v-switch>
              
              <v-switch
                v-model="settings.autoRefresh"
                label="自动刷新考勤记录"
                hint="每隔5分钟自动刷新考勤记录"
                persistent-hint
                color="primary"
                @change="saveSettings"
              ></v-switch>
              
              <v-switch
                v-model="settings.darkMode"
                label="深色模式"
                hint="使用深色主题"
                persistent-hint
                color="primary"
                @change="toggleDarkMode"
              ></v-switch>
              
              <v-divider class="my-4"></v-divider>
              
              <v-select
                v-model="settings.attendanceTimeout"
                :items="timeoutOptions"
                label="考勤超时设置"
                hint="设置考勤打卡超时时间"
                persistent-hint
                @change="saveSettings"
              ></v-select>
            </v-form>
          </v-card-text>
        </v-card>
        
        <v-card class="mt-4" elevation="2">
          <v-card-title class="headline">
            <v-icon left>mdi-information-outline</v-icon>
            系统信息
          </v-card-title>
          
          <v-card-text>
            <v-list dense>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>版本</v-list-item-title>
                  <v-list-item-subtitle>1.0.0</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>API状态</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip
                      x-small
                      :color="isAPIConnected ? 'success' : 'error'"
                    >
                      {{ isAPIConnected ? '已连接' : '未连接' }}
                    </v-chip>
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>开发者</v-list-item-title>
                  <v-list-item-subtitle>计算机科学技术学院</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
          
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" text @click="testConnection">
              <v-icon left>mdi-refresh</v-icon>
              测试连接
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- API配置对话框 -->
    <v-dialog v-model="configDialog" max-width="600px">
      <v-card>
        <v-card-title class="headline">
          <v-icon left>mdi-cloud</v-icon>
          API配置
        </v-card-title>
        
        <v-card-text>
          <v-form ref="apiForm" v-model="isAPIFormValid">
            <v-alert v-if="apiConfigError" type="error" class="mb-4">
              {{ apiConfigError }}
            </v-alert>
            
            <v-switch
              v-model="apiConfig.enabled"
              label="启用第三方API活体检测"
              color="primary"
            ></v-switch>
            
            <v-text-field
              v-model="apiConfig.secret_id"
              label="Secret ID"
              :rules="[v => !!v || 'Secret ID不能为空']"
              :disabled="!apiConfig.enabled"
              hint="腾讯云API的Secret ID"
              persistent-hint
            ></v-text-field>
            
            <v-text-field
              v-model="apiConfig.secret_key"
              label="Secret Key"
              :rules="[v => !!v || 'Secret Key不能为空']"
              :disabled="!apiConfig.enabled"
              hint="腾讯云API的Secret Key"
              persistent-hint
              type="password"
            ></v-text-field>
            
            <v-select
              v-model="apiConfig.region"
              :items="regionOptions"
              label="地区"
              :disabled="!apiConfig.enabled"
              hint="选择最靠近您的服务器区域以获得最佳性能"
              persistent-hint
            ></v-select>
          </v-form>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" text @click="configDialog = false">取消</v-btn>
          <v-btn
            color="success"
            text
            @click="saveAPIConfig"
            :disabled="!isAPIFormValid"
          >
            保存
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'Settings',
  data: () => ({
    livenessMethod: 'blink',
    configDialog: false,
    isAPIFormValid: false,
    apiConfigError: null,
    apiConfigured: false,
    isAPIConnected: false,
    settings: {
      enableNotifications: true,
      autoRefresh: false,
      darkMode: false,
      attendanceTimeout: 30
    },
    apiConfig: {
      enabled: false,
      secret_id: '',
      secret_key: '',
      region: 'ap-guangzhou'
    },
    timeoutOptions: [
      { text: '15分钟', value: 15 },
      { text: '30分钟', value: 30 },
      { text: '45分钟', value: 45 },
      { text: '60分钟', value: 60 }
    ],
    regionOptions: [
      { text: '华南地区(广州)', value: 'ap-guangzhou' },
      { text: '华东地区(上海)', value: 'ap-shanghai' },
      { text: '华北地区(北京)', value: 'ap-beijing' },
      { text: '港澳台地区(中国香港)', value: 'ap-hongkong' }
    ]
  }),
  computed: {
    ...mapGetters([
      'livenessMethod',
      'isLoading',
      'error'
    ])
  },
  methods: {
    ...mapActions([
      'setLivenessMethod'
    ]),
    
    updateLivenessMethod(method) {
      this.setLivenessMethod(method);
      this.saveSettings();
    },
    
    openConfigDialog() {
      this.configDialog = true;
    },
    
    async saveAPIConfig() {
      if (!this.isAPIFormValid) return;
      
      if (this.apiConfig.enabled && (!this.apiConfig.secret_id || !this.apiConfig.secret_key)) {
        this.apiConfigError = '启用API时必须提供Secret ID和Secret Key';
        return;
      }
      
      try {
        // 在实际项目中，这里应该调用后端API保存配置
        // const response = await this.$http.post('/api/configure_api', this.apiConfig);
        
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        this.apiConfigured = this.apiConfig.enabled;
        this.configDialog = false;
        this.apiConfigError = null;
        
        if (this.apiConfig.enabled) {
          this.$store.commit('SET_ERROR', null);
          this.$store.commit('SET_LIVENESS_METHOD', 'api');
        }
      } catch (error) {
        this.apiConfigError = '保存API配置失败: ' + error.message;
      }
    },
    
    saveSettings() {
      // 在实际项目中，应该将设置保存到localStorage或后端
      localStorage.setItem('settings', JSON.stringify(this.settings));
    },
    
    loadSettings() {
      const savedSettings = localStorage.getItem('settings');
      if (savedSettings) {
        this.settings = JSON.parse(savedSettings);
      }
    },
    
    toggleDarkMode() {
      this.$vuetify.theme.dark = this.settings.darkMode;
      this.saveSettings();
    },
    
    async testConnection() {
      // 在实际项目中，这里应该调用后端API测试连接
      // try {
      //   const response = await this.$http.get('/api/test_connection');
      //   this.isAPIConnected = response.data.success;
      // } catch (error) {
      //   this.isAPIConnected = false;
      // }
      
      // 模拟API调用
      this.isAPIConnected = Math.random() > 0.3;
    }
  },
  created() {
    this.loadSettings();
    this.livenessMethod = this.$store.getters.livenessMethod;
    
    // 模拟API配置状态
    this.apiConfigured = Math.random() > 0.5;
    this.isAPIConnected = Math.random() > 0.3;
  },
  mounted() {
    // 应用深色模式设置
    this.$vuetify.theme.dark = this.settings.darkMode;
  }
}
</script>

<style scoped>
.settings {
  margin-bottom: 20px;
}
</style> 