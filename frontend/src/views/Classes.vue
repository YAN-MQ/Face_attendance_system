<template>
  <div class="classes">
    <v-row>
      <v-col cols="12" md="7">
        <v-card elevation="2">
          <v-card-title class="headline">
            <v-icon left>mdi-account-group</v-icon>
            班级管理
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
            :items="classes"
            :search="search"
            :loading="isLoading"
            :items-per-page="10"
            class="elevation-1"
          >
            <template v-slot:top>
              <v-toolbar flat>
                <v-toolbar-title>班级列表</v-toolbar-title>
                <v-divider class="mx-4" inset vertical></v-divider>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="refreshData">
                  <v-icon left>mdi-refresh</v-icon>
                  刷新
                </v-btn>
                <v-btn color="success" class="ml-2" @click="openNewClassDialog">
                  <v-icon left>mdi-plus</v-icon>
                  新增班级
                </v-btn>
              </v-toolbar>
            </template>
            
            <!-- 班级名称列 -->
            <template v-slot:item.name="{ item }">
              <strong>{{ item.name }}</strong>
            </template>
            
            <!-- 学生数量列 -->
            <template v-slot:item.student_count="{ item }">
              <v-chip color="primary" small>{{ item.student_count || 0 }}</v-chip>
            </template>
            
            <!-- 操作列 -->
            <template v-slot:item.actions="{ item }">
              <v-icon small class="mr-2" @click="viewClass(item)">
                mdi-eye
              </v-icon>
              <v-icon small class="mr-2" @click="editClass(item)">
                mdi-pencil
              </v-icon>
              <v-icon small @click="deleteClass(item)">
                mdi-delete
              </v-icon>
            </template>
            
            <!-- 没有数据时显示 -->
            <template v-slot:no-data>
              <v-alert type="info" outlined>
                暂无班级数据，请添加班级。
              </v-alert>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="5">
        <v-card v-if="selectedClass" elevation="2">
          <v-card-title class="headline">
            <v-icon left>mdi-account-group</v-icon>
            {{ selectedClass.name }} - 详情
          </v-card-title>
          
          <v-card-text>
            <v-list dense>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>班级ID</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedClass.id }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>班级名称</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedClass.name }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>学生数量</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedClass.student_count || 0 }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item v-if="selectedClass.teacher">
                <v-list-item-content>
                  <v-list-item-title>班主任</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedClass.teacher }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item v-if="selectedClass.description">
                <v-list-item-content>
                  <v-list-item-title>描述</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedClass.description }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
            
            <v-divider class="my-4"></v-divider>
            
            <h3 class="mb-2">最近考勤统计</h3>
            <v-simple-table dense>
              <template v-slot:default>
                <thead>
                  <tr>
                    <th>状态</th>
                    <th>人数</th>
                    <th>比例</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>正常</td>
                    <td>{{ selectedClass.stats?.normal || 0 }}</td>
                    <td>{{ calcPercentage(selectedClass.stats?.normal, selectedClass.student_count) }}%</td>
                  </tr>
                  <tr>
                    <td>迟到</td>
                    <td>{{ selectedClass.stats?.late || 0 }}</td>
                    <td>{{ calcPercentage(selectedClass.stats?.late, selectedClass.student_count) }}%</td>
                  </tr>
                  <tr>
                    <td>缺勤</td>
                    <td>{{ selectedClass.stats?.absent || 0 }}</td>
                    <td>{{ calcPercentage(selectedClass.stats?.absent, selectedClass.student_count) }}%</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </v-card-text>
          
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" text @click="editClass(selectedClass)">
              <v-icon left>mdi-pencil</v-icon>
              编辑
            </v-btn>
            <v-btn color="error" text @click="deleteClass(selectedClass)">
              <v-icon left>mdi-delete</v-icon>
              删除
            </v-btn>
          </v-card-actions>
        </v-card>
        
        <v-card v-else elevation="2">
          <v-card-title class="headline">
            <v-icon left>mdi-information-outline</v-icon>
            班级管理说明
          </v-card-title>
          
          <v-card-text>
            <p>点击左侧班级查看详细信息。</p>
            <p>您可以添加、编辑和删除班级信息。</p>
            <p>班级信息将用于学生注册和考勤分析。</p>
          </v-card-text>
          
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="openNewClassDialog">
              <v-icon left>mdi-plus</v-icon>
              添加班级
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- 新增/编辑班级对话框 -->
    <v-dialog v-model="classDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">{{ formTitle }}</span>
        </v-card-title>
        
        <v-card-text>
          <v-form ref="form" v-model="isFormValid">
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="editedItem.name"
                    label="班级名称"
                    required
                    :rules="[v => !!v || '请输入班级名称']"
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12">
                  <v-text-field
                    v-model="editedItem.teacher"
                    label="班主任"
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12">
                  <v-textarea
                    v-model="editedItem.description"
                    label="描述"
                    rows="3"
                  ></v-textarea>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" text @click="closeClassDialog">取消</v-btn>
          <v-btn color="success" text @click="saveClass" :disabled="!isFormValid">保存</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- 删除确认对话框 -->
    <v-dialog v-model="deleteDialog" max-width="500px">
      <v-card>
        <v-card-title class="headline">确认删除</v-card-title>
        <v-card-text>确定要删除班级 "{{ editedItem.name }}" 吗？此操作不可撤销。</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="deleteDialog = false">取消</v-btn>
          <v-btn color="error" text @click="confirmDelete">确认删除</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'Classes',
  data: () => ({
    search: '',
    classDialog: false,
    deleteDialog: false,
    selectedClass: null,
    headers: [
      { text: '班级ID', value: 'id', sortable: true },
      { text: '班级名称', value: 'name', sortable: true },
      { text: '学生数量', value: 'student_count', sortable: true },
      { text: '班主任', value: 'teacher', sortable: true },
      { text: '操作', value: 'actions', sortable: false }
    ],
    editedIndex: -1,
    editedItem: {
      id: '',
      name: '',
      teacher: '',
      description: '',
      student_count: 0
    },
    defaultItem: {
      id: '',
      name: '',
      teacher: '',
      description: '',
      student_count: 0
    },
    isFormValid: false,
    // 示例数据 - 实际应用中应从后端获取
    sampleClasses: [
      {
        id: 'class1',
        name: '计算机科学与技术1班',
        teacher: '张教授',
        description: '本科2021级计算机科学与技术1班',
        student_count: 45,
        stats: { normal: 40, late: 3, absent: 2 }
      },
      {
        id: 'class2',
        name: '计算机科学与技术2班',
        teacher: '李教授',
        description: '本科2021级计算机科学与技术2班',
        student_count: 42,
        stats: { normal: 38, late: 2, absent: 2 }
      },
      {
        id: 'class3',
        name: '软件工程1班',
        teacher: '王教授',
        description: '本科2021级软件工程1班',
        student_count: 48,
        stats: { normal: 45, late: 2, absent: 1 }
      }
    ]
  }),
  computed: {
    ...mapGetters([
      'classInfo',
      'isLoading',
      'error'
    ]),
    formTitle () {
      return this.editedIndex === -1 ? '新增班级' : '编辑班级'
    },
    classes() {
      // 实际应用中应该使用从后端获取的数据
      // return this.classInfo.classes || []
      return this.sampleClasses
    }
  },
  methods: {
    ...mapActions([
      'fetchClassInfo'
    ]),
    
    calcPercentage(value, total) {
      if (!value || !total) return 0
      return ((value / total) * 100).toFixed(1)
    },
    
    viewClass(item) {
      this.selectedClass = item
    },
    
    openNewClassDialog() {
      this.editedIndex = -1
      this.editedItem = Object.assign({}, this.defaultItem)
      this.classDialog = true
    },
    
    editClass(item) {
      this.editedIndex = this.classes.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.classDialog = true
    },
    
    deleteClass(item) {
      this.editedIndex = this.classes.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.deleteDialog = true
    },
    
    closeClassDialog() {
      this.classDialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },
    
    saveClass() {
      if (this.editedIndex > -1) {
        // 更新现有班级
        Object.assign(this.classes[this.editedIndex], this.editedItem)
      } else {
        // 添加新班级
        this.editedItem.id = 'class' + (this.classes.length + 1) // 简单生成ID
        this.editedItem.student_count = 0 // 初始学生数为0
        this.sampleClasses.push(this.editedItem)
      }
      this.closeClassDialog()
    },
    
    confirmDelete() {
      this.sampleClasses.splice(this.editedIndex, 1)
      this.deleteDialog = false
      if (this.selectedClass && this.selectedClass.id === this.editedItem.id) {
        this.selectedClass = null
      }
    },
    
    async refreshData() {
      // 实际应用中从后端刷新数据
      await this.fetchClassInfo()
    }
  },
  async mounted() {
    // 获取班级信息
    await this.fetchClassInfo()
  }
}
</script>

<style scoped>
.classes {
  margin-bottom: 20px;
}
</style> 