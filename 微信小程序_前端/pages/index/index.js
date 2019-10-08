Page({

  /**
   * 页面的初始数据
   */
  data: {
  
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
    
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
    
  },
  getacc:function(e){
    console.log(e.detail.value)
    this.setData({
      accnum: e.detail.value
    })
  },
  getpassword:function(e){
    console.log(e.detail.value)
    this.setData({
      password: e.detail.value
    })
  },
  denglu:function(){
    let that=this;
    const db = wx.cloud.database()
    db.collection('car_users').where({
      password:that.data.password,
      accnum:that.data.accnum
    })
    .get({
      success: function (res) {
        if(!res){
          console.log(res.length)
         /* wx.showToast({
            title: '账号不存在或密码错误',
            icon: 'fail',
            duration: 2000
          })*/
        }
        else{
        console.log(res.data)
        wx.switchTab({
          url: '../users/users'
        })
        }
      },fail:function(){
       console.log("数据库出错")
      }
    })
   
  },
  zhuce:function(){
    wx.navigateTo({
      url: '../zhuce/zhuce',
    })
  }
})