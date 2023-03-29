<!--
  * @Create file time: 2021-06-01 22:41:21
  * @Auther: Ape Xiaotian
  * @last modified by: Yuan Xiaotian
  * @last modification time: 2021-07-29 22:51:07
  * Contact Qq:1638245306
  * @File introduction: Menu button management (entered by the custom permission of the menu)
-->
<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <template slot="header">
      <div>
        from menu
        <el-tag> {{ $route.query.name }}</el-tag>
      </div>
    </template>
    <d2-crud-x ref="d2Crud" v-bind="_crudProps" v-on="_crudListeners">
      <div slot="header">
        <crud-search
          ref="search"
          :options="crud.searchOptions"
          @submit="handleSearch"
        />
        <el-button-group>
          <el-button size="small" type="primary" @click="addRow"
          ><i class="el-icon-plus"/> New
          </el-button
          >
        </el-button-group>
        <crud-toolbar
          :search.sync="crud.searchOptions.show"
          :compact.sync="crud.pageOptions.compact"
          :columns="crud.columns"
          @refresh="doRefresh()"
          @columns-filter-changed="handleColumnsFilterChanged"
        />
      </div>
    </d2-crud-x>
  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
export default {
  name: 'menuButton',
  mixins: [d2CrudPlus.crud],
  data () {
    return {}
  },
  methods: {
    getCrudOptions () {
      return crudOptions(this)
    },
    pageRequest(query) {
      const menuId = this. $route. query. id
      return api. GetList({ ...query, menu: menuId })
    },
    addRequest(row) {
      const menuId = this. $route. query. id
      return api.createObj(row, menuId)
    },
    updateRequest(row) {
      return api.UpdateObj(row)
    },
    delRequest(row) {
      return api.DelObj(row.id)
    }
  }
}
</script>

<style lang="scss">
.yxtInput {
  .el-form-item__label {
    color: #49a1ff;
  }
}
</style>