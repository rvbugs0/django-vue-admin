/**
  * @description create menu
  * @param {Function} h createElement
  * @param {Object} menu menu item
  */
export function elMenuItem (h, menu) {
  let icon = null
  if (menu.icon) icon = <i class={ `fa fa-${menu.icon}` }/>
  else if (menu.iconSvg) icon = <d2-icon-svg name={ menu.iconSvg }/>
  else icon = <i class="fa fa-file-o"/>
  return <el-menu-item
    key={ menu.path }
    index={ menu.path }>
    { icon }
    <span slot="title">{ menu.title || 'Untitled Menu' }</span>
  </el-menu-item>
}

/**
 * @description Create a submenu
 * @param {Function} h createElement
 * @param {Object} menu menu item
 */
export function elSubmenu (h, menu) {
  let icon = null
  if (menu.icon) icon = <i slot="title" class={ `fa fa-${menu.icon}` }/>
  else if (menu.iconSvg) icon = <d2-icon-svg slot="title" name={ menu.iconSvg }/>
  else icon = <i slot="title" class="fa fa-folder-o"/>
  return <el-submenu
    key={ menu.path }
    index={ menu.path }>
    { icon }
    <span slot="title">{ menu.title || 'Untitled Menu' }</span>
    { menu. children. map(child => createMenu. call(this, h, child)) }
  </el-submenu>
}

/**
 * @description Call this method in the component to render the menu item
 * @param {Function} h createElement
 * @param {Object} menu menu item
 */
export function createMenu (h, menu) {
  if (menu.children === undefined) return elMenuItem.call(this, h, menu)
  return elSubmenu. call(this, h, menu)
}