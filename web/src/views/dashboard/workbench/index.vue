<template>
  <d2-container>
    <div class="page-header">

      <el-avatar src="https://q1.qlogo.cn/g?b=qq&amp;nk=190848757&amp;s=640" class="user-avatar">

      </el-avatar>
      <div class="title">
        <h1>DVAdmin - UTA</h1>
        <span> University of Texas at Arlington</span>
      </div>
    </div>

    <el-row :gutter="20">
      <el-col :span="12">
        <div class="grid-content bg-purple">

          <el-card class="box-card" >
            <div slot="header" class="clearfix">
              <span>Dashboard</span>
            </div>
            <el-row>
              <el-col :span="8" v-for="({name,icon,route,color},index) of navigators" :key="index" style="padding: 0">
                <el-card shadow="hover">
                  <div  style="display: flex;align-items: center;flex-direction: column;cursor: pointer" @click="()=>{gotoRoute(route)}">
                    <d2-icon-svg :name="icon" style="width: 25px;height: 25px;" :style="{fill:color}"/>
                    <div style="text-align: center;font-size: 12px;margin-top: 20px" v-text="name"></div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </el-card>

        </div>
      </el-col>
      <el-col :span="12">
        <el-card class="box-card"  style="margin-top: 25px">
            <div class="work">
              <d2-icon-svg name="work" style="margin-left: 50%;transform: translateX(-50%);height: 216px"/>
            </div>
          </el-card>

      </el-col>


    </el-row>

  </d2-container>
</template>

<script>
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from 'echarts/components'

use([
  CanvasRenderer,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
])
export default {
  name: 'workbench',
  data () {
    return {
      projects: [],
      navigators: [
        {
          name: 'Home',
          icon: 'home',
          route: {
            name: 'index'
          },
          color: 'rgb(31, 218, 202);'
        },
        {
          name: 'Department',
          icon: 'department',
          route: {
            name: 'dept'
          },
          color: 'rgb(225, 133, 37);'
        },
        {
          name: 'Role',
          icon: 'role',
          route: {
            name: 'role'
          },
          color: 'rgb(191, 12, 44);'
        },
        {
          name: 'Menu',
          icon: 'menu',
          route: {
            name: 'menu'
          },
          color: 'rgb(63, 178, 127);'
        },
        {
          name: 'User',
          icon: 'user',
          route: {
            name: 'user'
          },
          color: 'rgb(191, 12, 44);'
        },
        {
          name: 'Logs',
          icon: 'log',
          route: {
            name: 'operationLog'
          },
          color: 'rgb(0, 216, 255);'
        }
      ],
      chartData: {
        columns: ['date', 'sales'],
        rows: [
        { Date: 'January 1st', Sales: 123 },
           { Date: 'January 2', Sales: 1223 },
           { Date: 'January 3', Sales: 2123 },
           { Date: 'January 4th', Sales: 4123 },
           { Date: 'January 5th', Sales: 3123 },
           { Date: 'January 6th', Sales: 7123 }        
          ]
      }
    }
  },
  methods: {
    gotoRoute (route) {
      this.$router.push(route)
    }
  }
}
</script>

<style scoped lang="scss">

  $userAvatarLength: 72px;

  .page-header{
    box-sizing: border-box;
    padding: 16px;
    .user-avatar{
        width: $userAvatarLength;
        height: $userAvatarLength;
        line-height: $userAvatarLength;
      display: inline-block;
    }

    .title{
      display: inline-block;
      padding: 0 0 0 15px;
      position: relative;
      top: -5px;

      h1{
        font-size: 1.125rem;
        font-weight: 500;
        line-height: 1.75rem;
      }
      span{
        font-size: 14px;
        color: rgba(0,0,0,.45);
      }
    }

  }

  .project-detail{
    color: rgba(0,0,0,.45);
    height: 65px;
     img {
       width: 25px;
       height: 25px;
     }
    .name{
      margin-left: 1rem;
      font-size: 1rem;
      line-height: 2rem;
      height: 2rem;
      display: inline-block;
      color: rgba(0,0,0,.85);
      position: relative;
      top: -5px;
    }
    .slogan{
      font-size: 12px;
      padding: 5px 0;
      overflow:hidden;
      text-overflow:ellipsis;
      white-space:nowrap;
    }
    .team{
      font-size: 14px;
    }
  }

  .activity{
    padding: 0;
    .activity-avatar{
      width: 40px;
      height: 40px;
      line-height: 40px;
    }
    .activity-detail{
      padding: 10px;
      line-height: 15px;
      font-size: 14px;
      color: rgba(0,0,0,.85);
    }
  }
  .chart {
    height: 408px;
  }

  .el-divider--horizontal{
    margin: 4px 0;
    background: 0 0;
    border-top: 1px solid #e8eaec;

  }
  .el-card, .el-message {
    border-radius: 0;
  }
</style>
