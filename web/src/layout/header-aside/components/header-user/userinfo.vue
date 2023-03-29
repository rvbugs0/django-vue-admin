<template>
  <d2-container class="page">
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="User Settings" name="userInfo">
        <el-row :gutter="20">
          <el-col :span="10" :offset="6">
            <el-form
              ref="userInfoForm"
              label-width="100px"
              :model="userInfo"
              required-asterisk
              :rules="userInforules"
              :label-position="position"
              center
            >
              <el-form-item prop="avatar" label="Avatar">
                <d2p-cropper-uploader :value="userInfo.avatar || '/image/avatar.png'" @input="handleAvatarSuccess"/>
              </el-form-item>
              <el-form-item prop="name" required label="nickname">
                <el-input v-model="userInfo.name" clearable></el-input>
              </el-form-item>
              <el-form-item label="phone number" required prop="mobile">
                <el-input v-model="userInfo.mobile" clearable></el-input>
              </el-form-item>
              <el-form-item label="email" prop="email">
                <el-input v-model="userInfo.email" clearable></el-input>
              </el-form-item>
              <el-form-item label="gender" prop="gender">
                <el-radio-group v-model="userInfo.gender">
                  <el-radio :label="1">Male</el-radio>
                  <el-radio :label="0">Female</el-radio>
                  <el-radio :label="-1">Unknown</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="username" prop="dept">
                <el-input :value="userInfo.username" clearable disabled></el-input>
              </el-form-item>
              <el-form-item label="Department" prop="dept">
                <el-input :value="userInfo.dept_info && userInfo.dept_info.dept_name" clearable disabled></el-input>
              </el-form-item>
              <el-form-item label="current role" prop="role">
                <el-select :value="userInfo.role" multiple placeholder="Please select" disabled style="width: 100%;">
                  <el-option
                    v-for="item in userInfo.role_info"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item>
                <el-button @click="updateInfo" type="primary">
                  <i class="fa fa-check"></i>
                  renew
                </el-button>
                <el-button @click="resetForm('info')" type="info">
                  <i class="fa fa-reply-all"></i>
                  reset
                </el-button>
              </el-form-item>
            </el-form>
          </el-col>
        </el-row>
      </el-tab-pane>
      <el-tab-pane label="Password Settings" name="passwrod">
        <el-row :gutter="20">
          <el-col :span="10" :offset="6">
            <el-form
              ref="userPasswordForm"
              :model="userPasswordInfo"
              required-asterisk
              label-width="100px"
              :label-position="position"
              :rules="passwordRules"
              center
            >
              <el-form-item label="Original Password" required prop="oldPassword">
                <el-input
                  v-model="userPasswordInfo.oldPassword"
                  placeholder="Please enter the original password"
                  clearable
                ></el-input>
              </el-form-item>
              <el-form-item required prop="newPassword" label="new password">
                <el-input
                  type="password"
                  v-model="userPasswordInfo.newPassword"
                  placeholder="Please enter a new password"
                  clearable
                ></el-input>
              </el-form-item>
              <el-form-item required prop="newPassword2" label="Confirm password">
                <el-input
                  type="password"
                  v-model="userPasswordInfo.newPassword2"
                  placeholder="Please enter the new password again"
                  clearable
                ></el-input>
              </el-form-item>


              <el-form-item>
                 <el-button type="primary" @click="settingPassword">
                   <i class="fa fa-check"></i>Submit
                 </el-button>
                 <el-button @click="resetForm('passwordForm')" type="info">
                   <i class="fa fa-reply-all"></i> Reset
                 </el-button>
               </el-form-item>
             </el-form>
           </el-col>
         </el-row>
       </el-tab-pane>
     </el-tabs>
   </d2-container>
</template>
<script>
import util from '@/libs/util.js'
import { request } from '@/api/service'
import { mapActions } from 'vuex'
export default {
   name: 'userInfo',
   data () {
     var validatePass = (rule, value, callback) => {
       const pwdRegex = new RegExp('(?=.*[0-9])(?=.*[a-zA-Z]).{8,30}')
       if (value === '') {
         callback(new Error('Please enter a password'))
       } else if (value === this. userPasswordInfo. oldPassword) {
         callback(new Error('The original password is the same as the new password'))
       } else if (!pwdRegex. test(value)) {
         callback(new Error('The complexity of your password is too low (the password must contain letters and numbers)'))
       } else {
         if (this. userPasswordInfo. newPassword2 !== '') {
           this.$refs.userPasswordForm.validateField('newPassword2')
         }
         callback()
       }
     }
     var validatePass2 = (rule, value, callback) => {
       if (value === '') {
         callback(new Error('Please enter the password again'))
       } else if (value !== this. userPasswordInfo. newPassword) {
         callback(new Error('The passwords entered twice are inconsistent!'))
       } else {
         callback()
       }
     }
     return {
       position: 'left',
       activeName: 'userInfo',
       action: util. baseURL() + 'api/system/file/',
       headers: {
         Authorization: 'JWT' + util. cookies. get('token')
       },
       fileList: [],
       userInfo: {
         name: '',
         gender: '',
         mobile: '',
         avatar: '',
         email: ''
       },
       userInforules: {
         name: [{ required: true, message: 'Please enter a nickname', trigger: 'blur' }],
         mobile: [{ pattern: /^1[3-9]\d{9}$/, message: 'Please enter the correct mobile number' }]
       },
       userPasswordInfo: {
         oldPassword: '',
         newPassword: '',
         newPassword2: ''
       },
       passwordRules: {
         oldPassword: [
           {
             required: true,
             message: 'Please enter the original password',
             trigger: 'blur'
           }
         ],
         newPassword: [{ validator: validatePass, trigger: 'blur' }],
         newPassword2: [{ validator: validatePass2, trigger: 'blur' }]
       }
     }
   },
   mounted () {
     this. getCurrentUserInfo()
   },
   methods: {
     ...mapActions('d2admin/account', ['logout']),
     /**
      * Get current user information
      */
     getCurrentUserInfo() {
       const _self = this
       return request({
         url: '/api/system/user/user_info/',
         method: 'get',
         params: {}
       }).then((res) => {
         _self.userInfo = res.data
       })
     },
     /**
      * Update user information
      */
     updateInfo () {
       const _self = this

       _self.$refs.userInfoForm.validate((valid) => {
         if (valid) {
           const userInfo = _self. userInfo
           delete userInfo.role
           request({
             url: '/api/system/user/update_user_info/',
             method: 'put',
             data: userInfo
           }).then((res) => {
             _self.$message.success('modified successfully')
             _self. getCurrentUserInfo()
           })
         } else {
           // Validation failed
           // login form validation failed
           this.$message.error('Form verification failed, please check')
         }
       })
     },
     // reset
     resetForm(name) {
       const _self = this
       if (name === 'info') {
         _self. getCurrentUserInfo()
       } else {
         _self. userPasswordForm = {}
       }
     },
     // tab switching
     handleClick(tab, event) {
       const _self = this
       if (tab.paneName === 'userInfo') {
         _self.$refs.userPasswordForm.resetFields()
         _self. getCurrentUserInfo()
       } else {
         _self.$refs.userInfoForm.resetFields()
       }
     },
     /**
      * reset password
      */
     settingPassword () {
       const _self = this

       _self.$refs.userPasswordForm.validate((valid) => {
         if (valid) {
           const userId = util. cookies. get('uuid')
           if (userId) {
             const params = JSON. parse(JSON. stringify(_self. userPasswordInfo))
             params.oldPassword = _self.$md5(params.oldPassword)
             params.newPassword = _self.$md5(params.newPassword)
             params.newPassword2 = _self.$md5(params.newPassword2)
             request({
               url: '/api/system/user/' + userId + '/change_password/',
               method: 'put',
               data:params
             }).then((res) => {
               _self.activeName = 'userInfo'
               _self.$message.success('modified successfully')
               _self. logout({})
             })
           }
         } else {
           // Validation failed
           // login form validation failed
           this.$message.error('Form verification failed, please check')
         }
       })
     },
     /**
      * Avatar upload
      * @param res
      * @param file
      */
     handleAvatarSuccess(res, file) {
       this.userInfo.avatar = res
     }
   }
}
</script>