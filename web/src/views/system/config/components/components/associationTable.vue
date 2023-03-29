<template>
  <div>
    <el-form :model="formObj" ref="association">
      <el-form-item label="association table" prop="table" :rules="[
      { required: true, message: 'required', trigger: 'blur' }
    ]">
        <el-select v-model="formObj.table" filterable clearable placeholder="Please select" @change="handleChange">
          <el-option
            v-for="item in tableOptions"
            :key="item.table"
            :label="item.tableName"
            :value="item.table">
            <span style="float: left">{{ item. tableName }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px">{{ item.table }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="display field" prop="field" :rules="[
      { required: true, message: 'required', trigger: 'blur' }
    ]">
        <el-select v-model="formObj.field" filterable clearable placeholder="Please select">
          <el-option
            v-for="item in labelOptions"
            :key="item.table"
            :label="item.title"
            :value="item.field">
            <span style="float: left">{{ item. field }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px">{{ item.title }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="storage field" prop="primarykey" :rules="[
      { required: true, message: 'required', trigger: 'blur' }
    ]">
        <el-select v-model="formObj.primarykey" filterable clearable placeholder="Please select">
          <el-option
            v-for="(item,index) in labelOptions"
            :key="index"
            :label="item.title"
            :value="item.field">
            <span style="float: left">{{ item. field }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px">{{ item.title }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="filter condition" prop="oldSearchField" :rules="[
      { required: true, message: 'required', trigger: 'blur' }
    ]">
        <el-select v-model="formObj.oldSearchField" multiple filterable clearable placeholder="Please select"
                   @change="handleSearch">
          <el-option
            v-for="(item,index) in labelOptions"
            :key="index"
            :label="item.title"
            :value="item.field">
            <span style="float: left">{{ item. field }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px">{{ item.title }}</span>
          </el-option>
        </el-select>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import * as api from '../../api'

export default {
  name: 'associationTable',
  props: {
    value: {
      type: Object
    }
  },
  model: {
    prop: 'value',
    event: 'updateVal'
  },
  data () {
    return {
      formObj: {
        table: null,
        primarykey: null,
        field: null,
        searchField: null,
        oldSearchField: null
      },
      searchField: null,
      tableOptions: [],
      labelOptions: []
    }
  },
  methods: {
    // Initialization data
    init () {
      api.GetAssociationTable().then(res => {
        const { data } = res
        this. tableOptions = data
        // set default selected
        this.formObj.table = data[0].table
        this.labelOptions = data[0].tableFields
        this.formObj.primarykey = 'id'
        this.formObj.field = 'id'
      })
    },
    // select event
    handleChange(val) {
      const that = this
      const { tableFields } = that. tableOptions. find(item => {
        return item.table === val
      })
      that.labelOptions = tableFields
    },
    // filter condition selected
    handleSearch(val) {
      const that = this
      const fields = that.labelOptions.filter(item => {
        return val.indexOf(item.field) > -1
      })
      that.formObj.searchField = fields
    },
    // update data
    handleUpdate () {
      this. $emit('updateVal', this. formObj)
    },
    // data verification
    onSubmit () {
      let res = false
      this.$refs.association.validate((valid) => {
        if (valid) {
          res = true
        } else {
          return false
        }
      })
      return res
    }
  },
  created () {
    this.init()
  }
}
</script>

<style scoped>

</style>