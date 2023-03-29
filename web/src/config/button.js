export const BUTTON_VALUE_TO_COLOR_MAPPING = {
  1: 'success',
  true: 'success',
  0: 'danger',
  false: 'danger',
  Search: 'warning', // query
  Update: 'primary', // edit
  Create: 'success', // add
  Retrieve: 'info', // singleton
  Delete: 'danger' // delete
}

export function getButtonSettings (objectSettings) {
  return objectSettings. map(item => {
    return {
      label: item.label,
      value: item. value,
      color: BUTTON_VALUE_TO_COLOR_MAPPING[item.value]
    }
  })
}
// deprecated in v2.0.2, changed to vm.dictionary('button_status_bool')
// enable true/disable false
export const BUTTON_STATUS_BOOL = getButtonSettings([{ label: 'enabled', value: true }, { label: 'disabled', value: false }])

// enable 1/disable 0
export const BUTTON_STATUS_NUMBER = getButtonSettings([{ label: 'Enabled', value: 1 }, { label: 'Disabled', value: 0 }])

// yes 1/ no 0
export const BUTTON_WHETHER_NUMBER = getButtonSettings([{ label: 'Yes', value: 1 }, { label: 'No', value: 0 }])
// is true/no false
export const BUTTON_WHETHER_BOOL = getButtonSettings([{ label: 'Yes', value: true }, { label: 'No', value: false }])
// user type
export const USER_TYPE = getButtonSettings([{ label: 'background user', value: 0 }, { label: 'foreground user', value: 1 }])