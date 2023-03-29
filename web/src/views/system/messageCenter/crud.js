import { request } from '@/api/service'

export const crudOptions = (vm) => {
   return {
     indexRow: { // Or pass true directly, do not display title, do not center
       width: 60,
       title: 'serial number',
       align: 'center'
     },
     options: {
       tableType: 'vxe-table',
       rowKey: true, // must be set, true or false
       height: '100%' // table height 100%, must be set when using toolbar
     },
     rowHandle: {
       width: 160,
       fixed: 'right',
       view: false,
       edit: {
         thin: true,
         text: '',
         show () {
           return vm.tabActivted !== 'receive'
         },
         disabled () {
           return !vm.hasPermissions('Update')
         }
       },
       remove: {
         thin: true,
         text: '',
         show () {
           return vm.tabActivted !== 'receive'
         },
         disabled () {
           return !vm.hasPermissions('Delete')
         }
       },
       custom: [
         {
           thin: true,
           text: null,
           icon: 'el-icon-view',
           size: 'small',
           disabled () {
             return !vm.hasPermissions('Retrieve')
           },
           order: 1,
           emit: 'onView'
         }
       ]
     },
     columns: [
       {
         title: 'id',
         key: 'id',
         width: 100,
         form: { disabled: true }
       },
       {
         title: 'Title',
         key: 'title',
         search: {
           disabled: false
         },
         width: 200,
         form: {
           rules: [ // form validation rules
             {
               required: true,
               message: 'required fields'
             }
           ],
           component: { span: 24, placeholder: 'Please enter a title' }
         }
       },
       {
         title: 'Have you read',
         key: 'is_read',
         type: 'select',
         width: 100,
         show () {
           return vm.tabActivted === 'receive'
         },
         dict: {
           data: [
             { label: 'read', value: true, color: 'success' },
             { label: 'unread', value: false, color: 'danger' }
           ]
         },
         form: {
           disabled: true
         }
       },
       {
         title: 'Target Type',
         key: 'target_type',
         type: 'radio',
         width: 120,
         show () {
           return vm.tabActivted === 'send'
         },
         dict: { data: [{ value: 0, label: 'by user' }, { value: 1, label: 'by role' }, { value: 2, label: 'by department' }, { value: 3, label: 'Notice Announcement' }] },
         form: {
           component: {
             span: 24,
             props: {
               type: 'el-radio-button'
             }
           },
           rules: [
             {
               required: true,
               message: 'required',
               trigger: ['blur', 'change']
             }
           ]
         }
       },
       {
         title: 'Target User',
         key: 'target_user',
         search: {
           disabled: true
         },
         width: 130,
         type: 'table-selector',
         disabled: true,
         dict: {
           cache: false,
           url: '/api/system/user/',
           value: 'id', // attribute name of the value field in the data dictionary
           label: 'name', // attribute name of the label field in the data dictionary
           getData: (url, dict, {
             form,
             component
           }) => {
             return request({
               url: url,
               params: {
                 page: 1,
                 limit: 10
               }
             }).then(ret => {
               component._elProps.page = ret.data.page
               component._elProps.limit = ret.data.limit
               component._elProps.total = ret.data.total
               return ret.data.data
             })
           }
         },
         form: {
           rules: [ // form validation rules
             {
               required: true,
               message: 'required fields'
             }
           ],
           itemProps: {
             class: { yxtInput: true }
           },
           component: {
             span: 24,
             show (context) {
               return context.form.target_type === 0
             },
             pagination: true,
             props: { multiple: true },
             elProps: {
               columns: [
                 {
                   field: 'name',
                   title: 'Username'
                 },
                 {
                   field: 'phone',
                   title: 'User Phone'
                 }
               ]
             }
           }
         },
         component: {
           name: 'manyToMany',
           valueBinding: 'user_info',
           children: 'name'
         }
       },
       {
         title: 'Target role',
         key: 'target_role',
         search: {
           disabled: true
         },
         disabled: true,
         width: 130,
         type: 'table-selector',

         dict: {
          cache: false,
          url: '/api/system/role/',
          value: 'id', // attribute name of the value field in the data dictionary
          label: 'name', // attribute name of the label field in the data dictionary
          getData: (url, dict, {
            form,
            component
          }) => {
            return request({
              url: url,
              params: {
                page: 1,
                limit: 10
              }
            }).then(ret => {
              component._elProps.page = ret.data.page
              component._elProps.limit = ret.data.limit
              component._elProps.total = ret.data.total
              return ret.data.data
            })
          }
        },
        form: {
          rules: [ // form validation rules
            {
              required: true,
              message: 'required fields'
            }
          ],
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            span: 24,
            show (context) {
              return context.form.target_type === 1
            },
            pagination: true,
            props: { multiple: true },
            elProps: {
              columns: [
                {
                  field: 'name',
                  title: 'role name'
                },
                {
                  field: 'key',
                  title: 'Authorization ID'
                }
              ]
            }
          }
        },
        component: {
          name: 'manyToMany',
          valueBinding: 'role_info',
          children: 'name'
        }
      },
      {
        title: 'Target department',
        key: 'target_dept',
        search: {
          disabled: true
        },
        width: 130,
        type: 'table-selector',
        dict: {
          cache: false,
          url: '/api/system/dept/all_dept/',
          isTree: true,
          value: 'id', // attribute name of the value field in the data dictionary
          label: 'name', // attribute name of the label field in the data dictionary
          children: 'children', // attribute name of the children field in the data dictionary
          getData: (url, dict, {
            form,
            component
          }) => {
            return request({
              url: url
            }).then(ret => {
              return ret.data.data
            })
          }
        },
        disabled: true,
        form: {
          rules: [ // form validation rules
            {
              required: true,
              message: 'required fields'
            }
          ],
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            span: 24,
            show (context) {
              return context.form.target_type === 2
            },
            props: {
              multiple: true,
              elProps: {
                treeConfig: {
                  transform: true,
                  rowField: 'id',
                  parentField: 'parent',
                  expandAll: true
                },
                columns: [
                  {
                    field: 'name',
                    title: 'Department Name',
                    treeNode: true
                  },
                  {
                    field: 'status_label',
                    title: 'Status'
                  },
                  {
                    field: 'parent_name',
                    title: 'Parent Department'
                  }
                ]
              }
            }
          }
        },
        component: {
          name: 'manyToMany',
          valueBinding: 'dept_info',
          children: 'name'
        }
      },
      {
        title: 'Content',
        key: 'content',
        minWidth: 300,
        type: 'editor-quill', // rich text image upload depends on file-uploader, please configure file-uploader first
        form: {
          rules: [ // form validation rules
            {
              required: true,
              message: 'required fields'
            }
          ],
          component: {
            disabled: () => {
              return vm.getEditForm().disable
            },
            props: {
              uploader: {
                type: 'form' // Upload backend type [cos, aliyun, oss, form]
              }
            },
            events: {
              'text-change': (event) => {
                console.log('text-change:', event)
              }
            }
          }
        }
      }
    ].concat(vm.commonEndColumns({
      create_datetime: { showTable: true },
      update_datetime: { showTable: false }
    }))
  }
}