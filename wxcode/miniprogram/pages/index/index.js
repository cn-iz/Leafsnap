// miniprogram/pages/more/more.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    title: ["识别", '识别范围','关于'],
    statusBarHeight:null,
    title_h:null,
    current:0,
    index:0,
    clumns:[],
    showCard:1,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that=this
    wx.getSystemInfo({
      success(res) {
        console.log(res)
        var title_h=48
        if (res.system.indexOf("iOS")){
          title_h = 44
        }
        that.setData({ statusBarHeight: res.statusBarHeight, title_h: title_h, showCard: Math.floor(Math.random() * 5)+1})
      }
    })
    // 识别范围
    const db = wx.cloud.database('izcode')
    that=this
    db.collection('clumns').get().then(res => {
      // res.data 是一个包含集合中有权限访问的所有记录的数据，不超过 20 条
      that.setData({clumns:res.data})
    })
  },
  recognition:function(e){
    wx.navigateTo({
      url: '/pages/distinguish/distinguish'
    })
  },
  bindanimationfinish:function(e){
    this.setData({
      index: e.detail.current
    })
  },
  video:function(){
    wx.navigateTo({
      url: '/pages/video/video'
    })
  }
})