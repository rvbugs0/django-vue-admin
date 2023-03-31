export const BUTTON_VALUE_TO_COLOR_MAPPING = {
  1: 'success',
  true: 'success',
  0: 'danger',
  false: 'danger',
  Search: 'warning', // 查询
  Update: 'primary', // 编辑
  Create: 'success', // 新增
  Retrieve: 'info', // 单例
  Delete: 'danger' // 删除
}

export function getButtonSettings (objectSettings) {
  return objectSettings.map(item => {
    return {
      label: item.label,
      value: item.value,
      color: BUTTON_VALUE_TO_COLOR_MAPPING[item.value]
    }
  })
}
// v2.0.2 中已弃用，改为 vm.dictionary('button_status_bool')
// 启用 true/ 禁用 false
export const BUTTON_STATUS_BOOL = getButtonSettings([{ label: 'Enabled', value: true }, { label: 'Disabled', value: false }])

// 启用 1/ 禁用 0
export const BUTTON_STATUS_NUMBER = getButtonSettings([{ label: 'Enabled', value: 1 }, { label: 'Disabled', value: 0 }])

// 是 1/ 否 0
export const BUTTON_WHETHER_NUMBER = getButtonSettings([{ label: 'Yes', value: 1 }, { label: 'No', value: 0 }])
// 是 true/ 否 false
export const BUTTON_WHETHER_BOOL = getButtonSettings([{ label: 'Yes', value: true }, { label: 'No', value: false }])
// 用户类型
export const USER_TYPE = getButtonSettings([{ label: 'Background user', value: 0 }, { label: 'Foreground user', value: 1 }])
