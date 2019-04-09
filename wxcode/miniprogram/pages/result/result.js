// miniprogram/pages/result/result.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    data:null,
    clumns:[],
    statusBarHeight: null,
    title_h: null,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var r=[]
    if(options.c2>0){
      r.push(parseInt(options.c1))
      r.push(parseInt(options.c2))
    }else{
      r.push(parseInt(options.c1))
    }
    const db = wx.cloud.database('izcode')
    var that = this
    const _ = db.command
    db.collection('clumns')
      .where({
        _id: _.in(r)
      })
      .get()
      .then(res => {
        that.setData({ clumns: res.data })
      })
      .catch(console.error)
    
    wx.getSystemInfo({
      success(res) {
        var title_h = 48
        if (res.system.indexOf("iOS")) {
          title_h = 44
        }
        that.setData({ statusBarHeight: res.statusBarHeight, title_h: title_h })
      }
    })
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
  close:function(e){
    wx.navigateBack({
      delta: 1
    })
  }
})