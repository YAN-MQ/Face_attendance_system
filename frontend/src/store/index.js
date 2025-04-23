import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    attendanceRecords: [],
    classInfo: { classes: [] },
    livenessMethod: 'blink', // 默认活体检测方法
    loading: false,
    error: null,
    lastDetectionResult: null
  },
  mutations: {
    SET_ATTENDANCE_RECORDS(state, records) {
      state.attendanceRecords = records
    },
    SET_CLASS_INFO(state, info) {
      state.classInfo = info
    },
    SET_LIVENESS_METHOD(state, method) {
      state.livenessMethod = method
    },
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    SET_LAST_DETECTION_RESULT(state, result) {
      state.lastDetectionResult = result
    },
    ADD_ATTENDANCE_RECORD(state, record) {
      state.attendanceRecords.push(record)
    }
  },
  actions: {
    async fetchAttendanceRecords({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.get('/api/get_attendance')
        commit('SET_ATTENDANCE_RECORDS', response.data)
        commit('SET_ERROR', null)
      } catch (error) {
        commit('SET_ERROR', '获取考勤记录失败：' + error.message)
        console.error('获取考勤记录失败', error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async fetchClassInfo({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.get('/api/class_info')
        commit('SET_CLASS_INFO', response.data)
        commit('SET_ERROR', null)
      } catch (error) {
        commit('SET_ERROR', '获取班级信息失败：' + error.message)
        console.error('获取班级信息失败', error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async detectLiveness({ commit, state }, imageData) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.post('/api/detect_liveness', {
          image: imageData,
          method: state.livenessMethod
        })
        commit('SET_LAST_DETECTION_RESULT', response.data)
        commit('SET_ERROR', null)
        return response.data
      } catch (error) {
        const errorMsg = '活体检测失败：' + error.message
        commit('SET_ERROR', errorMsg)
        console.error(errorMsg, error)
        return { success: false, message: errorMsg }
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async recognizeFace({ commit, state }, imageData) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.post('/api/recognize_face', {
          image: imageData,
          method: state.livenessMethod
        })
        
        if (response.data.success) {
          commit('ADD_ATTENDANCE_RECORD', {
            student_id: response.data.student_id,
            student_name: response.data.student_name,
            timestamp: response.data.timestamp,
            similarity: response.data.similarity
          })
        }
        
        commit('SET_ERROR', null)
        return response.data
      } catch (error) {
        const errorMsg = '人脸识别失败：' + error.message
        commit('SET_ERROR', errorMsg)
        console.error(errorMsg, error)
        return { success: false, message: errorMsg }
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async registerFace({ commit }, { imageData, studentId, studentName, classId }) {
      commit('SET_LOADING', true);
      try {
        console.log(`开始注册学生信息: ID=${studentId}, 姓名=${studentName}, 班级=${classId}`);
        
        // 检查图像数据格式
        if (!imageData || typeof imageData !== 'string') {
          throw new Error('图像数据无效或格式不正确');
        }
        
        if (!imageData.startsWith('data:image')) {
          throw new Error('图像数据不是有效的Data URL格式');
        }
        
        console.log(`图像数据长度: ${imageData.length} 字符`);
        console.log(`图像数据前缀: ${imageData.substring(0, 30)}...`);
        
        // 构建请求数据
        const requestData = {
          image: imageData,
          student_id: studentId,
          student_name: studentName,
          class_id: classId
        };
        
        console.log("发送注册请求...");
        const response = await axios.post('/api/register_face', requestData);
        console.log("注册请求响应:", response.data);
        
        commit('SET_ERROR', null);
        return response.data;
      } catch (error) {
        const errorMsg = '人脸注册失败：' + error.message;
        console.error(errorMsg, error);
        
        // 如果有响应数据，输出更详细的错误信息
        if (error.response) {
          console.error('错误响应状态:', error.response.status);
          console.error('错误响应数据:', error.response.data);
        }
        
        commit('SET_ERROR', errorMsg);
        return { 
          success: false, 
          message: errorMsg,
          originalError: error.toString(),
          responseData: error.response ? error.response.data : null
        };
      } finally {
        commit('SET_LOADING', false);
      }
    },
    setLivenessMethod({ commit }, method) {
      commit('SET_LIVENESS_METHOD', method)
    }
  },
  getters: {
    isLoading: state => state.loading,
    error: state => state.error,
    attendanceRecords: state => state.attendanceRecords,
    classInfo: state => state.classInfo,
    livenessMethod: state => state.livenessMethod,
    lastDetectionResult: state => state.lastDetectionResult
  },
  modules: {
  }
}) 