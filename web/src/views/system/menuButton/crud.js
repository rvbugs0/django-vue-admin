/*
  * @Create file time: 2021-06-03 00:50:28
  * @Auther: Ape Xiaotian
  * @last modified by: Yuan Xiaotian
  * @last modification time: 2021-07-29 22:49:02
  * Contact Qq:1638245306
  * @file introduction: menu button and interface configuration
  */
import { request } from '@/api/service'
export const crudOptions = (vm) => {
   return {
     pageOptions: {
       compact: true
     },
     options: {
       tableType: 'vxe-table',
       rowKey: false,
       width: '100%',
       height: '100%' // table height 100%, must be set when using toolbar
     },
     rowHandle: {
       width: 180,
       edit: {
         thin: true,
         text: 'edit'
       },
       remove: {
         thin: true,
         text: 'remove'
       }
     },
     indexRow: { // Or pass true directly, do not display title, do not center
       title: 'S.No.',
       align: 'center',
       width: 100
     },
     viewOptions: {
       disabled: true,
       componentType: 'form'
     },
     formOptions: {
       defaultSpan: 24 // default form span
     },
     columns: [{
       title: 'Key words',
       key: 'search',
       show: false,
       disabled: true,
       search: {
         disabled: false,
         component: {
           props: {
             clearable: true
           },
           placeholder: 'Please enter a keyword'
         }
       },
       form: {
         disabled: true
       },
       view: { // View the individual configuration of the dialog component
         disabled: true
       }
     },
     {
       title: 'ID',
       key: 'id',
       show: false,
       width: 90,
       form: {
         disabled: true
       }
     },

     {
       title: 'Permission name',
       key: 'name',
       sortable: true,
       width: 150,
       search: {
         disabled: false
       },
       type: 'select',
       dict: {
         data: vm.dictionary('system_button')
       },
       form: {
         rules: [ // form validation rules
           { required: true, message: 'required fields' }
         ],
         component: {
           span: 12,
           props: {
             clearable: true,
             elProps: {
               allowCreate: true,
               filterable: true,
               clearable: true
             }
           }
         },
         itemProps: {
           class: { yxtInput: true }
         },
         valueChange (key, value, form, { getColumn, mode, component, immediate, getComponent }) {
           if (value != null) {
             // console. log('component. dictOptions', component. dictOptions)
             const obj = component.dictOptions.find(item => {
               // console. log(item. label, value)
               return item. value === value
             })
             if (obj && obj. value) {
               form.name = obj.label
               form.value = obj.value
             }
           }
         },
         helper: {
           render(h) {
             return (< el-alert title="A new value not in the list can be entered manually" type="warning" description="The more commonly used suggestions are placed in dictionary management"/>
             )
           }
         }
       }
     },
     {
       title: 'permission value',
       key: 'value',
       sortable: true,
       width: 200,
       search: {
         disabled: false
       },
       type: 'input',
       form: {
         rules: [ // form validation rules
           { required: true, message: 'required fields' }
         ],
         component: {
           span: 12,
           placeholder: 'Please enter permission value',
           props: {
             elProps: {
               clearable: true
             }
           }
         },
         itemProps: {
           class: { yxtInput: true }
         },
         helper: {
           render(h) {
             return (< el-alert title="Judgment display for front-end button permissions" type="warning" description="How to use: vm.hasPermissions (permission value)"/>
             )
           }
         }
       }
     },
     {
      title: 'Request method',
      key: 'method',
      sortable: true,
      width: 150,
      search: {
        disabled: false
      },
      type: 'select',
      dict: {
        data: [
          { label: 'GET', value: 0 },
          { label: 'POST', value: 1 },
          { label: 'PUT', value: 2 },
          { label: 'DELETE', value: 3 }
        ]
      },
      form: {
        rules: [ // form validation rules
          { required: true, message: 'required fields' }
        ],
        component: {
          span: 12
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    },
    {
      title: 'interface address',
      key: 'api',
      sortable: true,
      search: {
        disabled: true
      },
      type: 'select',
      dict: {
        url: '/swagger.json',
        label: 'label',
        value: 'value',
        getData: (url, dict) => {
          return request({ url: url }).then(ret => {
            const res = Object. keys(ret. paths)
            const data = []
            for (const item of res) {
              const obj = {}
              obj.label = item
              obj.value = item
              data. push(obj)
            }

            return data
          })
        }
      },
      form: {
        rules: [ // form validation rules
          { required: true, message: 'required fields' }
        ],
        component: {
          span: 24,
          props: {
            elProps: {
              allowCreate: true,
              filterable: true,
              clearable: true
            }

          }
        },
        itemProps: {
          class: { yxtInput: true }
        },
        helper: {
          render(h) {
            return (< el-alert title="Please fill in correctly to avoid being intercepted when requesting. Match singletons using regular expressions, for example: /api/xx/.*?/" type="warning" />
            )
          }
        }
      }
    }
    ]
  }
}