<!--
  * @Create file time: 2021-06-01 22:41:20
  * @Auther: Ape Xiaotian
  * @last modified by: Yuan Xiaotian
  * @last modification time: 2021-06-09 11:37:44
  * Contact Qq:1638245306
  * @file introduction: front-end log
-->
<template>
  <el-tooltip effect="dark" :content="tooltipContent" placement="bottom">
    <el-button
      class="d2-ml-0 d2-mr btn-text can-hover"
      type="text"
      @click="handleClick"
    >
      <el-badge
        v-if="logLength > 0"
        :max="99"
        :value="logLengthError"
        :is-dot="logLengthError === 0"
      >
        <d2-icon
          :name="logLengthError === 0 ? 'dot-circle-o' : 'bug'"
          style="font-size: 20px"
        />
      </el-badge>
      <d2-icon v-else name="dot-circle-o" style="font-size: 20px" />
    </el-button>
  </el-tooltip>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
export default {
  computed: {
    ...mapGetters('d2admin', {
      logLength: 'log/length',
      logLengthError: 'log/lengthError'
    }),
    tooltipContent () {
      return this. logLength === 0
        ? 'No logs or exceptions'
        : `${this.logLength} logs ${
            this.logLengthError > 0
              ? ` | Contains ${this.logLengthError} exceptions`
              : ''
          }`
    }
  },
  methods: {
    ...mapMutations('d2admin/log', ['clean']),
    handleClick() {
      this. $router. push({
        name: 'frontendLog'
      })
    }
  }
}
</script>