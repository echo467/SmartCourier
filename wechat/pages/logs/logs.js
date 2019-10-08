import gcoord from '../../utils/gcoord.js'
Page({

  /**
   * 页面的初始数据
   */
  data: {
    kuaidigongsi: ['顺丰快递', '韵达快递', '申通快递', '天猫快递'],
    pointlist:['a','b'],
    num_point:"",
    index: "",
    phonenum: "",
    fajiannum: [1, 2, 3],
    num:"",
    //以下是小车携带信息
    fajianshu:"",//快递发件数
    point: "",//送达地点
    cupboard1phone: "",
    cupboard2phone: "",
    cupboard3phone: "",
    //用于复位
    res_sendToServer: {
      "id": "abc",
      "fajiannum": 0,
      "cupboard1State": "open", "cupboard1phone": "",
      "cupboard2State": "open", "cupboard2phone": "",
      "cupboard3State": "open", "cupboard3phone": "",
      "carState": "a",//待放，行进，待取
      "destination": ""

    },
    sendToServer: { 
      "id":"abc",
      "fajiannum": 0,
      "cupboard1State": "open", "cupboard1phone":"" ,
      "cupboard2State": "open", "cupboard2phone":"",
      "cupboard3State": "open", "cupboard3phone":"",
      "carState":"a",//待放 a，行进 b ，待取 c
      "destination":""},
    fix_num:0, //确认发件数和输入的手机号数量一致

     markers: [{
      iconPath: '../../images/mappoint.png',
      id: 0,
      latitude: 39.96174659643712,
      longitude: 116.35552389252058,
      width: 25,
      height: 50
    }],
  },
  onLoad:function(){
   
  },
  //下拉刷新
  onPullDownRefresh: function () {
    wx.showNavigationBarLoading() //在标题栏中显示加载
    setTimeout(function () {
      wx.hideNavigationBarLoading() //完成停止加载
      wx.stopPullDownRefresh() //停止下拉刷新
    }, 1500);
  },
  choosefajian: function (e) {
    this.setData({
      num: e.detail.value,
      fajianshu: this.data.fajiannum[e.detail.value]
    })
  },
  choosepoint:function(e){
    this.setData({
      num_point: e.detail.value,
      point: this.data.pointlist[e.detail.value]
    })
    console.log("point:"+this.data.point)
  },
  getphnum1: function (e) {
    this.setData({
      cupboard1phone: e.detail.value
    })
    console.log("手机后四位：" + this.data.cupboard1phone)
  },
  getphnum2: function (e) {
    this.setData({
      cupboard2phone: e.detail.value
    })
    console.log("手机后四位：" + this.data.cupboard2phone)
  },
  getphnum3: function (e) {
    this.setData({
      cupboard3phone: e.detail.value
    })
    console.log("手机后四位：" + this.data.cupboard3phone)
  },
  //判断是否为正确手机号
  validatemobile: function (mobile) {
    if (mobile.length == 0) {
      wx.showToast({
        title: '请输入手机号！',
        icon: 'success',
        duration: 1500
      })
      return false;
    }
    if (mobile.length != 11) {
      wx.showToast({
        title: '手机号长度有误！',
        icon: 'success',
        duration: 1500
      })
      return false;
    }
    var myreg = /^(((13[0-9]{1})|(15[0-9]{1})|(18[0-9]{1})|(17[0-9]{1}))+\d{8})$/;
    if (!myreg.test(mobile)) {
      wx.showToast({
        title: '手机号有误！',
        icon: 'success',
        duration: 1500
      })
      return false;
    }
    return true;
  },
  //确定输入的电话号码数量和发件数一致
  fixNum:function(){
    if (this.data.cupboard1phone != "") {
      this.setData({
        fix_num: this.data.fix_num + 1
      })
    }
    if (this.data.cupboard2phone != "") {
      this.setData({
        fix_num: this.data.fix_num + 1
      })
    }
    if (this.data.cupboard3phone != "") {
      this.setData({
        fix_num: this.data.fix_num + 1
      })
    }
  },
  //所有数据复位
  resetData:function(){
    let that=this;
    this.setData({
     /* cupboard1phone: "",
      cupboard2phone: "",
      cupboard3phone: "",*/
      fix_num: 0,
      sendToServer: that.data.res_sendToServer
    })
  },
  xiadan: function () {
    const db = wx.cloud.database()
    let that = this;
    let sendToServerx=this.data.res_sendToServer;
    this.fixNum()
    //如果发件数等于输入的手机号的数目
    if(that.data.fix_num==that.data.fajianshu)
    {
    if(that.data.cupboard1phone!="")
    { 
      if (!that.validatemobile(that.data.cupboard1phone))
      { that.resetData()
        return false
      }
      sendToServerx.cupboard1phone=this.data.cupboard1phone,
      sendToServerx.cupboard1State="close",
        db.collection('car_send').add({
          // data 字段表示需新增的 JSON 数据
          data: {
            point: that.data.point,
            phonenum: that.data.cupboard1phone,
            cupboard:1,
            state:"待取"
          },
        success(res) {
          console.log(res)
        },
        fail(res) {
          console.log(res)
        }
        })
    }
    else
    { sendToServerx.cupboard1phone="",
      sendToServerx.cupboard1State = "open"}
    if (that.data.cupboard2phone != "") {
      if (!that.validatemobile(that.data.cupboard2phone)) {
        that.resetData()
        return false
      }
      sendToServerx.cupboard2phone = this.data.cupboard2phone,
        sendToServerx.cupboard2State = "close",
        db.collection('car_send').add({//创建相应的数据库数据
          // data 字段表示需新增的 JSON 数据
          data: {
            point: that.data.point,
            phonenum: that.data.cupboard2phone,
            cupboard: 2,
            state: "待取"
          },
          success(res){
            console.log(res)
          },
          fail(res){
            console.log(res)
          }
        })
    }
    else { sendToServerx.cupboard2phone = "",
      sendToServerx.cupboard2State = "open" }
    if (that.data.cupboard3phone != "") {
      if (!that.validatemobile(that.data.cupboard3phone)) {
        that.resetData()
        return false
      }
         sendToServerx.cupboard3phone = this.data.cupboard3phone,
         sendToServerx.cupboard3State = "close",
        db.collection('car_send').add({
          // data 字段表示需新增的 JSON 数据
          data: {
            point: that.data.point,
            phonenum: that.data.cupboard3phone,
            cupboard: 3,
            state: "待取"
          }
        })
    }
    else { sendToServerx.cupboard3phone = "",
      sendToServerx.cupboard3State = "open" }
    sendToServerx.destination=that.data.point,
    sendToServerx.fajiannum=that.data.fajianshu,
    sendToServerx.carState="b"    //应该是b 行进，暂时改成c 待取
    this.setData({
       sendToServer:sendToServerx
    })
     console.log("--data--:0"+JSON.stringify(this.data.sendToServer))
     // console.log("--data--:0" + JSON.stringify(sendToServerx))
    console.log("fix_num:"+this.data.fix_num)
    wx.request({
      url: 'http://139.199.105.136:6888/car/send',
      data: { //'msg': JSON.stringify(that.data.sendToServer)
        //'msg':"ooooooooooo"
        "id": that.data.sendToServer.id,
        "fajiannum": that.data.sendToServer.fajiannum,
        "cupboard1State": that.data.sendToServer.cupboard1State, 
        "cupboard1phone": that.data.sendToServer.cupboard1phone,
        "cupboard2State": that.data.sendToServer.cupboard2State, 
        "cupboard2phone": that.data.sendToServer.cupboard2phone,
        "cupboard3State": that.data.sendToServer.cupboard3State, 
        "cupboard3phone": that.data.sendToServer.cupboard3phone,
        "carState": that.data.sendToServer.carState,//待放 a，行进 b ，待取 c
        "destination": that.data.sendToServer.destination
        },
      method: 'GET', 
      success: function (res) {
        wx.showToast({
          title: '发送成功！',
          icon: 'none',
          duration: 1000
        })
      }
    })
    
    }//如果发件数等于输入的手机号的数目
  else
  {   console.log("发件数："+that.data.fajianshu)
      console.log("fix_num：" + that.data.fix_num)
      wx.showToast({
        title: '请输入正确发件数',
        icon: 'none',
        duration: 2000
      })


  }
 this.resetData()
  }
})