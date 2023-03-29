import layoutHeaderAside from '@/layout/header-aside'
import { checkPlugins } from '@/views/plugins/index.js'
// Since there are too many lazy loaded pages, the hot update of webpack will be too slow, so the development environment does not use lazy loading, only the production environment uses lazy loading
const _import = require('@/libs/util.import.' + process.env.NODE_ENV)
const pluginImport = require('@/libs/util.import.plugin')
/**
  * Displayed within the main frame
  */
const frameIn = [{
   path: '/',
   redirect: { name: 'index' },
   component: layoutHeaderAside,
   children: [
     // console
     {
       path: 'index',
       name: 'index',
       meta: {
         auth: true
       },
       component:_import('dashboard/workbench/index')
     },
     {
       path: 'userInfo',
       name: 'userInfo',
       meta: {
         title: 'Personal Information',
         auth: true
       },
       component: () => import('@/layout/header-aside/components/header-user/userinfo')
     },
     // dashboard workbench
     {
       path: 'workbench',
       name: 'workbench',
       meta: {
         title: 'Workbench',
         auth: true
       },
       component:_import('dashboard/workbench')
     },
     // Refresh the page must be kept
     {
       path: 'refresh',
       name: 'refresh',
       hidden: true,
       component:_import('system/function/refresh')
     },
     // Page redirection must be preserved
     {
       path: 'redirect/:route*',
       name: 'redirect',
       hidden: true,
       component:_import('system/function/redirect')
     }
   ]
}]

/**
  * displayed outside the main frame
  */
const frameOut = [
   // Log in
   {
     path: '/login',
     name: 'login',
     component:_import('system/login')
   }
]
/**
  * Sign in with
  */
const pluginsType = checkPlugins('dvadmin-oauth2-web')
if (pluginsType) {
   frameOut. push({
     path: '/oauth2',
     name: 'login',
     component: pluginsType === 'local' ? _import('plugins/dvadmin-oauth2-web/src/login/index') : pluginImport('dvadmin-oauth2-web/src/login/index')
   })
}
/**
  * error page
  */
const errorPage = [{
   path: '/404',
   name: '404',
   component:_import('system/error/404')
}]

// Export the menu that needs to be displayed
export const frameInRoutes = frameIn

// export after reorganization
export default [
   ...frameIn,
   ...frameOut,
   ...errorPage
]