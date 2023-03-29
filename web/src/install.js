import Vue from 'vue'
// import d2Crud from '@d2-project/d2-crud'
import d2CrudX from 'd2-crud-x'
import { d2CrudPlus } from 'd2-crud-plus'
import {
   D2pAreaSelector,
   D2pDemoExtend,
   D2pFileUploader,
   D2pFullEditor,
   D2pIconSelector,
   D2pUploader
} from 'd2p-extends' // source code import, upload component supports lazy loading
// http request
import { request } from '@/api/service'
import util from '@/libs/util'
import XEUtils from 'xe-utils'
import store from '@/store/index'
import types from '@/config/d2p-extends/types'
import { checkPlugins, plugins } from '@/views/plugins'

/**
  // vxe0
  import 'xe-utils'
  import VXETable from 'vxe-table'
  import 'vxe-table/lib/index.css'
  Vue. use(VXETable)
  **/

// Imported by renaming as follows can coexist with the official version, the tag in index.vue uses <d2-crud-x /> to use the enhanced version
// If no name is passed, the tag of d2CrudX is still <d2-crud>, which cannot coexist with the official version
Vue.use(d2CrudX, { name: 'd2-crud-x' })
// Register the dvadmin plugin
Vue. use(plugins)
// // Official version [introduced here for the coexistence of demo and official version, d2-crud-x can be used to completely replace the official version in new projects]
// Vue. use(d2Crud)
/**
  * @description Check whether the plugin is installed
  * @param {String} pluginName plugin name
  */
Vue.prototype.checkPlugins = checkPlugins
// import d2CrudPlus
Vue.use(d2CrudPlus, {
   starTip: false,
   getRemoteDictFunc(url, dict) {
     // configure your dictionary http request method here
     // For actual use, please change it to request
     return request({
       url: url,
       params: dict.body,
       method: 'get'
     }).then(ret => {
       if (dict. isTree) {
         return XEUtils.toArrayTree(ret.data.data || ret.data, { parentKey: 'parent', strict: false })
       } else {
         return ret.data.data || ret.data
       }
     })
   },
   commonOption () { // common configuration
     return {
       format: {
         page: { // The data structure configuration returned by the page interface,
           request: {
             current: 'page',
             size: 'limit'
           },
           response: {
             current: 'page', // current page number ret.data.current
             size: 'limit', // current page number ret.data.current
             // size: (data) => { return data.size }, // the number of items per page, ret.data.size, you can also configure a method to customize the return
             total: 'total', // total number of records ret.data.total
             records: 'data' // list array ret.data.records
           }
         }
       },
       pageOptions: {
         compact: true
       },
       options: {
         size: 'small'
       },
       formOptions: {
         nullToBlankStr: true, // When submitting the modification form, modify the undefined data to an empty string '', which can solve the problem that the field cannot be emptied
         defaultSpan: 12, // default form span
         saveRemind: true,
         labelWidth: '110px'
       },
       viewOptions: {
         disabled: false,
         componentType: 'form' // [form, row] form component or row component display
       },
       rowHandle: {
         width: 260,
         edit: {
           type: 'primary'
         }
       }
     }
   }
})


// install the extension
// Vue. use(D2pTreeSelector)
Vue. use(D2pAreaSelector)
Vue.use(D2pIconSelector)
Vue.use(D2pFullEditor, {
   ueditor: {
     serverUrl: '/api/ueditor/'
   }
})
Vue.use(D2pDemoExtend)
Vue. use(D2pFileUploader)
Vue.use(D2pUploader, {
   defaultType: 'form',
   cos: {
     domain: 'https://d2p-demo-1251260344.cos.ap-guangzhou.myqcloud.com',
     bucket: 'd2p-demo-1251260344',
     region: 'ap-guangzhou',
     secretId: '', //
     secretKey: '', // pass the secretKey and secretId to represent the use of local signature mode (unsafe, not recommended for production environments)
     getAuthorization (custom) { // Do not pass the secretKey to use the temporary signature mode, and this parameter must be passed at this time (safe, recommended for production environments)
       return request({
         url: '/upload/cos/getAuthorization',
         method: 'get'
       }).then(ret => {
         // The return structure is as follows
         // ret. data: {
         // TmpSecretId,
         // TmpSecretKey,
         // XCosSecurityToken,
         // ExpiredTime, // SDK will not call getAuthorization again before ExpiredTime
         // }
         return ret.data
       })
     }
   },
   alioss: {
     domain: 'https://d2p-demo.oss-cn-shenzhen.aliyuncs.com',
     bucket: 'd2p-demo',
     region: 'oss-cn-shenzhen',
     accessKeyId: '',
     accessKeySecret: '',
     getAuthorization (custom, context) { // Do not pass accessKeySecret means to use temporary signature mode, this parameter must be passed at this time (safe, recommended for production environment)
       return request({
         url: '/upload/alioss/getAuthorization',
         method: 'get'
       }).then(ret => {
         return ret.data
       })
     },
     sdkOpts: { // sdk configuration
       secure: true // The default is non-https upload, for security, set to true
     }
   },
   Qiniu: {
     bucket: 'd2p-demo',
     getToken(custom) {
       return request({
         url: '/upload/qiniu/getToken',
         method: 'get'
       }).then(ret => {
         return ret.data // {token:xxx,expires:xxx}
       })
     },
     domain: 'http://d2p.file.veryreader.com'
   },
   form: {
     action: util. baseURL() + 'api/system/file/',
     name: 'file',
     data: {}, // Upload additional parameters
     headers () {
       return {
         Authorization: 'JWT' + util. cookies. get('token')
       }
     },
     type: 'form',
     successHandle (ret, option) {
       if (ret.data === null || ret.data === '') {
         throw new Error('Upload failed')
       }
       return { url: util.baseURL() + ret.data.url, key: option.data.key, id: ret.data.id }
     },
     withCredentials: false // Whether to bring cookies
   }
})
d2CrudPlus.util.columnResolve.addTypes(types)
// Modify the official field type
const selectType = d2CrudPlus.util.columnResolve.getType('select')
selectType.component.props.color = 'auto' // Modify the official field type and set it to support automatic coloring
// Get dictionary configuration
Vue.prototype.dictionary = function (name) {
   return store.state.d2admin.dictionary.data[name]
}
// Get the dictionary label value
Vue.prototype.getDictionaryLabel = function (name, value) {
   const data = store.state.d2admin.dictionary.data[name]
   if (data && data instanceof Array) {
     for (var i = 0, len = data. length; i < len; i++) {
       if (data[i]. value === value) {
         return data[i].label
       }
     }
     return ''
   }
   return store.state.d2admin.dictionary.data[name]
}
// Get system configuration
Vue.prototype.systemConfig = function (name) {
   return store.state.d2admin.settings.data[name]
}
// Default Columns end showForm: display in form, showTable: display in table
Vue.prototype.commonEndColumns = function (param = {}) {
   /**
    * @param {Object} {
     description: {
       showForm: true,
       showTable: false
     },
     dept_belong_id: {
       showForm: false,
       showTable: false
     },
     modifier_name: {
       showForm: false,
       showTable: false
     },
     update_datetime: {
       showForm: false,
       showTable: true
     },
     create_datetime: {
       showForm: false,
       showTable: true
     }
   }
   */
   const showData = {
    description: {
      showForm: (param.description && param.description.showForm) !== undefined ? param.description.showForm : true,
      showTable: (param.description && param.description.showTable) !== undefined ? param.description.showTable : false
    },
    dept_belong_id: {
      showForm: (param.dept_belong_id && param.dept_belong_id.showForm) !== undefined ? param.dept_belong_id.showForm : false,
      showTable: (param.dept_belong_id && param.dept_belong_id.showTable) !== undefined ? param.dept_belong_id.showTable : false,
      showSearch: (param.dept_belong_id && param.dept_belong_id.showSearch) !== undefined ? param.dept_belong_id.showSearch : false
    },
    modifier_name: {
      showForm: (param.modifier_name && param.modifier_name.showForm) !== undefined ? param.modifier_name.showForm : false,
      showTable: (param.modifier_name && param.modifier_name.showTable) !== undefined ? param.modifier_name.showTable : false
    },
    update_datetime: {
      showForm: (param.update_datetime && param.update_datetime.showForm) !== undefined ? param.update_datetime.showForm : false,
      showTable: (param.update_datetime && param.update_datetime.showTable) !== undefined ? param.update_datetime.showTable : true
    },
    creator_name: {
      showForm: (param.creator_name && param.creator_name.showForm) !== undefined ? param.creator_name.showForm : false,
      showTable: (param.creator_name && param.creator_name.showTable) !== undefined ? param.creator_name.showTable : false
    },
    create_datetime: {
      showForm: (param.create_datetime && param.create_datetime.showForm) !== undefined ? param.create_datetime.showForm : false,
      showTable: (param.create_datetime && param.create_datetime.showTable) !== undefined ? param.create_datetime.showTable : true
    }
  }
  return [
    {
      title: 'Remark',
      key: 'description',
      show: showData.description.showTable,
      search: {
        disabled: true
      },
      type: 'textarea',
      form: {
        disabled: !showData.description.showForm,
        component: {
          placeholder: 'Please enter content',
          showWordLimit: true,
          maxlength: '200',
          props: {
            type: 'textarea'
          }
        }
      }
    },
    {
      title: 'edited by',
      show: showData.modifier_name.showTable,
      width: 100,
      key: 'modifier_name',
      form: {
        disabled: !showData.modifier_name.showForm
      }
    },
    {
      title: 'Department',
      key: 'dept_belong_id',
      show: showData.dept_belong_id.showTable,
      width: 150,
      search: {
        disabled: !showData.dept_belong_id.showSearch
      },
      type: 'tree-selector',
      dict: {
        cache: false,
        url: '/api/system/dept/all_dept/',
        // isTree: true,
        // dept: true,
        value: 'id', // attribute name of the value field in the data dictionary
        label: 'name', // attribute name of the label field in the data dictionary
        children: 'children' // attribute name of the children field in the data dictionary
        // getData: (url, dict, {
        // _,
        // component
        // }) => {
        // return request({
        // url: url
        // }).then(ret => {
        // return XEUtils.toArrayTree(ret.data, { parentKey: 'parent', strict: false })
        // })
        // }
      },
      component: {
        name: 'dept-format',
        props: { multiple: false, clearable: true }
      },
      form: {
        disabled: !showData.dept_belong_id.showForm,
        component: {
          props: { multiple: false, clearable: true }
        },
        helper: {
          render(h) {
            return (< el-alert title="If it is not filled by default, it is the department ID of the current created user" type="info" />
            )
          }
        }
      },
      // When receiving, process the data
      valueBuilder (row, col) {
        if (row[col. key]) {
          row[col.key] = Number(row[col.key])
        }
      }
    },
    {
      title: 'Update time',
      key: 'update_datetime',
      width: 160,
      show: showData.update_datetime.showTable,
      type: 'datetime',
      sortable: true,
      form: {
        disabled: !showData.update_datetime.showForm
      }
    },
    {
      title: 'Creation time',
      key: 'create_datetime',
      width: 160,
      search: {
        disabled: !showData.create_datetime.showForm,
        width: 240,
        component: { // Query box component configuration, generated according to form configuration by default
          name: 'el-date-picker',
          props: {
            type: 'daterange',
            'range-separator': 'to',
            'start-placeholder': 'start',
            'end-placeholder': 'end',
            valueFormat: 'yyyy-MM-dd'
          }
        }
      },
      show: showData.create_datetime.showTable,
      type: 'datetime',
      sortable: true,
      form: {
        disabled: !showData.create_datetime.showForm
      }
    }
  ]
}