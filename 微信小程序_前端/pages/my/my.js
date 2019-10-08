// pages/xiadan/xiadan.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    array: ['顺丰快递', '韵达快递', '申通快递', '天猫快递'],
    index:"",
    name:"",
    phonenum:"",
    whatkuaidi:""
  },
  bindPickerChange: function (e) {
    console.log('picker发送选择改变，携带值为', e.detail.value)
    this.setData({
      index: e.detail.value,
      whatkuaidi: this.data.array[e.detail.value]
    })
    console.log("快递公司是："+this.data.whatkuaidi)
  },
  getname:function(e){
    this.setData({
      name: e.detail.value
      })
    console.log("姓名："+this.data.name)
  },
  getphnum:function(e){
    this.setData({
      phonenum:e.detail.value
    })
    console.log("手机后四位："+this.data.phonenum)
  }
})