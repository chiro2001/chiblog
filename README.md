# chiblog

## 整体描述

是我的博客哟。

## 功能需求分析

1. 发表内容功能
   1. 内容分种类，每种种类对应不同类型的展示卡片
   2. 内容需要分类，用`Tag`、文件夹等做分类
   3. 参照`Notion`的`Page`类型，可以做到内容内嵌、内容引用、循环引用等
2. 内容编辑功能
   1. 可以在线编辑发布的内容，提供在线编辑器
   2. 提供图床（并且提供防盗链等可选功能）
   3. 文件编辑功能
      1. 从`git`按文件同步文章内容
3. 功能扩展模块
   1. 按照模块布置安装
      1. `API`按照模块编写和发布
      2. 前端按照模块编写和排版
4. 方便部署功能
   1. 提供一键转换为`serverless`，有利于发布到`Serverless`平台
5. 其他人发表内容功能
   1. 对本人发表的内容发布评论、点赞等
   2. 可以发布文章、留言
   3. 有操作权限限制
6. 实时互动功能
   1. 插入实时聊天功能
   2. 一键和本人发消息联系
7. 发表内容同步
   1. 可以在发表文章的时候在其他平台同步文章数据（最好还有评论和点赞等数据）

## 技术难点分析

1. 前端内容排布
   1. 需要瀑布流吧...如果真的有那么多数据的话
   2. 是否能够提供一种文件格式来排版（估计不能）
2. 后端`API`模块
   1. 按照模块来规划
   2. 按照`USGI`模块来组合
3. 后端数据库使用
   1. 使用`MongoDB`
   2. 放在同一个`Database`不同`Collection`里面
4. 前端`API`使用
5. 前端`Redux`数据管理
6. 前端内容编辑功能
   1. 是否用开源`Markdown`编辑器

## 详细分计划

[前端](./frontend/README.md)

[后端](./backend/README.md)