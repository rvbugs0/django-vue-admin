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
      fixed: 'right',
      view: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      width: 70,
      edit: {
        thin: true,
        text: '',
        show: false,
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: 'Delete',
        show: false,
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      }
    },
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      disabled: true,
      defaultSpan: 12 // 默认的表单 span
    },
    indexRow: { // 或者直接传true,不显示title，不居中
      title: 'S.No.',
      align: 'center',
      width: 70
    },
    columns: [
      {
        title: 'Keyword',
        key: 'search',
        show: false,
        disabled: true,
        search: {
          disabled: false
        },
        form: {
          show: false,
          component: {
            placeholder: 'Please enter a keyword'
          }
        }
      },
      {
        title: 'ID',
        key: 'id',
        width: 90,
        disabled: true,
        form: {
          disabled: true
        }
      },
      {
        title: 'Login username',
        key: 'username',
        search: {
          disabled: false
        },
        width: 140,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: 'Please enter username'
          }
        }
      },
      {
        title: 'Login IP',
        key: 'ip',
        search: {
          disabled: false
        },
        width: 130,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: 'Please enter the login IP'
          }
        }
      }, {
        title: 'ISP',
        key: 'isp',
        search: {
          disabled: true
        },
        disabled: true,
        width: 180,
        type: 'input',
        form: {
          component: {
            placeholder: 'Please enter the ISP'
          }
        }
      }, {
        title: 'Continent',
        key: 'continent',
        width: 80,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: 'Please enter the continent'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }, {
        title: 'Country',
        key: 'country',
        width: 80,
        type: 'input',
        form: {
          component: {
            placeholder: 'Please enter country'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }, {
        title: 'Province',
        key: 'province',
        width: 80,
        type: 'input',
        form: {
          component: {
            placeholder: 'Please enter province'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }, {
        title: 'City',
        key: 'city',
        width: 80,
        type: 'input',
        form: {
          component: {
            placeholder: 'Please enter a city'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }, {
        title: 'District',
        key: 'district',
        width: 80,
        type: 'input',
        form: {
          component: {
            placeholder: 'Please enter a district'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }, {
        title: 'area code',
        key: 'area_code',
        width: 100,
        type: 'input',
        form: {
          component: {
            placeholder: 'Please enter area code'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }, {
        title: 'English full name',
        key: 'country_english',
        width: 120,
        type: 'input',
        form: {
          component: {
            placeholder: 'Please enter the English full name'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }, {
        title: 'Abbreviation',
        key: 'country_code',
        width: 100,
        type: 'input',
        form: {
          component: {
            placeholder: 'Please enter a short name'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }, {
        title: 'longitude',
        key: 'longitude',
        width: 80,
        type: 'input',
        disabled: true,
        form: {
          component: {
            placeholder: 'please enter longitude'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }, {
        title: 'latitude',
        key: 'latitude',
        width: 80,
        type: 'input',
        disabled: true,
        form: {
          component: {
            placeholder: 'please enter latitude'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }, {
        title: 'login type',
        key: 'login_type',
        width: 100,
        type: 'select',
        search: {
          disabled: false
        },
        dict: {
          data: [{ label: 'Normal login', value: 1 }, { label: 'WeChat scan code login', value: 2 }]
        },
        form: {
          component: {
            placeholder: 'Please select a login type'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }, {
        title: 'operating system',
        key: 'os',
        width: 180,
        type: 'input',
        form: {
          component: {
            placeholder: 'Please enter the operating system'
          }
        }
      }, {
        title: 'browser name',
        key: 'browser',
        width: 180,
        type: 'input',
        form: {
          component: {
            placeholder: 'Please enter a browser name'
          }
        }
      }, {
        title: 'agent information',
        key: 'agent',
        disabled: true,
        width: 180,
        type: 'input',
        form: {
          component: {
            placeholder: 'Please enter agent information'
          }
        }
      }, {
        fixed: 'right',
        title: 'Log in time',
        key: 'create_datetime',
        width: 160,
        type: 'datetime'
      }
    ]
  }
}
