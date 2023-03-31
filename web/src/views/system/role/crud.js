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
      },
      custom: [{
        show (index, row) {
          return true
        },
        disabled () {
          return !vm.hasPermissions('Update')
        },
        text: 'authority management',
        type: 'warning',
        size: 'small',
        emit: 'createPermission'
      }]

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
          props: {
            clearable: true
          },
          placeholder: 'Please enter a keyword'
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
      title: 'Role Name',
      key: 'name',
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
          { required: true, message: 'Role name is required' }
        ],
        component: {
          props: {
            clearable: true
          },
          placeholder: 'Please enter a role name'
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    },
    {
      title: 'Authority ID',
      key: 'key',
      sortable: true,
      form: {
        rules: [ // 表单校验规则
          { required: true, message: 'Authorization ID required' }
        ],
        component: {
          props: {
            clearable: true
          },
          placeholder: 'Please enter the identification characters'
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    }, {
      title: 'Sort',
      key: 'sort',
      sortable: true,
      width: 80,
      type: 'number',
      form: {
        value: 1,
        component: {
          placeholder: 'Please enter sort'
        }
      }
    },
    {
      title: 'Are you an administrator',
      key: 'admin',
      sortable: true,
      type: 'radio',
      dict: {
        data: vm.dictionary('button_whether_bool')
      },
      form: {
        value: false,
        component: {
          placeholder: 'Please choose whether to be an administrator',
          show (context) {
            return vm.info.is_superuser
          }
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
      type: 'radio',
      dict: {
        data: vm.dictionary('button_status_bool')
      },
      form: {
        value: true,
        component: {
          placeholder: 'Please select a status'
        }
      },
      component: { props: { color: 'auto' } }
    }
    ].concat(vm.commonEndColumns())
  }
}
