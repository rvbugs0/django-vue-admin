export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      tableType: 'vxe-table',
      rowKey: true, // 必须设置，true or false
      rowId: 'id',
      height: '100%', // 表格高度100%, 使用toolbar必须设置
      highlightCurrentRow: false
    },
    rowHandle: {
      view: {
        thin: true,
        text: "",
        disabled() {
          return !vm.hasPermissions("Retrieve")
        }
      },
      width: 230,
      edit: {
        thin: true,
        text: "",
        disabled() {
          return !vm.hasPermissions("Update");
        }
      },
      remove: {
        thin: true,
        text: "",
        disabled( ) {
          return !vm.hasPermissions("Delete");
        },
      }
    },
    indexRow: {
      // 或者直接传true,不显示title，不居中
      title: "S.No.",
      align: "center",
      width: 100,
    },

    viewOptions: {
      componentType: "form",
    },
    formOptions: {
      defaultSpan: 24, // 默认的表单 span
      width: "35%",
    },
    columns: [
      {
        title: "Keywords",
        key: "search",
        show: false,
        disabled: true,
        search: {
          disabled: false,
        },
        form: {
          disabled: true,
          component: {
            props: {
              clearable: true,
            },
            placeholder: "Please enter a keyword",
          },
        },
        view: {
          // 查看对话框组件的单独配置
          disabled: true,
        },
      },
      {
        title: "ID",
        key: "id",
        show: false,
        width: 90,
        form: {
          disabled: true,
        },
      },

      {
        title: "Title",
        key: "title",
        sortable: true,
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true,
            },
          },
        },

        type: "input",
        form: {
          rules: [
            // 表单校验规则
            { required: true, message: "Title is required" },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "Please enter a title",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: "Exposed",
        key: "public_exposed",
        search: {
          disabled: false,
          title: "Exposed",
        },
        type: "select",
        form: {
          rules: [
            // 表单校验规则
            { required: true, message: "selection required" },
          ],
          component: {
            props: {
              filterable: true,
              multiple: false,
              clearable: true,
            },
          },
        },
        dict: {
          data: [
            { value: "false", label: "False" },
            { value: "true", label: "True" },
          ],
        },
      },
      {
        title: "Sensory attribute",
        key: "entity",
        search : {},
        type: "select",

        form: {
          rules: [{ required: true, message: 'Please select' }],
          component: { 
            props: { 
              filterable: true, 
              multiple: false, 
              clearable: true 
            }
          }
        },
        dict: {  
          data: [
            { value: 'sea_water_temperature_c', label: 'Sea Water Temperature' },
            { value: 'salinity', label: 'Salinity' },
            { value: 'ph', label: 'pH' },
            { value: 'dissolved_oxygen', label: 'Dissolved Oxygen' }
           
          ]
        },
      },
      {
        title: "Chart type",
        key: "type",
        search : {},
        type: "select",

        form: {
          rules: [{ required: true, message: 'Required' }],
          component: { //添加和修改时form表单的组件，支持任何v-model组件
            props: { //配置自定义组件的属性
              filterable: true, //可过滤选择项
              multiple: false, //支持多选
              clearable: true //可清除
            }
          }
        },
        dict: {  //本地数据字典
          data: [
            { value: 'bar', label: 'Bar chart' },
            { value: 'line', label: 'Line chart' },
            { value: 'area', label: 'Area chart' },
            { value: 'scroll_chart', label: 'Scrollable Line chart' },
           
          ]
        },
      }, {
        title: "Function type",
        key: "function_type",
        search : {},
        type: "select",

        form: {
          rules: [{ required: true, message: 'Required' }],
          component: { 
            props: { 
              filterable: true, 
              multiple: false, 
              clearable: true 
            }
          }
        },
        dict: {  
          data: [
            { value: 'monthly_average', label: 'Monthly Average' },
            { value: 'monthly_max', label: 'Monthly Maximum Value' },
            { value: 'monthly_min', label: 'Monthly Minimum Value' },
            { value: 'plain_value', label: 'Plain value' },
           
          ]
        },
      },{
        title: "Start Date",
        key: "start_date",
        sortable: true,
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
  
        type: 'date',
        form: {
          rules: [ // form validation rules
            { required: true, message: 'Required' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: 'Please enter start date'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        },
      },
      {
        title: "End Date",
        key: "end_date",
        sortable: true,
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
  
        type: 'date',
        form: {
          rules: [ // form validation rules
            { required: true, message: 'Required' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: 'Please enter end date'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        } ,
      },
      

    ]
  }
}
