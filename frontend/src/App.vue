<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>人脸识别考勤系统</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon @click="toggleDarkMode">
        <v-icon>{{ isDarkMode ? 'mdi-white-balance-sunny' : 'mdi-weather-night' }}</v-icon>
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app temporary>
      <v-list-item>
        <v-list-item-avatar>
          <v-img src="@/assets/logo.png"></v-img>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title class="text-h6">人脸识别考勤系统</v-list-item-title>
          <v-list-item-subtitle>班级考勤管理</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list dense nav>
        <v-list-item v-for="item in menuItems" :key="item.title" :to="item.path" link>
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-footer app>
      <span>&copy; {{ new Date().getFullYear() }} - 人脸识别考勤系统</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  data: () => ({
    drawer: false,
    isDarkMode: false,
    menuItems: [
      { title: '首页', path: '/', icon: 'mdi-home' },
      { title: '考勤打卡', path: '/attendance', icon: 'mdi-account-check' },
      { title: '人脸注册', path: '/register', icon: 'mdi-account-plus' },
      { title: '考勤记录', path: '/records', icon: 'mdi-clipboard-text' },
      { title: '班级管理', path: '/classes', icon: 'mdi-account-group' },
      { title: '系统设置', path: '/settings', icon: 'mdi-cog' }
    ]
  }),
  methods: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      this.$vuetify.theme.dark = this.isDarkMode;
    }
  }
};
</script> 