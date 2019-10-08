// pages/zhuce/zhuce.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
     accnum:"",//账号
     password:"",//密码
     phonenum:"",//手机号
     identity:"",//身份
     items: [
      { name: 'student', value: '学生' },
      { name: 'courier', value: '快递员' }
    ]
  },
  checkboxChange: function (e) {
    console.log('checkbox发生change事件，携带value值为：', e.detail.value[0])
    this.setData({
      identity: e.detail.value[0]
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },
  getaccnum:function(e){
    console.log(e.detail.value)
    this.setData({
      accnum:e.detail.value
    })
  },
  getpassword:function(e){
    console.log(e.detail.value)
    this.setData({
      password: e.detail.value
    })
  },
  getphonenum:function(e){
    console.log(e.detail.value)
    this.setData({
      phonenum: e.detail.value
    })
  },
  successzc:function(){
    const db = wx.cloud.database()
    let that=this;
    db.collection('car_users').add({
      // data 字段表示需新增的 JSON 数据
      data: {
       accnum:that.data.accnum,
       password:that.data.password,
       identity:that.data.identity,
       phonenum:that.data.phonenum
      },
      success: function (res) {
        // res 是一个对象，其中有 _id 字段标记刚创建的记录的 id
        console.log(res)
        wx.showToast({
          title: '成功',
          icon: 'success',
          duration: 2000,
          success:function(){
            wx.navigateBack({
              delta: 1
            })
          }
        })
       

      }
    })
  
  }
})