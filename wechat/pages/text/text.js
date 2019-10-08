Page({

  /**
   * 页面的初始数据
   */
  data: {
    
  },
  upJW:function(){
    wx.request({
      url: 'http://10.33.32.9/home/www/root/static/carpos/pos2.txt/',
      method: 'GET',
    })
  }
})