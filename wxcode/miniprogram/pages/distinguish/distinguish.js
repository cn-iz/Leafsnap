//index.js
const app = getApp()

Page({
  data: {
   
  },
  sort: function (a) {
    var b = a.slice().sort(function (a, b) {
      return b - a;
    })
    var r = []
    wx.hideLoading()
    var url='/pages/result/result?c1='
    if (b[0] > 2.5) {
      url=url+(a.indexOf(b[0]) + 1)
    }
    else {
      wx.showToast({
        icon: 'none',
        title: '我们暂时无法识别！',
        duration:2000
      })
      return
    }
    if (b[1] > 2.5) {
      url = url+'&c2=' + (a.indexOf(b[1]) + 1)
    }else{
      url = url + '&c2=0'
    }
    wx.navigateTo({
      url: url
    })
  },
  predict:function(ph){
    wx.showLoading({
      title: '识别中',
    })
    var that=this
    wx.uploadFile({
      url: 'https://leaf.thatblog.cn/predict', 
      filePath: ph,
      name: 'img',
      success(res) {
        const data = res.data
        that.sort(JSON.parse(data))
      },
      fail(e) {
        wx.hideLoading()
        wx.showToast({
          icon: 'none',
          title: '提交失败，请检查网络连接！',
        })
        console.log(e)
      }
    })
  },
  takePh:function(){
    const ctx = wx.createCameraContext()
    var that=this
    ctx.takePhoto({
      quality: 'high',
      success: (res) => {
        that.predict(res.tempImagePath)
      }
    })
  },
  open_album:function(e){
    var that=this
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['album'],
      success(res) {
        that.predict(res.tempFilePaths[0])
      }
    })
  },
  more:function(e){
    wx.navigateBack({
      delta: 1
    })
  }
})
