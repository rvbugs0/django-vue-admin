import { request } from '@/api/service'
import util from '@/libs/util'

export const crudOptions = (vm) => {
   util.filterParams(vm, ['dept_name', 'role_info{name}', 'dept_name_all'])
   return {
     pageOptions: {
       compact: true
     },
     options: {
       height: '100%',
       tableType: 'vxe-table',
       rowKey: true,
       rowId: 'id'
     },
     selectionRow: {
       align: 'center',
       width: 46
     },
     rowHandle: {
       width: 240,
       fixed: 'right',
       view: {
         thin: true,
         text: '',
         disabled () {
           return !vm.hasPermissions('Retrieve')
         }
       },
       edit: {
         thin: true,
         text: '',
         disabled () {
           return !vm.hasPermissions('Update')
         }
       },
       remove: {
         thin: true,
         text: '',
         disabled () {
           return !vm.hasPermissions('Delete')
         }
       },
       custom: [
         {
           thin: true,
           text: 'reset Password',
           size: 'small',
           type: 'warning',
           icon: 'el-icon-refresh-left',
           show () {
             return vm.hasPermissions('ResetPassword')
           },
           emit: 'resetPassword'
         }
       ]
     },
     viewOptions: {
       componentType: 'form'
     },
     formOptions: {
       defaultSpan: 12 // default form span
     },
     indexRow: { // Or pass true directly, do not display title, do not center
       title: 'S.no.',
       align: 'center',
       width: 60
     },
     columns: [
       {
         title: 'Key words',
         key: 'search',
         show: false,
         disabled: true,
         search: {
           disabled: false
         },
         form: {
           disabled: true,
           component: {
             placeholder: 'Please enter a keyword'
           }
         },
         view: {
           disabled: true
         }
       },
       {
         title: 'ID',
         key: 'id',
         disabled: true,
         form: {
           disabled: true
         }
       },
       {
         title: 'Username',
         key: 'username',
         search: {
           disabled: false
         },
         minWidth: 100,
         type: 'input',
         form: {
           rules: [ // form validation rules
             {
               required: true,
               message: 'Username Required'
             }
           ],
           component: {
             placeholder: 'Please input Username'
           },
           itemProps: {
             class: { yxtInput: true }
           }
         }
       },
       {
         title: 'password',
         key: 'password',
         minWidth: 90,
         type: 'input',
         form: {
           rules: [ // form validation rules
             {
               required: true,
               message: 'password required'
             }
           ],
           component: {
             span: 12,
             showPassword: true,
             placeholder: 'Please enter a password'
           },
           value: vm.systemConfig('base.default_password'),
           editDisabled: true,
           itemProps: {
             class: { yxtInput: true }
           }
         },
         disabled: true,
         valueResolve(row, key) {
           if (row. password) {
             row.password = vm.$md5(row.password)
           }
         }
       },
       {
         title: 'Name',
         key: 'name',
         minWidth: 90,
         search: {
           disabled: false
         },
         type: 'input',
         form: {
           rules: [ // form validation rules
             {
               required: true,
               message: 'Name is required'
             }
           ],
           component: {
             span: 12,
             placeholder: 'Please enter your name'
           },
           itemProps: {
             class: { yxtInput: true }
           }
         }
       },
       {
         title: 'Department',
         key: 'dept',
         search: {
           disabled: true
         },
         minWidth: 140,
         type: 'tree-selector',
         dict: {
           cache: true,
           isTree: true,
           url: '/api/system/dept/all_dept/',
           value: 'id', // attribute name of the value field in the data dictionary
           label: 'name' // attribute name of the label field in the data dictionary
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
             span: 12,
             pagination: true,


             props: { multiple: false }
            }
          },
          component: {
            name: 'foreignKey',
            valueBinding: 'dept_name'
          }
        },
        {
          title: 'Role',
          key: 'role',
          search: {
            disabled: true
          },
          minWidth: 130,
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
              span: 12,
              pagination: true,
              props: { multiple: true },
              elProps: {
                columns: [
                  {
                    field: 'name',
                    title: 'Role name'
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
          title: 'Mobile phone number',
          key: 'mobile',
          search: {
            disabled: false
          },
          minWidth: 110,
          type: 'input',
          form: {
            rules: [
              {
                max: 20,
                message: 'Please enter the correct mobile number',
                trigger: 'blur'
              },
              {
                pattern: /^1[3-9]\d{9}$/,
                message: 'Please enter a correct mobile number'
              }
            ],
            itemProps: {
              class: { yxtInput: true }
            },
            component: {
              placeholder: 'Please enter your phone number'
            }
          }
        }, {
          title: 'Mailbox',
          key: 'email',
          minWidth: 180,
          form: {
            rules: [
              {
                type: 'email',
                message: 'Please enter a correct email address',
                trigger: ['blur', 'change']
              }
            ],
            component: {
              placeholder: 'Please enter your email address'
            }
          }
        },
        {
          title: 'Gender',
          key: 'gender',
          type: 'radio',
          width: 70,
          dict: {
            data: vm.dictionary('gender')
          },
          form: {
            value: 1,
            component: {
              span: 12
            }
          },
          component: { props: { color: 'auto' } } // automatic coloring
        }, {
          title: 'User Type',
          key: 'user_type',
          search: {
            disabled: false
          },
          width: 145,
          type: 'select',
          dict: {
            data: vm.dictionary('user_type')
          },
          form: {
            show: false,
            value: 0,
            component: {
              span: 12
            }
          }
        }, {
          title: 'Status',
          key: 'is_active',
          search: {
            disabled: false
          },
          width: 70,
          type: 'radio',
          dict: {
            data: vm.dictionary('button_status_bool')
          },
          form: {
            value: true,
            component: {
              span: 12
            }
          }
        },
        {
          title: 'Avatar',
          key: 'avatar',
          type: 'avatar-cropper',
          width: 60,
          align: 'left',
          form: {
            component: {
              props: {
                elProps: { // Consistent with el-uploader configuration
                  multiple: false,
                  limit: 1 // limit 5 files
                },
                sizeLimit: 500 * 1024 // cannot exceed the limit
              },
              span: 24
            },
            helper: 'Restrict file size to 500k'
          }
        }
      ].concat(vm.commonEndColumns({
        create_datetime: { showTable: false },
        update_datetime: { showTable: false }
      }))
    }
 }