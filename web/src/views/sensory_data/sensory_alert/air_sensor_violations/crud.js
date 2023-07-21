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
    indexRow: { // Or pass true directly, do not display title, do not center
      title: 'S.No.',
      align: 'center',
      width: 100
    },

    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 24, // default form span
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
      title: 'SO2 Value',
      key: 'SO2_value',
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
        rules: [ // form validation rules
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
      title: 'NO2 Value',
      key: 'NO2_value',
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
        rules: [ // form validation rules
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
      title: 'O3 Value',
      key: 'O3_value',
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
        rules: [ // form validation rules
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
      title: 'Date Recorded (Start)',
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

      type: 'datetime',
    },
    {
      title: 'Date Recorded (End)',
      key: 'end_date',
      sortable: false,
      show:false,
      search: {
        disabled: false,
        component: {
          props: {
            clearable: true
          }
        }
      },

      type: 'date',
     
    }
    ]
    .concat(vm.commonEndColumns({
      create_datetime: { showTable: false },
      update_datetime: { showTable: false }
    }))
    
  }
}