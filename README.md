# CIBot (oldname Qabot)
    
    A hybrid chat-bot enhanced by crowd intelligence.

- **Architecture**
  - 依赖一个在线聊天平台，以及基于该平台的SDK/命令行客户端/机器人作适配器
    - Wechat + [wxBot](https://github.com/liuwons/wxBot)
    - Discord + [discord.py](https://github.com/Rapptz/discord.py)
  - 这个Django工程本身作为数据库管理+信息处理中枢
  - 推荐有问答AI接口(可选)
    - [QA-Snake](https://github.com/SnakeHacker/QA-Snake)
    - [图灵机器人](http://www.tuling123.com/)

- **Run**
  -  cd bin
  - ./QaBot.sh start

- **Port Info**
  - 8000    Django
  - 50000   QA-SNAKE
