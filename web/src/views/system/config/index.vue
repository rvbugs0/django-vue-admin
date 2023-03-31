<template>
  <d2-container>
    <div>
      <el-header>
        <div class="yxt-flex-between">
          <div>
            <el-tag>System Configuration: You can customize your website</el-tag>
          </div>
          <div>
            <el-button-group>
              <el-button
                type="primary"
                size="small"
                icon="el-icon-folder-add"
                @click="tabsDrawer=true"
              >
              add group
              </el-button>
              <el-button
                size="small"
                type="warning"
                icon="el-icon-edit-outline"
                @click="contentDrawer=true"
              >
              add content
              </el-button>
            </el-button-group>
          </div>
        </div>
      </el-header>
    </div>
    <div>
      <el-drawer
        v-if="tabsDrawer"
        title="add group"
        :visible.sync="tabsDrawer"
        direction="rtl"
        size="30%"
      >
        <addTabs></addTabs>
      </el-drawer>
    </div>
    <div>
      <el-drawer
        v-if="contentDrawer"
        title="add content"
        :visible.sync="contentDrawer"
        direction="rtl"
        size="30%"
      >
        <addContent></addContent>
      </el-drawer>
    </div>
    <el-tabs type="border-card" v-model="editableTabsValue">
      <el-tab-pane
        :key="index"
        v-for="(item, index) in editableTabs"
        :label="item.title"
        :name="item.key"
      >
        <span slot="label" v-if="item.icon"><i :class="item.icon" style="font-weight: 1000;font-size: 16px;"></i></span>
        <el-row v-if="item.icon">
          <el-col :offset="4" :span="8">
            <addContent></addContent>
          </el-col>
        </el-row>
        <formContent v-else :options="item" :editableTabsItem="item"></formContent>
      </el-tab-pane>
    </el-tabs>
  </d2-container>
</template>

<script>
import addTabs from '@/views/system/config/components/addTabs'
import * as api from './api'
import addContent from '@/views/system/config/components/addContent'
import formContent from '@/views/system/config/components/formContent'

export default {
  name: 'config',
  components: {
    addTabs,
    addContent,
    formContent
  },
  data () {
    return {
      tabsDrawer: false,
      contentDrawer: false,
      editableTabsValue: 'base',
      editableTabs: [],
      tabIndex: 2
    }
  },
  methods: {
    getTabs () {
      api.GetList({
        limit: 999,
        parent__isnull: true
      }).then(res => {
        const { data } = res.data
        data.push({
          title: 'none',
          icon: 'el-icon-plus',
          key: 'null'
        })
        this.editableTabs = data
      })
    }
  },
  created () {
    this.getTabs()
  }
}
</script>

<style scoped>

</style>
