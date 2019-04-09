// miniprogram/pages/save/save.js
Page({
  data: {
    ph:null
  },
  onLoad: function (options) {
    this.setData({
      ph:options.ph
    })
  },
  savePh: function () {
    wx.saveImageToPhotosAlbum({
      filePath: this.data.ph,
      success(res) {
        wx.navigateBack({
          delta: -1
        });
      }
    })
  }
})