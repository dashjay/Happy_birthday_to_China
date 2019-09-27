import baidu from '@/components/baidu'
import chineseMap from '@/components/chineseMap'
import map from '@/components/map'
import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {path: '/', name: 'map', component: map},
    {path: '/chinese', name: 'chinesemap', component: chineseMap},
    {path: '/baidu', name: 'baidu', component: baidu}
  ]
})
