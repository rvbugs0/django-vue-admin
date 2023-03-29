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
         text: 'Delete'
       }
     },
     indexRow: { // Or pass true directly, do not display title, do not center
       title: 'serial number',
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
             placeholder: 'Please enter keywords'
           }
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
         title: 'Request method',
         key: 'method',
         sortable: true,
         search: {
           disabled: false
         },
         type: 'select',
         dict: {
           data: [
             {
               label: 'GET',
               value: 0
             },
             {
               label: 'POST',
               value: 1
             },
             {
               label: 'PUT',
               value: 2
             },
             {
               label: 'DELETE',
               value: 3
             }
           ]
         },
         form: {
           rules: [ // form validation rules
             {
               required: true,
               message: 'required fields'
             }
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
         title: 'Interface address',
         key: 'url',
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
             {
               required: true,
               message: 'required fields'
             }
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
               return (< el-alert title="Please fill in correctly to avoid being intercepted when requesting. Matching singletons use regular expressions, for example: /api/xx/.*?/" type="warning"/>
               )
             }
           }
         }
       },
       {
         title: 'Data Authority Authentication',
         key: 'enable_datasource',
         search: {
           disabled: false
         },
         width: 150,
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
         title: 'Remarks',
         key: 'description',
         search: {
           disabled: true
         },
         type: 'textarea',
         form: {
           component: {
             placeholder: 'Please enter content',
             showWordLimit: true,
             maxlength: '200',
             props: {
               type: 'textarea'
             }
           }
         }
       }
     ]
   }
}