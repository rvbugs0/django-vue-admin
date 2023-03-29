<!--
  * @Create file time: 2021-06-01 22:41:20
  * @Auther: Ape Xiaotian
  * @last modified by: Yuan Xiaotian
  * @last modification time: 2021-07-27 00:18:52
  * Contact Qq:1638245306
  * @file description:
-->
<template>
  <el-dropdown size="small" class="d2-mr">
    <el-link
      type="primary"
      :underline="false"
      style="margin-bottom: 2px;margin-left: 10px"
      v-if="isTenants"
      >
      <span>
        Current tenant: {{info.tenant_name}}
      </span>
      <span class="btn-text">{{
      info.name ? `Hi ${info.name}` : "not logged in"
    }}</span>
    </el-link>
    <span class="btn-text" v-else>{{
      info.name ? `Hi ${info.name}` : "not logged in"
    }}</span>
    <el-dropdown-menu slot="dropdown">
      <el-dropdown-item @click.native="userInfo">
        <d2-icon name="cog" class="d2-mr-5" />Personal Information
      </el-dropdown-item>
      <el-dropdown-item @click.native="logOff" divided>
        <d2-icon name="power-off" class="d2-mr-5" />
        log out
      </el-dropdown-item>
    </el-dropdown-menu>
    <el-image v-if="info.avatar" :src="info.avatar" :preview-src-list="[info.avatar]" style="width: 20px;height: 20px;border-radius: 20%;top: 5px;" alt="Avatar"></el-image>
  </el-dropdown>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
  computed: {
    ...mapState('d2admin/user', ['info'])
  },
  data () {
    return {
      isTenants: window.pluginsAll && window.pluginsAll.indexOf('dvadmin-tenants-web') !== -1
    }
  },
  methods: {
    ...mapActions('d2admin/account', ['logout']),
    /**
     * @description logout
     */
    logOff () {
      this. logout({
        confirm: true
      })
    },
    /** personal information */
    userInfo () {
      this. $router. push({ path: 'userInfo' })
    }
  }
}
</script>