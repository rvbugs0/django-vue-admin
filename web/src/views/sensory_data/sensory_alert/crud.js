export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true,
    },
    options: {
      tableType: "vxe-table",
      rowKey: true, // 必须设置，true or false
      rowId: "id",
      height: "100%", // 表格高度100%, 使用toolbar必须设置
      highlightCurrentRow: false,
    },
    rowHandle: {
      view: {
        thin: true,
        text: "",
        disabled() {
          return !vm.hasPermissions("Retrieve");
        },
      },
      width: 230,
      edit: {
        thin: true,
        text: "",
        disabled() {
          return !vm.hasPermissions("Update");
        },
      },
      remove: {
        thin: true,
        text: "",
        disabled() {
          return !vm.hasPermissions("Delete");
        },
      },
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
        title: "Sensory attribute",
        key: "entity",
        search: {},
        type: "select",

        form: {
          rules: [{ required: true, message: "Please select" }],
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
            {
              value: "sea_water_temperature_c",
              label: "Sea Water Temperature",
            },
            { value: "salinity", label: "Salinity" },
            { value: "ph", label: "pH" },
            { value: "dissolved_oxygen", label: "Dissolved Oxygen" },
          ],
        },
      },
      
      {
        title: "Lower treshold",
        key: "lower_treshold",
        sortable: true,
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true,
            },
          },
        },
        type: "number", // change type from 'date' to 'number'
        form: {
          rules: [
            // form validation rules
            { required: true, message: "Required" },
            { type: "number", message: "Input must be a number" }, // add validation for numeric input
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "Please enter end date",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },

      {
        title: "Upper treshold",
        key: "upper_treshold",
        sortable: true,
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true,
            },
          },
        },
        type: "number", // change type from 'date' to 'number'
        form: {
          rules: [
            // form validation rules
            { required: true, message: "Required" },
            { type: "number", message: "Input must be a number" }, // add validation for numeric input
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "Please enter end date",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },

    ],
  };
};
