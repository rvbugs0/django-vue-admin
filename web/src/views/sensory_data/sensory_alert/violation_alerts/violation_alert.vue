<script>
import * as api from './api'

export default {
  name: "violation_alerts",
  
  data() {
    return {};
  },
  methods: {
    sendEmailAlerts(){
      return api.sendAlerts();
    }
    
  }
}
</script>


<template>
  <div>

    <button @click="sendEmailAlerts">Send Email Alerts</button>


  </div>
</template>


<style lang="scss">
.yxtInput {
  .el-form-item__label {
    color: #49a1ff;
  }
}
</style>