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
      rowKey: true, // 必须设置，true or false
      rowId: 'id',
      height: '100%', // 表格高度100%, 使用toolbar必须设置
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
        iconLoaded: 'el-icon-loading' // 美化loading图标
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
      // 或者直接传true,不显示title，不居中
      title: 'S.No.',
      align: 'center',
      width: 100
    },

    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 12 // 默认的表单 span
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
          // 查看对话框组件的单独配置
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
        title: 'Superior Department',
        key: 'parent',
        type: 'tree-selector',
        dict: {
          isTree: true,
          label: 'name',
          value: 'id',
          cache: false,
          getData: (url, dict, { form, component }) => { // 配置此参数会覆盖全局的getRemoteDictFunc
            return api.DeptLazy().then(ret => { return ret })
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
        title: 'Department name',
        key: 'name',
        sortable: true,
        treeNode: true, // 设置为树形列
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
            // 表单校验规则
            { required: true, message: 'Department name required' }
          ],
          component: {
            span: 12,
            props: {
              clearable: true
            },
            placeholder: 'Please enter department name'
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
        title: 'Contact Number',
        key: 'phone',
        sortable: true,
        form: {
          component: {
            span: 12,
            props: {
              clearable: true
            },
            placeholder: 'Please enter a contact no.'
          }
        }
      },
      {
        title: 'Email',
        key: 'email',
        sortable: true,
        form: {
          component: {
            span: 12,
            props: {
              clearable: true
            },
            placeholder: 'Please enter your email'
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
        title: 'Sort',
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
    ]
    // .concat(vm.commonEndColumns())
  }
}
