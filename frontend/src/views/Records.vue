<template>
  <div class="records">
    <v-row>
      <v-col cols="12">
        <v-card elevation="2">
          <v-card-title class="headline">
            <v-icon left>mdi-clipboard-text</v-icon>
            考勤记录
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="搜索"
              single-line
              hide-details
              class="ml-2"
              style="max-width: 300px;"
            ></v-text-field>
          </v-card-title>
          
          <v-data-table
            :headers="headers"
            :items="attendanceRecords"
            :search="search"
            :loading="isLoading"
            :items-per-page="10"
            class="elevation-1"
          >
            <template v-slot:top>
              <v-toolbar flat>
                <v-toolbar-title>学生考勤记录</v-toolbar-title>
                <v-divider class="mx-4" inset vertical></v-divider>
                <v-select
                  v-model="selectedClass"
                  :items="classOptions"
                  label="班级筛选"
                  item-text="name"
                  item-value="id"
                  style="max-width: 200px;"
                  clearable
                  class="ml-2"
                  @change="filterByClass"
                ></v-select>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="refreshData">
                  <v-icon left>mdi-refresh</v-icon>
                  刷新
                </v-btn>
                <v-btn color="primary" class="ml-2" @click="exportToExcel">
                  <v-icon left>mdi-file-excel</v-icon>
                  导出Excel
                </v-btn>
              </v-toolbar>
            </template>
            
            <!-- 学生姓名列 -->
            <template v-slot:item.student_name="{ item }">
              <v-chip small>{{ item.student_name }}</v-chip>
            </template>
            
            <!-- 日期列 -->
            <template v-slot:item.date="{ item }">
              {{ formatDate(item.date) }}
            </template>
            
            <!-- 时间列 -->
            <template v-slot:item.time="{ item }">
              {{ item.time }}
            </template>
            
            <!-- 状态列 -->
            <template v-slot:item.status="{ item }">
              <v-chip
                :color="getStatusColor(item.status)"
                small
              >
                {{ getStatusText(item.status) }}
              </v-chip>
            </template>
            
            <!-- 识别置信度列 -->
            <template v-slot:item.recognition_confidence="{ item }">
              {{ (item.recognition_confidence * 100).toFixed(2) }}%
            </template>
            
            <!-- 活体检测方法列 -->
            <template v-slot:item.liveness_method="{ item }">
              {{ getLivenessMethodText(item.liveness_method) }}
            </template>
            
            <!-- 操作列 -->
            <template v-slot:item.actions="{ item }">
              <v-icon small class="mr-2" @click="viewDetails(item)">
                mdi-eye
              </v-icon>
            </template>
            
            <!-- 没有数据时显示 -->
            <template v-slot:no-data>
              <v-alert type="info" outlined>
                暂无考勤记录数据，请先进行考勤打卡。
              </v-alert>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- 详情对话框 -->
    <v-dialog v-model="detailsDialog" max-width="500">
      <v-card>
        <v-card-title>考勤详情</v-card-title>
        <v-card-text v-if="selectedRecord">
          <v-list dense>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>学号</v-list-item-title>
                <v-list-item-subtitle>{{ selectedRecord.student_id }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>姓名</v-list-item-title>
                <v-list-item-subtitle>{{ selectedRecord.student_name }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>日期</v-list-item-title>
                <v-list-item-subtitle>{{ formatDate(selectedRecord.date) }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>时间</v-list-item-title>
                <v-list-item-subtitle>{{ selectedRecord.time }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            
            <v-list-item v-if="selectedRecord.similarity">
              <v-list-item-content>
                <v-list-item-title>相似度</v-list-item-title>
                <v-list-item-subtitle>{{ (selectedRecord.similarity * 100).toFixed(2) }}%</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>状态</v-list-item-title>
                <v-list-item-subtitle>
                  <v-chip
                    x-small
                    :color="getStatusColor(selectedRecord.status)"
                  >
                    {{ getStatusText(selectedRecord.status) }}
                  </v-chip>
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            
            <v-list-item v-if="selectedRecord.recognition_confidence">
              <v-list-item-content>
                <v-list-item-title>识别置信度</v-list-item-title>
                <v-list-item-subtitle>{{ (selectedRecord.recognition_confidence * 100).toFixed(2) }}%</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            
            <v-list-item v-if="selectedRecord.liveness_method">
              <v-list-item-content>
                <v-list-item-title>活体检测方法</v-list-item-title>
                <v-list-item-subtitle>{{ getLivenessMethodText(selectedRecord.liveness_method) }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            
            <v-list-item v-if="selectedRecord.liveness_confidence">
              <v-list-item-content>
                <v-list-item-title>活体检测置信度</v-list-item-title>
                <v-list-item-subtitle>{{ (selectedRecord.liveness_confidence * 100).toFixed(2) }}%</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="detailsDialog = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'Records',
  data: () => ({
    search: '',
    selectedClass: null,
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
    ],
    classOptions: [
      { id: 'class1', name: '计算机科学与技术1班' },
      { id: 'class2', name: '计算机科学与技术2班' },
      { id: 'class3', name: '软件工程1班' },
      { id: 'class4', name: '软件工程2班' },
      { id: 'class5', name: '网络工程1班' }
    ],
    filteredRecords: [],
    isFiltered: false
  }),
  computed: {
    ...mapGetters([
      'attendanceRecords',
      'isLoading',
      'error',
      'classInfo'
    ]),
    displayRecords() {
      return this.isFiltered ? this.filteredRecords : this.attendanceRecords;
    }
  },
  methods: {
    ...mapActions(['fetchAttendanceRecords', 'fetchClassInfo']),
    
    formatDate(dateStr) {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      if (isNaN(date.getTime())) return dateStr;
      
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
      });
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
      // 这里应该实现导出为Excel的功能
      // 实际开发中可能需要使用第三方库，如xlsx.js
      alert('导出Excel功能需要在实际项目中实现');
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
.records {
  margin-bottom: 20px;
}
</style> 