import { find, assign } from 'lodash'

const users = [
   { username: 'admin', password: 'admin', uuid: 'admin-uuid', name: 'Admin' },
   { username: 'editor', password: 'editor', uuid: 'editor-uuid', name: 'Editor' },
   { username: 'user1', password: 'user1', uuid: 'user1-uuid', name: 'User1' }
]

export default ({ service, request, serviceForMock, requestForMock, mock, faker, tools }) => ({
   /**
    * @description login
    * @param {Object} data The information carried by the login
    */
   SYS_USER_LOGIN(data = {}) {
     // mock data
     mock
       .onAny('/login')
       .reply(config => {
         const user = find(users, tools. parse(config. data))
         return user
           ? tools.responseSuccess(assign({}, user, { token: faker.random.uuid() }))
           : tools.responseError({}, 'Account or password is incorrect')
       })
     // interface request
     return requestForMock({
       url: '/login',
       method: 'post',
       data
     })
   }
})