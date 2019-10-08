// 云函数入口文件
const cloud = require('wx-server-sdk');

cloud.init()
const db = cloud.database();
// 云函数入口函数
exports.main = async (event, context) => {
  try {
    return await db.collection('car_send').where({
      _id: event.id
    })
      .update({
        data: {
          state:"取件完成"
        },
      }).then(res => {
        console.log("执行到了这里")
      })
  } catch (e) {
    console.error(e)
  }
}