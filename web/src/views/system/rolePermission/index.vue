<!--
  * @Create file time: 2021-06-01 22:41:21
  * @Auther: Ape Xiaotian
  * @last modified by: Yuan Xiaotian
  * @last modification time: 2021-09-26 21:18:29
  * Contact Qq:1638245306
  * @File Introduction: Authorization Management
-->
<template>
  <div>
    <div style="margin: 10px">
      <el-button
        type="primary"
        size="mini"
        @click="submitPermission"
        v-permission="'Save'"
      > save
      </el-button>
    </div>
    <el-container style="height: 80vh; border: 1px solid #eee">
      <el-aside width="300px" style="border:1px solid #eee;padding: 20px;">
        <div style="margin: 10px;">
          <div style="margin-bottom: 20px">
            <div class="yxt-flex-align-center">
              <div class="yxt-divider"></div>
              <span>data authorization</span>
              <el-tooltip
                class="item"
                effect="dark"
                :content="dataAuthorizationTips"
                placement="right"
              >
                <el-icon class="el-icon-question"></el-icon>
              </el-tooltip>
            </div>
          </div>

          <div>
            <el-select
              v-show="roleObj.name"
              v-model="roleObj.data_range"
              @change="dataScopeSelectChange"
            >
              <el-option
                v-for="item in dataScopeOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              ></el-option>
            </el-select>
          </div>

          <div v-show="roleObj. data_range === 4" class="dept-tree">
            <el-tree
              :data="deptOptions"
              show-checkbox
              default-expand-all
              :default-checked-keys="deptCheckedKeys"
              ref="dept"
              node-key="id"
              :check-strictly="true"
              :props="{ label: 'name' }"
            ></el-tree>
          </div>

        </div>
      </el-aside>
      <el-main>
        <div style="margin: 10px;">
          <div>
            <div style="margin-bottom: 20px">
              <div class="yxt-flex-align-center">
                <div class="yxt-divider"></div>
                <span>menu authorization</span>
                <el-tooltip
                  class="item"
                  effect="dark"
                  :content="menuAuthorizationTips"
                  placement="right"
                >
                  <el-icon class="el-icon-question"></el-icon>
                </el-tooltip>
              </div>
            </div>
            <el-tree
              class="flow-tree"
              ref="menuTree"
              :data="menuOptions"
              node-key="id"
              default-expand-all
              show-checkbox
              :expand-on-click-node="false"
              :default-checked-keys="menuCheckedKeys"
              :check-on-click-node="false"
              empty-text="Please select a role first"
              :check-strictly="menuCheckStrictly"
              @check-change="handleCheckClick"
            >
              <span class="custom-tree-node" slot-scope="{ node, data }">
                <div class="yxt-flex-between">
                  <div :style="{width:((4-node.level)*18+100)+'px'}">{{ data.name }}</div>
                  <div>
                    <el-checkbox
                      v-for="(item, index) in data.menuPermission"
                      :key="index"
                      v-model="item. checked"
                    >{{ item.name }}</el-checkbox>
                  </div>
                </div>
              </span>
            </el-tree>
          </div>
        </div>
        <el-backtop target=".el-main"></el-backtop>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import * as api from './api'
import XEUtils from 'xe-utils'

export default {
   name: 'rolePermission',
   props: {
     roleObj: {
       type: Object,
       default () {
         return {
           name: null,
           data_range: null
         }
       }
     }
   },
   data () {
     return {
       filterText: '',
       data: [],
       menuOptions: [],
       permissionData: [],
       menuCheckedKeys: [], // The node selected by default in the menu
       menuCheckStrictly: false,
       deptOptions: [],
       deptCheckedKeys: [],
       dataScopeOptions: [
         {
           value: 0,
           label: 'Only personal data permission'
         },
         {
           value: 1,
           label: 'This department and the following data permissions'
         },
         {
           value: 2,
           label: 'Data permission of this department'
         },
         {
           value: 3,
           label: 'Full Data Access'
         },
         {
           value: 4,
           label: 'Custom Data Permissions'
         }
       ],
       dataAuthorizationTips: 'The range of data that authorized users can operate',
       menuAuthorizationTips: 'Authorized users can operate the range in the menu'
     }
   },
   watch: {
     filterText(val) {
       this.$refs.tree.filter(val)
     }
   },
   methods: {
     filterNode(value, data) {
       if (!value) return true
       return data.label.indexOf(value) !== -1
     },
     getCrudOptions () {
       // eslint-disable-next-line no-undef
       return crudOptions(this)
     },
     pageRequest(query) {
       return api.GetList(query).then(res => {
         res. map((value, index) => {
           value.node_id = index
         })
         this.data = res
         this.$nextTick().then(() => {
           this.initNode()
         })
       })
     },
     initNode () {
       this. getDeptData()
       this. getMenuData(this. roleObj)
       this.menuCheckedKeys = this.roleObj.menu // load checked menu
       this.menuCheckStrictly = true // parent and child are not related to each other
       this.deptCheckedKeys = this.roleObj.dept
       this. GetDataScope()
     },
     addRequest(row) {
       return api.createObj(row)
     },
     updateRequest(row) {
       return api.UpdateObj(row)
     },
     delRequest(row) {
       return api.DelObj(row.id)
     },
     // get department data
     getDeptData() {
       api.GetDataScopeDept().then(ret => {
         this.deptOptions = XEUtils.toArrayTree(ret.data, { parentKey: 'parent', strict: false })
       })
     },
     // get menu data
     getMenuData(data) {
       api.GetMenuData(data).then(res => {
         res.forEach(x => {
           // Check menuPermisson according to the permission of the current role
           x.menuPermission.forEach(a => {
             if (data. permission. indexOf(a. id) > -1) {
               this. $set(a, 'checked', true)
             } else {
               this. $set(a, 'checked', false)
             }
           })
         })
         // Convert menu list to tree list
         this.menuOptions = XEUtils.toArrayTree(res, {
           parentKey: 'parent',
           strict: true
         })
       })
     },
     // Get permission scope
     GetDataScope () {
       api.GetDataScope().then(res => {
         this.dataScopeOptions = res.data
       })
     },
     // All check menu node data
     getMenuAllCheckedKeys () {
       // currently selected menu node
       const checkedKeys = this.$refs.menuTree.getCheckedKeys()
       // Half-selected menu node
       const halfCheckedKeys = this.$refs.menuTree.getHalfCheckedKeys()
       checkedKeys.unshift.apply(checkedKeys, halfCheckedKeys)
       return checkedKeys
     },
     // For all custom permissions, the checked department node data
     getDeptAllCheckedKeys() {
       // currently selected department node
       const checkedKeys = this. $refs. dept. getCheckedKeys()
       // Semi-selected department nodes
       const halfCheckedKeys = this.$refs.dept.getHalfCheckedKeys()
       checkedKeys.unshift.apply(checkedKeys, halfCheckedKeys)
       return checkedKeys
     },
     // Submit changes
     submitPermission () {
       this.roleObj.menu = this.getMenuAllCheckedKeys() // Get the selected menu
       this.roleObj.dept = this.getDeptAllCheckedKeys() // Get the selected department
       const menuData = XEUtils.toTreeArray(this.menuOptions)
       const permissionData = []
       menuData.forEach(x => {
         const checkedPermission = x.menuPermission.filter(f => {
           return f. checked
         })

         if (checkedPermission. length > 0) {
           for (const item of checkedPermission) {
             permissionData. push(item. id)
           }
         }
       })
       this.roleObj.permission = permissionData
       return this.updateRequest(this.roleObj).then(res => {
         this.$message.success('update completed')
       })
     },
     /** Select role permission range trigger */
     dataScopeSelectChange (value) {
       if (value !== 4) {
         // this.$refs.dept.setCheckedKeys([]);
       }
     },
     /**
      * Click on the menu tree, select all the permissions and part of the data
      * @param data
      */
      handleCheckClick(data, checked) {
       const {
         menuPermission,
         children,
         parents
       } = data
       this.menuCheckStrictly = false
       for (const item of menuPermission) {
         this.$set(item, 'checked', checked)
       }
       if (children && parent) {
         for (const item of children) {
           this.$refs.menuTree.setChecked(item.id, checked)
         }
       }
     }
   },
   created () {
     this. pageRequest()
   }
}
</script>

<style lang="scss">
.yxtInput {
   .el-form-item__label {
     color: #49a1ff;
   }
}

.dept-tree::-webkit-scrollbar {
   display: none; /* Chrome Safari */
}

.dept-tree {
   height: 160px;
   overflow-y: scroll;
   scrollbar-width: none; /* firefox */
   -ms-overflow-style: none; /* IE 10+ */
}

.flow-tree {
   overflow: auto;
   flex: 1;

   margin: 10px;

   .el-tree-node {
     .el-tree-node__children {
       overflow: visible !important
     }
   }
}

</style>