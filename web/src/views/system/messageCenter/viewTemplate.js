export default {
  title: {
    title: 'Title',
    key: 'title',
    component: {
      span: 24,
      placeholder: 'Please enter a title',
      disabled: true
    },
    rules: [
      {
        required: true,
        message: 'required fields'
      }
    ],
    order: 10
  },
  content: {
    title: 'Content',
    key: 'content',
    component: {
      name: 'd2p-quill',
      span: 24,
      disabled: true,
      props: {
        uploader: {
          type: 'form'
        }
      },
      events: {}
    },
    rules: [
      {
        required: true,
        message: 'required fields'
      }
    ],
    order: 10
  }
}