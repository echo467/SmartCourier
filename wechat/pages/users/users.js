import gcoord from '../../utils/gcoord.js'
Page({

  /**
   * 页面的初始数据
   */
  data: {
    result_text: ["39.96174659643712","116.35552389252058"],
    deviceW:"",
    deviceH:"",
    car_longitude:"116.35765585552397",//小车经度
    car_latitude:"39.96095349639502",//小车纬度
    getJW_setInter:"",//得经纬度的计时器函数的编号
    ifshowMarkers:false,
    markers: [{
      iconPath: '../../images/mappoint.png',
      id: 0,
      latitude: "39.96174659643712", 
      longitude: "116.35552389252058", 
      width:25,
      height: 50
    }],
    currtab: 0,
    swipertab: [{ name: '待取', index: 0 }, { name: '地图查看', index: 1 }],
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
    // 页面渲染完成
    this.getDeviceInfo()
    this.orderShow()
  },
  //实现下拉刷新
  onPullDownRefresh: function () {
    let that=this;
    wx.showNavigationBarLoading() //在标题栏中显示加载
    setTimeout(function () {
      that.getkuaidiList()
      that.getCarstate()
      wx.hideNavigationBarLoading() //完成停止加载
      wx.stopPullDownRefresh() //停止下拉刷新
    }, 1500);
  },


  getDeviceInfo: function () {
    let that = this
    wx.getSystemInfo({
      success: function (res) {
        that.setData({
          deviceW: res.windowWidth,
          deviceH: res.windowHeight
        })
      }
    })
  },

  /**
  * @Explain：选项卡点击切换
  */
  tabSwitch: function (e) {
    var that = this
    if (this.data.currtab === e.target.dataset.current) {
      return false
    } else {
      that.setData({
        currtab: e.target.dataset.current
      })
    }
  },

  tabChange: function (e) {
    this.setData({ currtab: e.detail.current })
    this.orderShow()
    this.getCarstate()
  },

  orderShow: function () {
    let that = this
    switch (this.data.currtab) {
      case 0:
        that.alreadyShow()
        that.cancel_get_J_W()
        break
      case 1:
        that.getJ_W()
        break
    }
  },
  //得到未取快递列表
  getkuaidiList() {
    let that = this
    const db = wx.cloud.database();
    db.collection('car_send').where({
      phonenum: "18501155966",
      state: "待取"
    }).get({
      success: function (res) {
        console.log(res.data)
        that.setData({
          kuaidiList: res.data
        })
      }
    })
  },
  alreadyShow: function () {
    this.getkuaidiList()
  },

  //每隔5s得一次经纬度
  getJ_W: function () {
    let that = this;
    let alongitude="";
    let alatitude="";
    //将计时器赋值给setInter
    that.data.getJW_setInter = setInterval(
      function () {
       wx.request({
          url: 'http://139.199.105.136:6888/car/request',
          method: 'GET',
          success: function (res) {
            console.log("res.data.latitude=" + res.data.latitude)
            console.log("res.data.longitude=" + res.data.longitude)
            alatitude = res.data.latitude,
            alongitude=res.data.longitude;
          var result = gcoord.transform(
              [  alongitude,alatitude],    // 经纬度坐标
               gcoord.WGS84,                 // 当前坐标系 硬件GPS
                  gcoord.GCJ02);
          console.log("result="+result)
           that.setData({
             markers: [{
               iconPath: '../../images/mappoint.png',
               id: 0,
               latitude: result[1],
               longitude: result[0], 
               width: 25,
               height: 50
             }],
              car_latitude: result[0],
              car_longitude:result[1],
            
           })
            console.log("marker.longitude="+that.data.markers[0].longitude)
            console.log("marker.alatitude=" + that.data.markers[0].latitude)
          }
        })
        console.log("每隔5s获得一次经纬度")
        //发送给刘组
        var send_result = gcoord.transform(
          [alongitude, alatitude],    // 经纬度坐标
          gcoord.WGS84,                 // 当前坐标系 硬件GPS
          gcoord.BD09);
        wx.request({
          url: 'http://182.92.86.34:8099/apis/sendpos',
          method: 'GET',
          data:{
            latitude: send_result[1],
            longitude: send_result[0], 
          },
          success: function (res) {
            console.log("发送给合作组"+JSON.stringify(res))
          }
        })
      }
      , 5000); 
  },
  //取消获得经纬度的重复函数
  cancel_get_J_W:function(){
    let that=this;
    clearInterval(that.data.getJW_setInter)
  },
  chakan: function () {
    console.log("点击了查看")
  },
  //每一s得到小车的状态
  getCarstate:function()
  { let that=this;
    wx.request({
      url: 'http://139.199.105.136:6888/car/request',
      method: 'GET',
      success: function (res) {
        if (res.data.car_state=="c")
        {
          that.setData({
            ifArrive: true
          })
        }
       else{
          that.setData({
            ifArrive: false
          })
       }
        console.log(res.data.car_state)
      }
    })
 
  },
  //一键取件
  qujian: function (e) {
    let that = this;
    console.log(e.currentTarget.dataset.id) 
    if(that.data.ifArrive) 
    {
      wx.request({
        url: 'http://139.199.105.136:6888/car/send',
        data: {
          'openCupboard': e.currentTarget.dataset.cupboard,
          "change": ""
        },
        method: 'GET',
        success: function (res) {
          console.log(res)
        }
      })

      //将快递信息修改为已取件
      wx.cloud.callFunction({
        name: 'qujian',
        data: {
          id: e.currentTarget.dataset.id
        },
        success: function (res) {
          console.log(res),
            wx.showModal({
              title: 'success',
              content: '取件成功！',
            })
            that.getkuaidiList()
        },
        fail: console.error
      })
    }
    else
    {
      wx.showToast({
        title: '快递未到达！',
        icon: 'success',
        duration: 1500
      })
    }

  }

})
