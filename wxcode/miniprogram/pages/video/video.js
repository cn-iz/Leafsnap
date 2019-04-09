// miniprogram/pages/video/video.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    time:0,
    isruning: false
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
  timer:null,
  end:function(){
    clearInterval(this.timer)
    wx.showLoading({
      title: '识别中',
      mask: true,
    })
    var cc = wx.createCameraContext()
    var that = this
    cc.stopRecord({
      // tempThumbPath
      // tempVideoPath
      success: function (res) {
        that.up_video(res.tempVideoPath)
        // console.log(res)
      },
      fail: function (res) {
        that.setData({ isruning: false })
      }
    })
  },
  start:function(){
    var cc=wx.createCameraContext()
    var that=this
    this.setData({ time: 0 })
    that.timer = setInterval(function () {
      that.setData({ time: Math.floor((that.data.time + 0.2) * 10) / 10 })
    }, 200)
    this.setData({ isruning: true })
    cc.startRecord({
      timeoutCallback: function (res) {
        that.up_video(res.tempVideoPath)
      }
    })
  },
  up_video:function(video){
    this.setData({ isruning: false })
    this.setData({ time: 0 })
    var that = this
    wx.uploadFile({
      url: 'https://leaf.thatblog.cn/predict_video',
      filePath: video,
      name: 'video',
      success(res) {
        const data = res.data
        that.sort(JSON.parse(data))
      },
      fail(e) {
        wx.hideLoading()
        // wx.showToast({
        //   title: '提交失败，请检查网络连接！',
        // })
        console.log(e)
      }
    })
  },
  sort: function (a) {
    var b = a.slice().sort(function (a, b) {
      return b - a;
    })
    var r = []
    wx.hideLoading()
    var url = '/pages/result/result?c1='
    if (b[0] > 2.5) {
      url = url + (a.indexOf(b[0]) + 1)
    }
    else {
      wx.showToast({
        icon: 'none',
        title: '我们暂时无法识别！',
        duration: 2000
      })
      return
    }
    if (b[1] > 2.5) {
      url = url + '&c2=' + (a.indexOf(b[1]) + 1)
    } else {
      url = url + '&c2=0'
    }
    wx.navigateTo({
      url: url
    })
  },
  open_album:function(e){
    wx.chooseVideo({
      sourceType: ['album'],
      maxDuration: 60,
      camera: 'back',
      success(res) {
        wx.showLoading({
          title: '识别中',
          mask: true,
        })
        up_video(res.tempFilePath)
      }
    })
  }
})