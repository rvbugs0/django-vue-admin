<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x ref="d2Crud" v-bind="_crudProps" v-on="_crudListeners">
      <div slot="header">
        <crud-search ref="search" :options="crud.searchOptions" @submit="handleSearch" />
        <el-button-group>
          <el-button size="small" v-permission="'Create'" type="primary" @click="addRow"><i class="el-icon-plus" />
            Add</el-button>
          <el-button size="small" type="warning" @click="onExport" v-permission="'Export'"><i class="el-icon-download" />
            export
          </el-button>
        </el-button-group>
        <crud-toolbar :search.sync="crud.searchOptions.show" :compact.sync="crud.pageOptions.compact"
          :columns="crud.columns" @refresh="doRefresh()" 
          @columns-filter-changed="handleColumnsFilterChanged"
          />
      </div>
    </d2-crud-x>
    <!--  角色授权  -->
    <div>
    </div>
  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
export default {
  name: 'sensory_table',
  mixins: [d2CrudPlus.crud],
  data() {
    return {

    }
  },
  methods: {
    getCrudOptions() {
      return crudOptions(this)
    },

    pageRequest(query) {

      if (query.date_recorded) {
        
        // console.log(formattedDate)
        var q = {...query}
        q.start_date = query.date_recorded
        
        if(q.end_date){
          q.end_date = query.end_date

        }else{
          q.end_date = query.date_recorded
        }

        
        
        return api.GetList(q,true)
      }else{
        return api.GetList(query)

      }

      return api.GetList(query,query.start_date)
    },
    addRequest(row) {
      return api.createObj(row)
    },
    updateRequest(row) {
      return api.UpdateObj(row)
    },
    delRequest(row) {
      return api.DelObj(row.id)
    }, onExport() {
      const that = this
      this.$confirm('Are you sure to export all data items?', 'warning', {
        confirmButtonText: 'Sure',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(function () {
        const query = that.getSearch().getForm()
        console.log(query)
        return api.exportData({ ...query })
      })
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


