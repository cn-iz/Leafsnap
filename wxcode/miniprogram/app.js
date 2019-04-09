//app.js
App({
  onLaunch: function () {
    wx.cloud.init({
      env: 'izcode-a08893'
    })
    this.globalData = {}
  }
})
