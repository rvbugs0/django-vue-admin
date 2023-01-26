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
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      width: 230,
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
    indexRow: { // 或者直接传true,不显示title，不居中
      title: 'S.No.',
      align: 'center',
      width: 100
    },

    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 24, // 默认的表单 span
      width: '35%'
    },
    columns: [{
      title: '关键词',
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
          placeholder: '请输入关键词'
        }
      },
      view: { // 查看对话框组件的单独配置
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
      title: 'Sea water Temperature (C)',
      key: 'sea_water_temperature_c',
      sortable: true,
      search: {
        disabled: false,
        component: {
          props: {
            clearable: true
          }
        }
      },

      type: 'input',
      form: {
        rules: [ // 表单校验规则
          { required: true, message: '角色名称必填项' }
        ],
        component: {
          props: {
            clearable: true
          },
          placeholder: '请输入角色名称'
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    },
    {
      title: 'Salinity',
      key: 'salinity',
      sortable: true,
      search: {
        disabled: false,
        component: {
          props: {
            clearable: true
          }
        }
      },

      type: 'input',
      form: {
        rules: [ // 表单校验规则
          { required: true, message: '角色名称必填项' }
        ],
        component: {
          props: {
            clearable: true
          },
          placeholder: '请输入角色名称'
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    }, 
    {
      title: 'pH',
      key: 'ph',
      sortable: true,
      search: {
        disabled: false,
        component: {
          props: {
            clearable: true
          }
        }
      },

      type: 'input',
      form: {
        rules: [ // 表单校验规则
          { required: true, message: '角色名称必填项' }
        ],
        component: {
          props: {
            clearable: true
          },
          placeholder: '请输入角色名称'
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    },

    {
      title: 'Dissolved Oxygen',
      key: 'dissolved_oxygen',
      sortable: true,
      search: {
        disabled: false,
        component: {
          props: {
            clearable: true
          }
        }
      },

      type: 'input',
      form: {
        rules: [ // 表单校验规则
          { required: true, message: '角色名称必填项' }
        ],
        component: {
          props: {
            clearable: true
          },
          placeholder: '请输入角色名称'
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    },
    {
      title: 'Date Recorded',
      key: 'date_recorded',
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
        rules: [ // 表单校验规则
          { required: true, message: '角色名称必填项' }
        ],
        component: {
          props: {
            clearable: true
          },
          placeholder: '请输入角色名称'
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    }
    ].concat(vm.commonEndColumns())
  }
}
