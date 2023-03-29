export const crudOptions = (vm) => {
  return {

    pageOptions: {
      compact: true
    },
    options: {
      tableType: 'vxe-table',
      rowKey: true, // must be set, true or false
      rowId: 'id',
      height: '100%', // table height 100%, must be set when using toolbar
      highlightCurrentRow: false,
      treeConfig: { // tree data configuration
        children: 'children',
        hasChild: 'hasChildren',
        expandAll: true
      }
    },
    rowHandle: {
      width: 230,
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
      custom: [{
        text: 'dictionary configuration',
        type: 'success',
        size: 'small',
        emit: 'dictionaryConfigure'
      }]
    },
    indexRow: { // Or pass true directly, do not display title, do not center
      title: 'serial number',
      align: 'center',
      width: 80
    },
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 24, // default form span
      width: '35%'
    },
    columns: [{
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
      view: { // View the individual configuration of the dialog component
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
      title: 'dictionary name',
      key: 'label',

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
        rules: [ // form validation rules
          { required: true, message: 'Dictionary name is required' }
        ],
        component: {
          props: {
            clearable: true
          },
          placeholder: 'Please enter the dictionary name'
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    },
    {
      title: 'dictionary number',
      key: 'value',
      search: {
        disabled: true,
        component: {
          props: {
            clearable: true
          }
        }
      },
      type: 'input',
      form: {
        rules: [ // form validation rules
          { required: true, message: 'dictionary number is required' }
        ],
        component: {
          props: {
            clearable: true
          },
          placeholder: 'Please enter the dictionary number'
        },
        itemProps: {
          class: { yxtInput: true }
        },
        helper: {
          render(h) {
            return (< el-alert title="How to use: vm.dictionary('dictionary number')" type="warning"/>
            )
          }
        }
      }
    },

    {
      title: 'Status',
      key: 'status',
      width: 90,
      search: {
        disabled: false
      },
      type: 'radio',
      dict: {
        data: vm.dictionary('button_status_bool')
      },
      component: {
        props: {
          options: []
        }
      },
      form: {
        rules: [ // form validation rules
          { required: true, message: 'status required' }
        ],
        value: true,
        component: {
          placeholder: 'Please select a status'
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    },
    {
      title: 'sort',
      key: 'sort',
      width: 90,
      type: 'number',
      form: {
        value: 1,
        component: {
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    }
    ].concat(vm.commonEndColumns({
      description: {
        showForm: true,
        showTable: true
      }
    }))
  }
}