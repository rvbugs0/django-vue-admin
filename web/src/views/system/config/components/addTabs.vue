<template>
  <div>
    <el-form ref="form" :model="form" :rules="rules" label-width="80px">
      <el-form-item label="title" prop="title">
        <el-input v-model="form.title"></el-input>
      </el-form-item>
      <el-form-item label="key value" prop="key">
        <el-input v-model="form.key"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">create now</el-button>
        <el-button>Cancel</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import * as api from '../api'

export default {
  name: 'addTabs',
  inject: ['refreshView'],
  data () {
    return {
      form: {
        title: null,
        key: null
      },
      rules: {
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
            pattern: /^[A-Za-z0-9]+$/,
            message: 'English and numbers only'
          }
        ]
      }
    }
  },
  methods: {
    onSubmit () {
      const that = this
      that.$refs.form.validate((valid) => {
        if (valid) {
          api.createObj(that.form).then(res => {
            this.$message.success('added successfully')
            this.refreshView()
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
