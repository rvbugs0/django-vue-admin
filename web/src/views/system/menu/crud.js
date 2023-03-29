import { request } from '@/api/service'
import { urlPrefix as menuPrefix } from './api'
import XEUtils from 'xe-utils'
export const crudOptions = (vm) => {
  // 验证路由地址
  const validateWebPath = (rule, value, callback) => {
    const isLink = vm.getEditForm().is_link
    let pattern = /^\/.*?/
    if (isLink) {
      pattern = /^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+/g
    } else {
      pattern = /^\/.*?/
    }
    if (!pattern.test(value)) {
      callback(new Error('correct address please'))
    } else {
      callback()
    }
  }
  return {
    pagination: false,
    pageOptions: {
      compact: true
    },
    options: {
      tableType: 'vxe-table',
      rowKey: true,
      rowId: 'id',
      height: '100%', // 表格高度100%, 使用toolbar必须设置
      highlightCurrentRow: false,
      // defaultExpandAll: true,
      // expandAll: true,
      treeConfig: {
        transform: true,
        rowField: 'id',
        parentField: 'parent',
        expandAll: true,
        hasChild: 'hasChild',
        lazy: true,
        loadMethod: vm.loadContentMethod
      }
    },
    rowHandle: {
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
      width: 230,
      fixed: 'right',
      custom: [{
        show (index, row) {
          if (row.web_path && !row.is_link) {
            return true
          }
          return false
        },
        disabled () {
          return !vm.hasPermissions('Update')
        },
        text: ' Menu Button',
        type: 'warning',
        size: 'small',
        emit: 'createPermission'
      }]

    },
    indexRow: { // 或者直接传true,不显示title，不居中
      title: 'Serial No.',
      align: 'center',
      width: 80
    },
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 12 // 默认的表单 span
    },
    columns: [
      {
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
            placeholder: '请输入关键词'
          }
        },
        form: {
          disabled: true,
          component: {
            props: {
              clearable: true
            }
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
        width: 60,
        form: {
          component: {
            show: false
          }
        }
      },
      {
        title: 'Parent menu',
        key: 'parent',
        show: false,
        search: {
          disabled: true
        },
        type: 'cascader',
        dict: {
          url: menuPrefix,
          cache: false,
          isTree: true,
          value: 'id', // 数据字典中value字段的属性名
          label: 'name', // 数据字典中label字段的属性名
          children: 'children', // 数据字典中children字段的属性名
          getData: (url, dict, { form, component }) => { // 配置此参数会覆盖全局的getRemoteDictFunc
            return request({ url: url, params: { limit: 999, status: 1, is_catalog: 1 } }).then(ret => {
              const responseData = ret.data.data
              const result = XEUtils.toArrayTree(responseData, { parentKey: 'parent', strict: true })
              return [{ id: null, name: 'root node', children: result }]
            })
          }
        },
        form: {
          component: {
            props: {
              elProps: {
                clearable: true,
                showAllLevels: false, // 仅显示最后一级
                props: {
                  checkStrictly: true, // 可以不需要选到最后一级
                  emitPath: false,
                  clearable: true
                }
              }
            }
          }
        }
      },
      {
        title: 'menu name',
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
        minWidth: 180,
        type: 'input',
        form: {
          rules: [ // 表单校验规则
            { required: true, message: 'Menu name is required' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: 'Please enter a menu name'
          },
          itemProps: {
            class: { yxtInput: true }
          }

        }
      },
      {
        title: 'icon',
        key: 'icon',
        width: 60,
        type: 'icon-selector',
        form: {
          component: {
            placeholder: 'Please enter an icon'
          }
        }
      },
      {
        title: 'to sort',
        key: 'sort',
        width: 60,
        type: 'number',
        form: {
          value: 1,
          component: {
            placeholder: 'Please enter sort'
          }
        }
      },
      {
        title: 'Is it a directory',
        key: 'is_catalog',
        width: 100,
        type: 'dict-switch',
        search: {
          disabled: true
        },
        dict: {
          data: vm.dictionary('button_whether_bool')
        },
        form: {
          value: false,
          component: {
            placeholder: 'Please choose whether to catalog'
          },
          valueChange (key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            if (!value) {
              form.web_path = undefined
              form.component = undefined
              form.component_name = undefined
              form.cache = false
              form.is_link = false
            }
          }
        }
      },
      {
        title: 'external link',
        key: 'is_link',
        width: 70,
        type: 'radio',
        dict: {
          data: vm.dictionary('button_whether_bool')
        },
        form: {
          value: false,
          component: {
            show (context) {
              const { form } = context
              return !form.is_catalog
            },
            placeholder: 'Please choose whether to link'
          },
          valueChange (key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            form.web_path = undefined
            form.component = undefined
            form.component_name = undefined
            if (value) {
              getColumn('web_path').title = 'external link address'
              getColumn('web_path').component.placeholder = 'Please enter the external link address'
              getColumn('web_path').helper = {
                render (h) {
                  return (< el-alert title="External link address, please start with https|http|ftp|rtsp|mms" type="warning" />
                  )
                }
              }
            } else {
              getColumn('web_path').title = 'routing address'
              getColumn('web_path').component.placeholder = 'Please enter the routing address'
              getColumn('web_path').helper = {
                render (h) {
                  return (< el-alert title="The address of the url in the browser, please start with /" type="warning" />
                  )
                }
              }
            }
          }
        }
      },
      {
        title: 'routing address',
        key: 'web_path',
        width: 150,
        show: false,
        form: {
          rules: [
            { required: true, message: 'Please enter the correct routing address' },
            { validator: validateWebPath, trigger: 'change' }
          ],
          component: {
            show (context) {
              const { form } = context
              return !form.is_catalog
            },
            props: {
              clearable: true
            },
            placeholder: 'Please enter the routing address'
          },
          helper: {
            render (h) {
              return (< el-alert title="The address of the url in the browser, please start with /" type="warning" />
              )
            }
          }
        }
      },
      {
        title: 'component address',
        key: 'component',
        type: 'select',
        show: false,
        dict: {
          cache: false,
          data: vm.searchFiles()
        },
        form: {
          rules: [
            { required: true, message: 'Please select component address' }
          ],
          component: {
            show (context) {
              const { form } = context
              return !form.is_catalog && !form.is_link
            },
            props: {
              clearable: true,
              filterable: true // 可过滤选择项
            },
            placeholder: 'Please enter the component address'
          },
          helper: {
            render (h) {
              return (< el-alert title="Folder address under src/views" type="warning" />
              )
            }
          }
        }
      },
      {
        title: 'component name',
        key: 'component_name',
        width: 170,
        form: {
          rules: [
            { required: true, message: 'Please enter a component name' }
          ],
          component: {
            show (context) {
              const { form } = context
              return !form.is_catalog && !form.is_link
            },
            props: {
              clearable: true
            },
            placeholder: 'Please enter a component name'
          },
          helper: {
            render (h) {
              return (< el-alert title="The name in the xx.vue file" type="warning" />
              )
            }
          }
        }
      },
      {
        title: 'Have authority',
        key: 'menuPermission',
        type: 'select',
        width: 300,
        form: {
          disabled: true,
          component: {
            elProps: { // el-select的配置项，https://element.eleme.cn/#/zh-CN/component/select
              filterable: true,
              multiple: true,
              clearable: true
            }
          }
        }
      },
      {
        title: 'Cache',
        key: 'cache',
        search: {
          disabled: false
        },
        width: 60,
        type: 'radio',
        dict: {
          data: vm.dictionary('button_whether_bool')
        },
        form: {
          value: false,
          component: {
            show (context) {
              const { form } = context
              return !form.is_catalog
            },
            placeholder: 'Please choose whether to cache'
          },
          helper: {
            render (h) {
              return (< el-alert title="Whether to enable page caching, the component name needs to be consistent with the name of the xx.vue page" type="warning" />
              )
            }
          }
        }
      },
      {
        title: 'Side visible',
        key: 'visible',
        search: {
          disabled: false
        },
        width: 75,
        type: 'radio',
        dict: {
          data: vm.dictionary('button_whether_bool')
        },
        form: {
          value: true,
          component: {
            placeholder: 'Please select side visible'
          },
          rules: [ // 表单校验规则
            { required: true, message: 'Required fields visible on side' }
          ],
          helper: {
            render (h) {
              return (< el-alert title="Whether to show in the side menu" type="warning" />
              )
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
        width: 70,
        type: 'radio',
        dict: {
          data: vm.dictionary('button_status_bool')
        },
        form: {
          value: true,
          component: {
            placeholder: 'Please select a status'
          },
          rules: [ // 表单校验规则
            { required: true, message: 'Status Required' }
          ]
        }
      }
    ].concat(vm.commonEndColumns({
      update_datetime: { showTable: false }
    }))
  }
}
