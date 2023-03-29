import * as api from './api'
export const crudOptions = (vm) => {
   return {
     pageOptions: {
       compact: true
     },
     pagination: false,
     options: {
       tableType: 'vxe-table',
       stripe: false,
       rowKey: true, // must be set, true or false
       rowId: 'id',
       height: '100%', // table height 100%, must be set when using toolbar
       highlightCurrentRow: false,
       defaultExpandAll: true,
       treeConfig: {
         transform: true,
         rowField: 'id',
         parentField: 'parent',
         hasChild: 'hasChild',
         lazy: true,
         loadMethod: ({ row }) => {
           return api.GetList({ parent: row.id }).then(ret => {
             return ret.data.data
           })
         },
         iconLoaded: 'el-icon-loading' // Beautify the loading icon
       }
     },
     rowHandle: {
       width: 140,
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
       }
     },
     indexRow: {
       // Or pass true directly, do not display title, do not center
       title: 'serial number',
       align: 'center',
       width: 100
     },

     viewOptions: {
       componentType: 'form'
     },
     formOptions: {
       defaultSpan: 12 // default form span
     },
     columns: [
       {
         title: 'Keywords',
         key: 'search',
         show: false,
         disabled: true,
         search: {
           disabled: false
         },
         form: {
           disabled: true,
           component: {
             props: {
               clearable: true
             },
             placeholder: 'Please enter keywords'
           }
         },
         view: {
           // View the individual configuration of the dialog component
           disabled: true
         }
       },
       {
         title: 'ID',
         key: 'id',
         show: false,
         disabled: true,
         width: 90,
         form: {
           disabled: true
         }
       },
       {
         show: false,
         title: 'Superior department',
         key: 'parent',
         type: 'tree-selector',
         dict: {
           isTree: true,
           label: 'name',
           value: 'id',
           cache: false,
           getData: (url, dict, { form, component }) => { // Configuring this parameter will override the global getRemoteDictFunc
             return api. DeptLazy(). then(ret => { return ret })
           }
         },
         form: {
           helper: 'Leave blank by default as the creator\'s department',
           component: {
             span: 12,
             props: {
               multiple: false
             }
           }
         }
       },
       {
         title: 'Department Name',
         key: 'name',
         sortable: true,
         treeNode: true, // set as a tree column
         search: {
           disabled: false,
           component: {
             props: {
               clearable: true
             }
           }
         },
         width: 180,
         type: 'input',
         form: {
           rules: [
             // form validation rules
             { required: true, message: 'Department name is required' }
           ],
           component: {
             span: 12,
             props: {
               clearable: true
             },
             placeholder: 'Please enter the department name'
           },
           itemProps: {
             class: { yxtInput: true }
           }
         }
       },
       {
         title: 'Department ID',
         key: 'key',
         sortable: true,
         form: {
           component: {
             props: {
               clearable: true
             },
             placeholder: 'Please enter the identification character'
           },
           itemProps: {
             class: { yxtInput: true }
           }
         }
       },
       {
         title: 'Responsible person',
         key: 'owner',
         sortable: true,
         form: {
           component: {
             span: 12,
             props: {
               clearable: true
             },
             placeholder: 'Please enter the person in charge'
           }
         }
       },
       {
         title: 'Contact number',
         key: 'phone',
         sortable: true,
         form: {
           component: {
             span: 12,
             props: {
               clearable: true
             },
             placeholder: 'Please enter a contact number'
           }
         }
       },
       {
         title: 'Mailbox',
         key: 'email',
         sortable: true,
         form: {
           component: {
             span: 12,
             props: {
               clearable: true
             },
             placeholder: 'Please enter your email address'
           },
           rules: [
             {
               type: 'email',
               message: 'Please enter a correct email address',
               trigger: ['blur', 'change']
             }
           ]
         }
       },
       {
         title: 'sort',
         key: 'sort',
         sortable: true,
         width: 80,
         type: 'number',
         form: {
           value: 1,
           component: {
             span: 12,
             placeholder: 'Please select a serial number'
           }
         }
       },
       {
         title: 'Status',
         key: 'status',
         sortable: true,
         search: {
           disabled: false
         },
         width: 90,
         type: 'radio',
         dict: {
           data: vm.dictionary('button_status_bool')
         },
         form: {
           value: true,
           component: {
             span: 12,
             placeholder: 'Please select a status'
           }
         }
       }
     ].concat(vm.commonEndColumns())
   }
}