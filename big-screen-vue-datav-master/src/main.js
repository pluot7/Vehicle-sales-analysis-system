import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import dataV from '@jiaminghi/data-view';
// 引入全局css
import './assets/scss/style.scss';
// 按需引入vue-awesome图标
import Icon from 'vue-awesome/components/Icon';
import 'vue-awesome/icons/chart-bar.js';
import 'vue-awesome/icons/chart-area.js';
import 'vue-awesome/icons/chart-pie.js';
import 'vue-awesome/icons/chart-line.js';
import 'vue-awesome/icons/align-left.js';

import $http from '@/api/index.js';

//引入echart
import echarts from 'echarts'

Vue.prototype.$echarts = echarts
Vue.config.productionTip = false;

// 修复这里：直接赋值，不要调用函数
Vue.prototype.$http = $http

// 全局注册
Vue.component('icon', Icon);
Vue.use(dataV);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');