<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'



export default {
  name: "sensory_alert_table",
  mixins: [d2CrudPlus.crud],
  data() {
    return {};
  },
  methods: {
    getCrudOptions() {
      return crudOptions(this);
    },
    pageRequest(query) {
      return api.GetList(query);
    },
    addRequest(row) {
      return api.createObj(row);
    },
    updateRequest(row) {
      return api.UpdateObj(row);
    },
    delRequest(row) {
      return api.DelObj(row.id);
    }
  }
}
</script>


<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x ref="d2Crud" v-bind="_crudProps" v-on="_crudListeners">
      <div slot="header">
        <crud-search ref="search" :options="crud.searchOptions" @submit="handleSearch" />
        <el-button-group>
          <el-button size="small" v-permission="'Create'" type="primary" @click="addRow"><i class="el-icon-plus" />
            Add</el-button>
        </el-button-group>
        <crud-toolbar :search.sync="crud.searchOptions.show" :compact.sync="crud.pageOptions.compact"
          :columns="crud.columns" @refresh="doRefresh()" @columns-filter-changed="handleColumnsFilterChanged" />
      </div>
    </d2-crud-x>
    <!--  角色授权  -->
    

  </d2-container>
</template>


<style lang="scss">
.yxtInput {
  .el-form-item__label {
    color: #49a1ff;
  }
}
</style>