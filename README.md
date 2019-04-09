# Leafsnap
迁移学习 inception_v3， 利用视频、图片生成中间特征，并用中间特征训练新建logits层，建立识别模型；利用flask开放接口；搭建基于微信小程序的前端识别程序。

## 结构说明
* web_api 为服务器端包括flask搭建api，tensorflow迁移学习inception_v3构建和训练识别模型的代码
* wxcode 为前端微信小程序代码
