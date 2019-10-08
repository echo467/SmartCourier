// 云函数入口文件
const cloud = require('wx-server-sdk');
cloud.init()
// 云函数入口函数
exports.main = async (event, context) => {
  console.log("这里是云函数")
  const db = cloud.database();
  const _ = cloud.database().command;
  const id = event.id;//该记录的唯一标识码
  const aopenid = event.aopenid;//用户的openid
  console.log(event)
  
  var chaxun=db.collection('dapei').where({
      _id: id,//所有保存了id在数据库中的记录
    }).get()
        .then(res => {
        console.log("查询成功")
        console.log(res.data[0])
        let index = res.data[0].dianzanid.indexOf(aopenid);
        console.log("index"+index);
        if ( index==-1) {//小于零即为未点赞过，所以该用户可以给这条分享点赞
           console.log("执行到了更新中")
       var dianzan=db.collection('dapei').doc(id).update({
            // data 传入需要局部更新的数据
            data: {
              dianzannum: _.inc(1),//点赞数加
              dianzanid: _.push(aopenid),//将点赞者的openid push进点赞集合中
            }
            }).then(res=>{wx.showModal({
              title: 'success',
              content: '点赞成功',
            })})
      }
        else { console.log("已经点过赞") }
      });return chaxun;

  return {
    event,
    id,
    aopenid
  
  }
}