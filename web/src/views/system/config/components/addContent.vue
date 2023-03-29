<template>
  <div style="padding: 20px">
    <el-form ref="form" :model="form" :rules="rules" label-width="80px">
      <el-form-item label="belongs to the group" prop="parent">
        <el-select v-model="form.parent" placeholder="Please select group" clearable>
          <el-option :label="item.title" :value="item.id" :key="index"
                     v-for="(item,index) in parentOptions"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="title" prop="title">
        <el-input v-model="form.title" placeholder="Please enter" clearable></el-input>
      </el-form-item>
      <el-form-item label="key value" prop="key">
        <el-input v-model="form.key" placeholder="Please enter" clearable></el-input>
      </el-form-item>
      <el-form-item label="form type" prop="form_item_type">
        <el-select v-model="form.form_item_type" placeholder="Please select" clearable>
          <el-option :label="item.label" :value="item.value" :key="index"
                     v-for="(item,index) in dictionary('config_form_type')"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item
        v-if="[4,5,6].indexOf(form.form_item_type)>-1"
        label="dictionary key"
        prop="setting"
        :rules="[{required: true,message: 'cannot be empty'}]">
        <el-input v-model="form.setting" placeholder="Please enter the key value in the dictionary" clearable></el-input>
      </el-form-item>
      <div v-if="[13,14].indexOf(form.form_item_type)>-1">
        <associationTable ref="associationTable" v-model="form.setting"
                          @updateVal="associationTableUpdate"></associationTable>
      </div>
      <el-form-item label="validation rules">
        <el-select v-model="form.rule" multiple placeholder="Please select (multiple choices)" clearable>
          <el-option :label="item.label" :value="item.value" :key="index"
                     v-for="(item,index) in ruleOptions"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="prompt information" prop="placeholder">
        <el-input v-model="form.placeholder" placeholder="Please enter" clearable></el-input>
      </el-form-item>
      <el-form-item label="sort" prop="sort">
        <el-input-number v-model="form.sort" :min="0" :max="99"></el-input-number>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">Create Now</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import * as api from '../api'
import associationTable from './components/associationTable'

export default {
  name: 'addContent',
  inject: ['refreshView'],
  components: {
    associationTable
  },
  data () {
    return {
      form: {
        parent: null,
        title: null,
        key: null,
        form_item_type: null,
        rule: null,
        placeholder: null
      },
      rules: {
        parent: [
          {
            required: true,
            message: 'Please select'
          }
        ],
        title: [
          {
            required: true,
            message: 'Please enter'
          }
        ],
        key: [
          {
            required: true,
            message: 'Please enter'
          },
          {
            pattern: /^[A-Za-z0-9_]+$/,
            message: 'Please enter numbers, letters or underscores'
          }
        ],
        form_item_type: [
          {
            required: true,
            message: 'Please enter'
          }
        ]
      },
      // parent content
      parentOptions: [],
      ruleOptions: [
        {
          label: 'required',
          value: '{"required": true, "message": "Required items cannot be empty"}'
        },
        {
          label: 'Email',
          value: '{ "type": "email", "message": "Please enter a correct email address"}'
        },
        {
          label: 'URL address',
          value: '{ "type": "url", "message": "Please enter the correct URL address"}'
        }
      ]
    }
  },
  methods: {
    getParent () {
      api. GetList({
        parent__isnull: true,
        limit: 999
      }).then(res => {
        const { data } = res. data
        this. parentOptions = data
      })
    },
    // submit
    onSubmit () {
       const that = this
       that.associationTableUpdate().then(() => {
         const form = JSON. parse(JSON. stringify(that. form))
         const rules = []
         for (const item of form.rule) {
           const strToObj = JSON. parse(item)
           rules. push(strToObj)
         }
         form.rule = rules
         that.$refs.form.validate((valid) => {
           if (valid) {
             api.createObj(form).then(res => {
               this.$message.success('Add success')
               this. refreshView()
             })
           } else {
             console. log('error submit!!')
             return false
           }
         })
       })
     },
     // Association table data update
     associationTableUpdate () {
       const that = this
       return new Promise(function (resolve, reject) {
         if (that. $refs. associationTable) {
           if (!that. $refs. associationTable. onSubmit()) {
             // eslint-disable-next-line prefer-promise-reject-errors
             return reject(false)
           }
           const { formObj } = that. $refs. associationTable
           that.form.setting = formObj
           return resolve(true)
         } else {
           return resolve(true)
         }
       })
     }
   },
   created () {
     this. getParent()
   }
}
</script>

<style scoped>

</style>