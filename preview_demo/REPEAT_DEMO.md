# 订单监控演示页

原始视觉参考是 [Tabler 的 Tables 演示](https://preview.tabler.io/tables.html?theme=light) 和 [Dashboard](https://preview.tabler.io/?theme=light)：借鉴它的紧凑工具栏、清晰列表、状态标签及浅色界面。此处使用自建界面和演示订单，不是第三方网站的兼容性声明。

原有 `video-*.html`、`video-demo.js` 和 `video-demo.css` 保留，用于“刷新并点击”的资讯翻页场景。新建 `repeat-*.html` 用于“仅重复点击”的订单监控场景；两条演示线分别展示不同用途。

## 视频里的操作

1. 在订单页选择“待发货”。可以进一步搜索某件商品。
2. 在扩展里选择“仅重复点击”，直接选取订单页右侧的双箭头刷新图标。
3. 重新打开扩展，设置间隔并开始。
4. 展示新订单进入列表、选中的筛选条件保留，再打开扩展停止。

页面没有自动刷新定时器。新数据只在刷新图标收到真实点击后进入列表，筛选和搜索也实际参与结果计算；重载网页会恢复初始状态。因此录像能表现“按钮替你点，页面不用重来”。页面明确标注演示数据。

商店截图保留资讯页的“刷新并点击”场景。本轮预览视频重点展示订单页的图标选择和局部更新，每个设备系列、每种语言仍为一支视频。正式素材均从新版扩展在 Safari 中的实际操作录制。

## 生成与预览

十种语言的文字在 `repeat-copy.json`，共享交互在 `repeat-demo.js`，样式在 `repeat-demo.css`。修改源文件后运行：

```sh
python3 scripts/build_repeat_demo.py
python3 -m http.server 8769 --bind 127.0.0.1
```

打开 `/preview_demo/repeat-zh-hans.html`。页面右上角可切换十种语言，包括阿拉伯语从右到左布局。保留 `noindex,nofollow`，不加入网站 sitemap。

实际拍摄使用这些网页作为被操作的对象，不用它们替代扩展 UI。截图、录像及测试记录保存到项目已忽略的生成目录或临时目录，不放进此网站仓库。
