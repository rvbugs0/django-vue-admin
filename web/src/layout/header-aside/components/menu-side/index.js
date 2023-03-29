import { mapState } from 'vuex'
import menuMixin from '../mixin/menu'
import { createMenu } from '../libs/util.menu'
import BScroll from 'better-scroll'

export default {
   name: 'd2-layout-header-aside-menu-side',
   mixins: [
     menuMixin
   ],
   render(h) {
     return <div class="d2-layout-header-aside-menu-side">
       <el-menu
         collapse={ this.asideCollapse }
         collapseTransition={ this.asideTransition }
         uniqueOpened={true}
         defaultActive={ this. $route. fullPath }
         ref="menu"
         onSelect={ this. handleMenuSelect }>
         { this. aside. map(menu => createMenu. call(this, h, menu)) }
       </el-menu>
       {
         this.aside.length === 0 && !this.asideCollapse
           ? <div class="d2-layout-header-aside-menu-empty" flex="dir:top main:center cross:center">
             <d2-icon name="inbox"></d2-icon>
             <span>No sidebar menu</span>
           </div>
           : null
       }
     </div>
   },
   data () {
     return {
       asideHeight: 300,
       BS: null
     }
   },
   computed: {
     ...mapState('d2admin/menu', [
       'aside',
       'asideCollapse',
       'asideTransition'
     ])
   },
   watch: {
     // Destroy better scroll when menu is collapsed and expanded
     asideCollapse (val) {
       this. scrollDestroy()
       setTimeout(() => {
         this. scrollInit()
       }, 500)
     }
   },
   mounted () {
     this. scrollInit()
   },
   beforeDestroy () {
     this. scrollDestroy()
   },
   methods: {
     scrollInit() {
       this.BS = new BScroll(this.$el, {
         mouseWheel: true,
         click: true
         // You can turn on scrollbars if you want
         // scrollbar: {
         // fade: true,
         // interactive: false
         // }
       })
     },
     scrollDestroy () {
       // https://github.com/d2-projects/d2-admin/issues/75
       try {
         this. BS. destroy()
       } catch (e) {
         delete this.BS
         this.BS = null
       }
     }
   }
}