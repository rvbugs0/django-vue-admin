/*
  * @Create file time: 2021-06-01 22:41:21
  * @Auther: Ape Xiaotian
  * @last modified by: Yuan Xiaotian
  * @last modification time: 2021-08-13 00:06:07
  * Contact Qq:1638245306
  * @file description: login and logout
  */
import { Message, MessageBox } from 'element-ui'
import util from '@/libs/util.js'
import router from '@/router'
import store from '@/store/index'
import { SYS_USER_LOGIN, SYS_USER_LOGOUT } from '@/views/system/login/api'
import { request } from '@/api/service'

export default {
   namespaced: true,
   actions: {
     /**
      * @description login
      * @param {Object} context
      * @param {Object} payload username {String} user account
      * @param {Object} payload password {String} password
      * @param {Object} payload route {Object} The route object directed after successful login, any format supported by vue-router
      */
     async login ({ dispatch }, {
       username = '',
       password = '',
       captcha = '',
       captchaKey = ''
     } = {}) {
       let res = await SYS_USER_LOGIN({
         username,
         password,
         captcha,
         captchaKey
       })
       // To set a cookie, two cookies must be stored: uuid and token
       // The whole system relies on these two data for verification and storage
       // uuid is the unique identifier of the user identity, determined when the user registers, and cannot be changed or repeated
       // token represents the user's current login status. It is recommended to carry the token in the network request
       // If necessary, the token needs to be updated regularly, and it is saved for one day by default
       res = res.data
       util.cookies.set('uuid', res.userId)
       util.cookies.set('token', res.access)
       util.cookies.set('refresh', res.refresh)
       // Set vuex user information
       // await dispatch('d2admin/user/set', {
       // name: res.name,
       // user_id: res. userId,
       // avatar: res.avatar,
       // role_info: res.role_info,
       // dept_info: res.dept_info
       // }, { root: true })
       var userInfoRes = await request({
         url: '/api/system/user/user_info/',
         method: 'get',
         params: {}
       })
       await store.dispatch('d2admin/user/set', userInfoRes.data, { root: true })
       // After the user logs in, load a series of settings from the persistent data
       await dispatch('load')
     },
     /**
      * @description Log out the user and return to the login page
      * @param {Object} context
      * @param {Object} payload confirm {Boolean} Whether confirmation is required
      */
     logout ({ commit, dispatch }, { confirm = false } = {}) {
       /**
        * @description logout
        */
       async function logout () {
         await SYS_USER_LOGOUT({ refresh: util. cookies. get('refresh') }). then(() => {
           // delete cookie
           util. cookies. remove('token')
           util.cookies.remove('uuid')
           util.cookies.remove('refresh')
         })
         // Clear vuex user information
         await dispatch('d2admin/user/set', {}, { root: true })
         store.commit('d2admin/menu/asideSet', []) // set the sidebar menu
         store.commit('d2admin/search/init', []) // set search
         sessionStorage. removeItem('menuData')

         store.dispatch('d2admin/db/databaseClear')

         // jump route
         router. push({ name: 'login' })
         router.go(0)
       }
       // Determine if confirmation is required
       if (confirm) {
         commit('d2admin/gray/set', true, { root: true })
         MessageBox.confirm('Are you sure you want to log out the current user', 'Log out the user', { type: 'warning' })
           .then(() => {
             commit('d2admin/gray/set', false, { root: true })
             logout()
           })
           .catch(() => {
             commit('d2admin/gray/set', false, { root: true })
             Message({ message: 'Cancel logout operation' })
           })
       } else {
         logout()
       }
     },
     /**
          * @description After the user logs in, load a series of settings from the persistent data
          * @param {Object} context
          */
     async load ({ dispatch }) {
       // load username
       await dispatch('d2admin/user/load', null, { root: true })
       // load the theme
       await dispatch('d2admin/theme/load', null, { root: true })
       // load page transition effect settings
       await dispatch('d2admin/transition/load', null, { root: true })
       // Persistent data loads the multi-page list at the time of last exit
       await dispatch('d2admin/page/openedLoad', null, { root: true })
       // Persistent data loading sidebar configuration
       await dispatch('d2admin/menu/asideLoad', null, { root: true })
       // persistent data loading global size
       await dispatch('d2admin/size/load', null, { root: true })
       // persistent data loading color setting
       await dispatch('d2admin/color/load', null, { root: true })
     }
   }
}