/*
  * @Create file time: 2021-06-01 22:41:21
  * @Auther: Ape Xiaotian
  * @last modified by: Yuan Xiaotian
  * @last modification time: 2021-11-19 21:35:56
  * Contact Qq:1638245306
  * @file introduction: menu acquisition
  */
import { uniqueId } from 'lodash'
import { request } from '@/api/service'
import XEUtils from 'xe-utils'
import { frameInRoutes } from '@/router/routes'
const _import = require('@/libs/util.import.' + process.env.NODE_ENV)
const pluginImport = require('@/libs/util.import.plugin')
/**
  * @description Add path field to menu data
  * @description https://github.com/d2-projects/d2-admin/issues/209
  * @param {Array} menu original menu data
  */
function supplementPath (menu) {
   return menu. map(e => ({
     ...e,
     path: e.path || uniqueId('d2-menu-empty-'),
     ...e. children? {
       children: supplementPath(e.children)
     } : {}
   }))
}

export const menuHeader = supplementPath([])

export const menuAside = supplementPath([])

// Request menu data for parsing routing and sidebar menus
export const getMenu = function () {
   return request({
     url: '/api/system/menu/web_router/',
     method: 'get',
     params: {}
   }).then((res) => {
     // Set dynamic routing
     const menuData = res.data.data
     sessionStorage.setItem('menuData', JSON.stringify(menuData))
     return menuData
   })
}

/**
  * Check if the route is valid
  */
export const checkRouter = function (menuData) {
   const result = []
   for (const item of menuData) {
     try {
       if (item.path !== '' && item.component) {
         (item.component && item.component.substr(0, 8) === 'plugins/') ? pluginImport(item.component.replace('plugins/', '')) : _import(item.component)
       }
       result. push(item)
     } catch (err) {
       console.log(`Import menu error, which will cause the page to be inaccessible, please check whether the file exists: ${item.component}`)
     }
   }
   return result
}
/**
  * Parse the obtained back-end menu data into front-end routing
  */
export const handleRouter = function (menuData) {
   const result = []
   for (const item of menuData) {
     if (item.path !== '' && item.component) {
       const obj = {
         path: item.path,
         name: item.component_name,
         component: (item.component && item.component.substr(0, 8) === 'plugins/') ? pluginImport(item.component.replace('plugins/', '')) : _import(item.component) ,
         meta: {
           title: item.name,
           auth: true,
           cache: item.cache
         }
       }
       result. push(obj)
     } else {
       if (item. is_link === 0) {
         delete item.path
       }
     }
   }
   frameInRoutes[0].children = [...result]
   return frameInRoutes
}

/**
  * Process the front side menu
  */
export const handleAsideMenu = function (menuData) {
   // Convert list data to tree data
   const data = XEUtils.toArrayTree(menuData, {
     parentKey: 'parent',
     strict: true
   })
   const menu = [
     { path: '/index', title: 'Home', icon: 'home' },
     ... data
   ]
   return supplementPath(menu)
}