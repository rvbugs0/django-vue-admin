<!--
  * @Create file time: 2021-06-01 22:41:21
  * @Auther: Ape Xiaotian
  * @last modified by: Yuan Xiaotian
  * @last modification time: 2021-07-29 19:27:29
  * Contact Qq:1638245306
  * @file introduction: role management
-->
<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @createPermission="createPermission"
    >
      <div slot="header">
        <crud-search
          ref="search"
          :options="crud.searchOptions"
          @submit="handleSearch"
        />
        <el-button-group>
          <el-button
            size="small"
            v-permission="'Create'"
            type="primary"
            @click="addRow"
            ><i class="el-icon-plus" />Add</el-button
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
<!-- Role Authorization -->
    <div>
      <el-drawer
        title="role authorization"
        :visible.sync="rolePermissionShow"
        direction="rtl"
        size="70%"
        >
        <template slot="title">
          <div>
            Current role <el-tag>{{roleObj?roleObj.name:'none'}}</el-tag>
          </div>
        </template>
        <div>
          <rolePermission v-if="rolePermissionShow" :role-obj="roleObj"></rolePermission>
        </div>
      </el-drawer>
    </div>
  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
import rolePermission from '../rolePermission'
import { mapState } from 'vuex'

export default {
  name: 'role',
  mixins: [d2CrudPlus.crud],
  components: {
    rolePermission
  },
  computed: {
    ...mapState('d2admin/user', ['info'])
  },
  data () {
    return {
      rolePermissionShow: false,
      roleObj: undefined
    }
  },
  methods: {
    getCrudOptions () {
      return crudOptions(this)
    },
    pageRequest(query) {
      return api. GetList(query)
    },
    addRequest(row) {
      return api.createObj(row)
    },
    updateRequest(row) {
      return api.UpdateObj(row)
    },
    delRequest(row) {
      return api.DelObj(row.id)
    },
    // authorization
    createPermission(scope) {
      console. log(scope)
      this.roleObj = scope.row
      this.rolePermissionShow = true
      // this. $router. push({
      // name: 'rolePermission',
      // params: { id: scope. row. id }
      // })
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