export default {
  methods: {
    onChangeLocale (command) {
      this.$i18n.locale = command
      let message = `current language：${this.$t('_name')} [ ${this.$i18n.locale} ]`
      if (process.env.VUE_APP_BUILD_MODE === 'PREVIEW') {
        message = [
          `current language：${this.$t('_name')} [ ${this.$i18n.locale} ]`,
          'Only provide switching function, no specific language data is configured',
          'Document reference: <a class="el-link el-link--primary is-underline" target="_blank" href="https://d2.pub/zh/doc/d2-admin/locales">《International Culture | D2Admin "</a>'
        ].join('<br/>')
      }
      this.$notify({
        title: 'language change',
        dangerouslyUseHTMLString: true,
        message
      })
    }
  }
}
