<template>
  <div class="records-page">
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <v-card class="solid-card mb-5" elevation="3">
            <v-card-title class="text-h4 font-weight-bold primary--text py-4">
              <v-icon large color="primary" class="mr-3">mdi-clipboard-text</v-icon>
              考勤记录
            </v-card-title>
          </v-card>
        </v-col>
      </v-row>
      
      <v-row>
        <v-col cols="12" lg="3" md="4">
          <v-card class="solid-card hover-card mb-4" elevation="2">
            <v-card-title class="subtitle-1">
              <v-icon color="primary" class="mr-2">mdi-filter-variant</v-icon>
              筛选选项
            </v-card-title>
            <v-card-text>
              <v-text-field
                v-model="search"
                label="搜索"
                prepend-icon="mdi-magnify"
                clearable
                outlined
                dense
                hide-details
                class="mb-4"
              ></v-text-field>
              
              <v-select
                v-model="selectedClass"
                :items="classOptions"
                label="班级筛选"
                item-text="name"
                item-value="id"
                prepend-icon="mdi-account-group"
                outlined
                dense
                clearable
                hide-details
                class="mb-4"
                @change="filterByClass"
              ></v-select>
              
              <v-divider class="my-4"></v-divider>
              
              <v-btn 
                color="primary" 
                block 
                class="btn-pulse mb-3" 
                rounded
                elevation="2"
                @click="refreshData"
              >
                <v-icon left>mdi-refresh</v-icon>
                刷新数据
              </v-btn>
              
              <v-btn 
                color="success" 
                block 
                class="btn-pulse" 
                rounded
                elevation="2"
                @click="exportToExcel"
              >
                <v-icon left>mdi-file-excel</v-icon>
                导出Excel
              </v-btn>
            </v-card-text>
          </v-card>
          
          <v-card class="solid-card hover-card stats-card" elevation="2">
            <v-card-title class="subtitle-1">
              <v-icon color="primary" class="mr-2">mdi-chart-box</v-icon>
              考勤统计
            </v-card-title>
            <v-card-text>
              <div class="stat-item">
                <div class="stat-label">总记录数</div>
                <div class="stat-value">{{ attendanceRecords.length }}</div>
              </div>
              
              <div class="stat-item">
                <div class="stat-label">正常出勤</div>
                <div class="stat-value success--text">
                  {{ attendanceRecords.filter(r => r.status === 'normal').length }}
                </div>
              </div>
              
              <div class="stat-item">
                <div class="stat-label">迟到</div>
                <div class="stat-value warning--text">
                  {{ attendanceRecords.filter(r => r.status === 'late').length }}
                </div>
              </div>
              
              <div class="stat-item">
                <div class="stat-label">缺勤</div>
                <div class="stat-value error--text">
                  {{ attendanceRecords.filter(r => r.status === 'absent').length }}
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="12" lg="9" md="8">
          <v-card class="solid-card" elevation="2">
            <v-card-title class="d-flex justify-space-between align-center">
              <span class="subtitle-1 font-weight-medium">
                <v-icon color="primary" class="mr-2">mdi-table</v-icon>
                学生考勤记录表
              </span>
              <div class="d-flex align-center">
                <v-chip small color="primary" class="mr-2">
                  <v-icon left small>mdi-eye</v-icon>
                  {{ displayRecords.length }} 条记录
                </v-chip>
                <v-btn icon small @click="refreshData" class="btn-pulse">
                  <v-icon>mdi-refresh</v-icon>
                </v-btn>
              </div>
            </v-card-title>
            
            <v-data-table
              :headers="headers"
              :items="attendanceRecords"
              :search="search"
              :loading="isLoading"
              :items-per-page="10"
              class="elevation-0"
              :footer-props="{
                'items-per-page-options': [5, 10, 15, 20, -1],
                'items-per-page-text': '每页显示'
              }"
              :loading-text="'正在加载数据...'"
              :no-data-text="'暂无考勤记录数据'"
            >
              <!-- 学生姓名列 -->
              <template v-slot:item.student_name="{ item }">
                <v-chip small label class="font-weight-medium">
                  {{ item.student_name }}
                </v-chip>
              </template>
              
              <!-- 日期列 -->
              <template v-slot:item.date="{ item }">
                <span class="font-weight-medium">{{ formatDate(item.date) }}</span>
              </template>
              
              <!-- 时间列 -->
              <template v-slot:item.time="{ item }">
                <span>{{ item.time }}</span>
              </template>
              
              <!-- 状态列 -->
              <template v-slot:item.status="{ item }">
                <v-chip
                  small
                  :color="getStatusColor(item.status)"
                  label
                  class="white--text"
                >
                  {{ getStatusText(item.status) }}
                </v-chip>
              </template>
              
              <!-- 识别置信度列 -->
              <template v-slot:item.recognition_confidence="{ item }">
                <v-progress-linear
                  :value="item.recognition_confidence * 100"
                  height="10"
                  rounded
                  :color="getConfidenceColor(item.recognition_confidence)"
                  class="mt-1"
                ></v-progress-linear>
                <span class="caption">{{ (item.recognition_confidence * 100).toFixed(1) }}%</span>
              </template>
              
              <!-- 活体检测方法列 -->
              <template v-slot:item.liveness_method="{ item }">
                <v-chip
                  x-small
                  outlined
                  :color="getLivenessMethodColor(item.liveness_method)"
                >
                  {{ getLivenessMethodText(item.liveness_method) }}
                </v-chip>
              </template>
              
              <!-- 操作列 -->
              <template v-slot:item.actions="{ item }">
                <v-btn icon small color="info" class="mr-2 btn-pulse" @click="viewDetails(item)">
                  <v-icon small>mdi-eye</v-icon>
                </v-btn>
              </template>
              
              <!-- 没有数据时显示 -->
              <template v-slot:no-data>
                <div class="d-flex flex-column align-center py-5">
                  <v-icon size="64" color="grey lighten-1">mdi-calendar-blank</v-icon>
                  <div class="text-subtitle-1 mt-3 text-center grey--text">
                    暂无考勤记录数据，请先进行考勤打卡。
                  </div>
                  <v-btn color="primary" class="mt-4 btn-pulse" rounded to="/attendance">
                    <v-icon left>mdi-account-check</v-icon>
                    前往考勤
                  </v-btn>
                </div>
              </template>
            </v-data-table>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    
    <!-- 详情对话框 -->
    <v-dialog v-model="detailsDialog" max-width="500" transition="dialog-transition">
      <v-card class="solid-card">
        <v-card-title class="primary--text d-flex justify-space-between align-center">
          <span>
            <v-icon color="primary" class="mr-2">mdi-account-details</v-icon>
            考勤详情
          </span>
          <v-btn icon small @click="detailsDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text v-if="selectedRecord" class="pt-4">
          <v-row>
            <v-col cols="12" sm="6">
              <div class="detail-item">
                <v-icon small color="primary" class="mr-2">mdi-badge-account</v-icon>
                <div class="detail-label">学号</div>
                <div class="detail-value">{{ selectedRecord.student_id }}</div>
              </div>
            </v-col>
            
            <v-col cols="12" sm="6">
              <div class="detail-item">
                <v-icon small color="primary" class="mr-2">mdi-account</v-icon>
                <div class="detail-label">姓名</div>
                <div class="detail-value">{{ selectedRecord.student_name }}</div>
              </div>
            </v-col>
            
            <v-col cols="12" sm="6">
              <div class="detail-item">
                <v-icon small color="primary" class="mr-2">mdi-calendar</v-icon>
                <div class="detail-label">日期</div>
                <div class="detail-value">{{ formatDate(selectedRecord.date) }}</div>
              </div>
            </v-col>
            
            <v-col cols="12" sm="6">
              <div class="detail-item">
                <v-icon small color="primary" class="mr-2">mdi-clock-outline</v-icon>
                <div class="detail-label">时间</div>
                <div class="detail-value">{{ selectedRecord.time }}</div>
              </div>
            </v-col>
            
            <v-col cols="12" sm="6" v-if="selectedRecord.similarity">
              <div class="detail-item">
                <v-icon small color="primary" class="mr-2">mdi-account-check</v-icon>
                <div class="detail-label">相似度</div>
                <div class="detail-value">
                  <v-progress-linear
                    :value="selectedRecord.similarity * 100"
                    height="6"
                    rounded
                    :color="getConfidenceColor(selectedRecord.similarity)"
                  ></v-progress-linear>
                  <span class="caption">{{ (selectedRecord.similarity * 100).toFixed(2) }}%</span>
                </div>
              </div>
            </v-col>
            
            <v-col cols="12" sm="6">
              <div class="detail-item">
                <v-icon small color="primary" class="mr-2">mdi-alert-circle-outline</v-icon>
                <div class="detail-label">状态</div>
                <div class="detail-value">
                  <v-chip
                    x-small
                    :color="getStatusColor(selectedRecord.status)"
                    label
                    class="white--text"
                  >
                    {{ getStatusText(selectedRecord.status) }}
                  </v-chip>
                </div>
              </div>
            </v-col>
            
            <v-col cols="12" sm="6" v-if="selectedRecord.recognition_confidence">
              <div class="detail-item">
                <v-icon small color="primary" class="mr-2">mdi-face-recognition</v-icon>
                <div class="detail-label">识别置信度</div>
                <div class="detail-value">
                  <v-progress-linear
                    :value="selectedRecord.recognition_confidence * 100"
                    height="6"
                    rounded
                    :color="getConfidenceColor(selectedRecord.recognition_confidence)"
                  ></v-progress-linear>
                  <span class="caption">{{ (selectedRecord.recognition_confidence * 100).toFixed(2) }}%</span>
                </div>
              </div>
            </v-col>
            
            <v-col cols="12" sm="6" v-if="selectedRecord.liveness_method">
              <div class="detail-item">
                <v-icon small color="primary" class="mr-2">mdi-shield-check</v-icon>
                <div class="detail-label">活体检测方法</div>
                <div class="detail-value">
                  <v-chip
                    x-small
                    outlined
                    :color="getLivenessMethodColor(selectedRecord.liveness_method)"
                  >
                    {{ getLivenessMethodText(selectedRecord.liveness_method) }}
                  </v-chip>
                </div>
              </div>
            </v-col>
            
            <v-col cols="12" sm="6" v-if="selectedRecord.liveness_confidence">
              <div class="detail-item">
                <v-icon small color="primary" class="mr-2">mdi-shield-account</v-icon>
                <div class="detail-label">活体检测置信度</div>
                <div class="detail-value">
                  <v-progress-linear
                    :value="selectedRecord.liveness_confidence * 100"
                    height="6"
                    rounded
                    :color="getConfidenceColor(selectedRecord.liveness_confidence)"
                  ></v-progress-linear>
                  <span class="caption">{{ (selectedRecord.liveness_confidence * 100).toFixed(2) }}%</span>
                </div>
              </div>
            </v-col>
          </v-row>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn color="primary" text rounded class="btn-pulse" @click="detailsDialog = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import * as XLSX from 'xlsx';

export default {
  name: 'Records',
  data: () => ({
    attendanceRecords: [],
    filteredRecords: [],
    classInfo: null,
    classOptions: [],
    search: '',
    selectedClass: null,
    isLoading: false,
    isFiltered: false,
    detailsDialog: false,
    selectedRecord: null,
    headers: [
      { text: '学号', value: 'student_id', sortable: true },
      { text: '姓名', value: 'student_name', sortable: true },
      { text: '日期', value: 'date', sortable: true },
      { text: '时间', value: 'time', sortable: true },
      { text: '状态', value: 'status', sortable: true },
      { text: '识别置信度', value: 'recognition_confidence', sortable: true },
      { text: '活体检测方法', value: 'liveness_method', sortable: true },
      { text: '操作', value: 'actions', sortable: false }
    ]
  }),
  computed: {
    ...mapState(['error']),
    
    displayRecords() {
      return this.isFiltered ? this.filteredRecords : this.attendanceRecords;
    }
  },
  methods: {
    ...mapMutations(['SET_ERROR']),
    
    async fetchAttendanceRecords() {
      this.isLoading = true;
      try {
        const response = await fetch('/api/get_attendance');
        if (!response.ok) throw new Error('获取考勤记录失败');
        
        const data = await response.json();
        this.attendanceRecords = data;
      } catch (error) {
        console.error('获取考勤记录出错:', error);
        this.SET_ERROR(`获取考勤记录失败: ${error.message}`);
      } finally {
        this.isLoading = false;
      }
    },
    
    async fetchClassInfo() {
      try {
        const response = await fetch('/api/class_info');
        if (!response.ok) throw new Error('获取班级信息失败');
        
        const data = await response.json();
        this.classInfo = data;
      } catch (error) {
        console.error('获取班级信息出错:', error);
        this.SET_ERROR(`获取班级信息失败: ${error.message}`);
      }
    },
    
    formatDate(dateString) {
      const date = new Date(dateString);
      const month = ('0' + (date.getMonth() + 1)).slice(-2);
      const day = ('0' + date.getDate()).slice(-2);
      const dayOfWeek = ['日', '一', '二', '三', '四', '五', '六'][date.getDay()];
      
      return `${date.getFullYear()}年${month}月${day}日 星期${dayOfWeek}`;
    },
    
    getStatusColor(status) {
      switch(status) {
        case 'normal':
          return 'success';
        case 'late':
          return 'warning';
        case 'absent':
          return 'error';
        default:
          return 'success';
      }
    },
    
    getStatusText(status) {
      switch(status) {
        case 'normal':
          return '正常';
        case 'late':
          return '迟到';
        case 'absent':
          return '缺勤';
        default:
          return '正常';
      }
    },
    
    getLivenessMethodText(method) {
      switch(method) {
        case 'blink':
          return '眨眼检测';
        case 'deep_learning':
          return '深度学习';
        case 'api':
          return 'API检测';
        default:
          return method || '未知';
      }
    },
    
    getLivenessMethodColor(method) {
      switch(method) {
        case 'blink':
          return 'purple';
        case 'deep_learning':
          return 'blue';
        case 'api':
          return 'cyan';
        default:
          return 'grey';
      }
    },
    
    getConfidenceColor(score) {
      if (score > 0.8) return 'success';
      if (score > 0.6) return 'primary';
      if (score > 0.4) return 'warning';
      return 'error';
    },
    
    viewDetails(item) {
      this.selectedRecord = item;
      this.detailsDialog = true;
    },
    
    async refreshData() {
      await this.fetchAttendanceRecords();
      this.isFiltered = false;
    },
    
    filterByClass(classId) {
      if (!classId) {
        this.isFiltered = false;
        return;
      }
      
      // 在实际系统中，这应该是从后端获取的数据，这里只是模拟
      this.filteredRecords = this.attendanceRecords.filter(record => {
        // 假设每个学生记录都有对应的班级信息
        return record.class_id === classId;
      });
      
      this.isFiltered = true;
    },
    
    exportToExcel() {
      try {
        // 显示加载状态
        this.isLoading = true;
        
        // 准备要导出的数据
        const records = this.isFiltered ? this.filteredRecords : this.attendanceRecords;
        
        if (records.length === 0) {
          this.SET_ERROR('没有可导出的数据');
          this.isLoading = false;
          return;
        }
        
        // 创建要导出的数据数组，转换字段名为中文
        const exportData = records.map(record => ({
          '学号': record.student_id,
          '姓名': record.student_name,
          '日期': record.date,
          '时间': record.time,
          '状态': this.getStatusText(record.status),
          '识别置信度': (record.recognition_confidence * 100).toFixed(1) + '%',
          '活体检测方法': this.getLivenessMethodText(record.liveness_method),
          '活体检测置信度': record.liveness_confidence ? (record.liveness_confidence * 100).toFixed(1) + '%' : '未知'
        }));
        
        // 创建工作簿和工作表
        const workbook = XLSX.utils.book_new();
        const worksheet = XLSX.utils.json_to_sheet(exportData);
        
        // 设置列宽
        const columnWidths = [
          { wch: 15 }, // 学号
          { wch: 10 }, // 姓名
          { wch: 12 }, // 日期
          { wch: 10 }, // 时间
          { wch: 8 },  // 状态
          { wch: 12 }, // 识别置信度
          { wch: 12 }, // 活体检测方法
          { wch: 15 }  // 活体检测置信度
        ];
        worksheet['!cols'] = columnWidths;
        
        // 将工作表添加到工作簿
        XLSX.utils.book_append_sheet(workbook, worksheet, '考勤记录');
        
        // 生成文件名，包含当前日期时间
        const now = new Date();
        const dateStr = `${now.getFullYear()}${(now.getMonth()+1).toString().padStart(2, '0')}${now.getDate().toString().padStart(2, '0')}`;
        const timeStr = `${now.getHours().toString().padStart(2, '0')}${now.getMinutes().toString().padStart(2, '0')}`;
        const fileName = `考勤记录_${dateStr}_${timeStr}.xlsx`;
        
        // 导出Excel文件
        XLSX.writeFile(workbook, fileName);
        
        // 导出成功提示
        this.$store.commit('SET_SUCCESS', '考勤记录已成功导出为Excel文件');
      } catch (error) {
        console.error('导出Excel失败:', error);
        this.SET_ERROR(`导出Excel失败: ${error.message}`);
      } finally {
        this.isLoading = false;
      }
    }
  },
  async mounted() {
    // 获取考勤记录和班级信息
    await Promise.all([
      this.fetchAttendanceRecords(),
      this.fetchClassInfo()
    ]);
    
    // 更新班级选项
    if (this.classInfo && this.classInfo.classes && this.classInfo.classes.length > 0) {
      this.classOptions = this.classInfo.classes.map(c => ({ 
        id: c.id || c.class_id, 
        name: c.name || c.class_name 
      }));
    }
  }
}
</script>

<style scoped>
.records-page {
  min-height: calc(100vh - 145px);
  position: relative;
}

/* 统计卡片样式 */
.stats-card {
  background: linear-gradient(to right bottom, rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.5));
}

.stat-item {
  display: flex;
  flex-direction: column;
  padding: 12px;
  margin-bottom: 8px;
  border-radius: 8px;
  background-color: rgba(0, 0, 0, 0.03);
  transition: all 0.3s ease;
}

.stat-item:hover {
  background-color: rgba(0, 0, 0, 0.06);
  transform: translateY(-2px);
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.7;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 1.3rem;
  font-weight: 700;
}

/* 详情项样式 */
.detail-item {
  margin-bottom: 12px;
  padding: 8px;
  border-radius: 8px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.02);
  transition: all 0.3s ease;
}

.detail-item:hover {
  background-color: rgba(0, 0, 0, 0.04);
}

.detail-label {
  font-size: 0.85rem;
  opacity: 0.7;
  margin-right: 8px;
}

.detail-value {
  font-weight: 500;
  flex-grow: 1;
  text-align: right;
}

/* 动画效果 */
.dialog-transition-enter-active,
.dialog-transition-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.dialog-transition-enter-from,
.dialog-transition-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* 添加响应式样式 */
@media (max-width: 600px) {
  .detail-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .detail-value {
    text-align: left;
    margin-top: 4px;
  }
}
</style> 