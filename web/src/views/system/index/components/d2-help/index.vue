<template>
  <div>
    <el-button type="primary" @click="dialogVisible = true" plain round>
      <d2-icon name="question-circle-o" class="d2-mr-5"/>
      need any help
    </el-button>
    <el-dialog
      title="help"
      width="600px"
      :visible.sync="dialogVisible"
      :append-to-body="true">
      <div style="margin-top: -25px;">
        <h2 class="d2-mt-0">
          Here are some references
        </h2>
        <el-button-group>
          <el-button @click="$open('https://d2.pub/zh/doc/d2-admin')">
            <d2-icon name="book" class="d2-mr-5"/>
            document
          </el-button>
          <el-button @click="$open('https://github.com/d2-projects/d2-admin/issues?q=is%3Aissue+is%3Aclosed')">
            <d2-icon name="question" class="d2-mr-5"/>
            historical questions
          </el-button>
          <el-button @click="$open('https://github.com/d2-projects/d2-admin/issues/new/choose')">
            <d2-icon name="plus" class="d2-mr-5"/>
            Submit a question
          </el-button>
        </el-button-group>
        <h2>Ask other users or authors</h2>
        <el-row :gutter="20">
          <el-col :span="12">
            <img src="./image/qq.svg" style="width: 100%;">
            <div class="d2-help--qr-info">
              Please use mobile phone QQ to scan the QR code above<br/>
              1 group 806395827 (full) | 2 groups 592981556
            </div>
          </el-col>
          <el-col :span="12">
            <img src="./image/we.svg" style="width: 100%;">
            <div class="d2-help--qr-info">
              Please use WeChat to scan the QR code above<br/>
              Add the author's WeChat friend and invite to join the WeChat group
            </div>
          </el-col>
        </el-row>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data () {
    return {
      dialogVisible: false
    }
  }
}
</script>

<style lang="scss" scoped>
.d2-help--qr-info {
  background-color: #f4f4f5;
  color: #909399;
  width: 100%;
  padding: 8px 16px;
  margin: 0;
  box-sizing: border-box;
  border-radius: 4px;
  position: relative;
  overflow: hidden;
  opacity: 1;
  display: flex;
  align-items: center;
  transition: opacity .2s;
}
</style>
