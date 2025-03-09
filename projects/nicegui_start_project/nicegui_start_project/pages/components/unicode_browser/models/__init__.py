"""
### 通用命名原则
场景	            推荐后缀	    示例	            适用说明
纯数据容器	        Record	    UserRecord	        表示不可变数据集合
数据模型（ORM/ODM）	Model	    UserModel	        与数据库表/集合直接映射
验证/序列化模型	    Schema	    UserCreateSchema	用于请求/响应数据校验
数据传输对象（DTO）	DTO	        UserDTO	            跨层传输数据的载体
业务逻辑实体	        Entity	    UserEntity	        核心业务领域对象
配置类	            Config	    DatabaseConfig	    参数配置类
服务类	            Service	    UserService	        业务逻辑处理类

### 数据传输对象（DTO）
> **一种设计模式**，主要用于在不同系统层之间高效、安全地传输数据。

以下是关于 DTO 的详细解析：
- 目的：DTO 用于封装数据，**减少网络传输量**，隐藏内部数据结构，降低层间耦合。
- 结构：通常为纯数据容器，仅包含字段、getter/setter 方法，不包含业务逻辑。

使用场景：
- 接口传参：REST API的请求/响应体中定义DTO，避免暴露实体细节。
- 数据脱敏：过滤敏感字段（如password），仅传递必要数据（如username, email）。
- 数据聚合：组合多个实体的字段，简化前端调用（如订单详情包含用户信息）。



"""

from .entities import *
