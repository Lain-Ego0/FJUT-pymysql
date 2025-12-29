# FJUT-pymysql
# 图书借阅管理系统完整解决方案
## 一、系统分析报告
### （一）系统功能分析
#### 1.  核心用户角色
系统分为**管理员**和**借阅者**两大核心角色，权限边界清晰：
- 管理员：负责系统整体维护、数据管理及业务审核
- 借阅者：负责个人借阅业务办理及信息查询

#### 2.  整体功能梳理
系统围绕图书借阅全流程设计，覆盖“图书管理-借阅者管理-借阅归还-逾期管控-统计分析”五大核心业务，具体功能如下：
1.  图书管理功能：图书信息的录入、修改、删除、模糊查询（按书名/ISBN/出版社/作者），确保馆藏图书数据准确完整
2.  借阅者管理功能：借书证办理（信息录 入）、信息修改、借书证注销、借阅者信息查询，绑定借阅者核心身份信息
3.  借阅归还功能：借书操作（校验借阅限额）、还书操作（校验逾期状态）、借阅记录查询（按借阅者/图书/日期）
4.  逾期管理功能：自动检测逾期图书、生成逾期提醒、逾期罚款登记，管控借阅期限风险
5.  辅助查询统计功能：图书借阅排行、借阅者借阅统计、馆藏图书库存统计，为图书室管理提供数据支撑

#### 3.  关键业务约束
-  借阅限额：每位借阅者每次最多借阅8本图书
-  借阅期限：单本图书最长借阅期限为30天
-  数据唯一性：图书ISBN（书号）唯一、借书证ID唯一

### （二）系统功能模块设计
#### 1.  功能模块结构图
```
图书借阅管理系统
├── 图书管理模块
│   ├── 图书信息录入
│   ├── 图书信息修改/删除
│   ├── 图书信息模糊查询
├── 借阅者管理模块
│   ├── 借书证办理（借阅者录入）
│   ├── 借阅者信息修改/注销
│   ├── 借阅者信息查询
├── 借阅业务模块
│   ├── 借书操作（限额校验）
│   ├── 还书操作（逾期校验）
│   ├── 借阅记录多条件查询
├── 逾期管理模块
│   ├── 逾期图书自动检测
│   ├── 逾期信息提醒
│   ├── 逾期罚款登记
├── 统计分析模块
│   ├── 图书借阅热度排行
│   ├── 借阅者借阅次数统计
│   ├── 馆藏图书分类统计
```

#### 2.  各模块核心职责
| 模块名称         | 核心职责                                                                 |
|------------------|--------------------------------------------------------------------------|
| 图书管理模块     | 维护馆藏图书基础数据，确保图书信息可查、可改、可追溯                     |
| 借阅者管理模块   | 维护借阅者身份数据，作为借书、还书业务的身份凭证                         |
| 借阅业务模块     | 执行核心借书/还书流程，校验业务约束（8本限额、30天期限），生成借阅记录   |
| 逾期管理模块     | 监控借阅超期情况，记录罚款信息，降低图书逾期未还的风险                   |
| 统计分析模块     | 汇总业务数据，为图书室采购、管理优化提供决策支持                         |

### （三）数据库数据字典
#### 1.  核心实体及字段定义
| 表名               | 字段名称         | 数据类型         | 长度 | 主键/外键 | 非空 | 字段说明                                   |
|--------------------|------------------|------------------|------|-----------|------|--------------------------------------------|
| book（图书表）     | isbn             | varchar          | 20   | 主键      | 是   | 图书编号（ISBN），唯一标识                 |
|                    | book_name        | varchar          | 100  | -         | 是   | 图书名称                                   |
|                    | publisher        | varchar          | 50   | -         | 是   | 出版社名称                                 |
|                    | price            | decimal(10,2)    | -    | -         | 是   | 图书定价                                   |
|                    | content_intro    | text             | -    | -         | 否   | 图书内容简介                               |
|                    | is_delete        | tinyint          | 1    | -         | 是   | 逻辑删除标记（0=未删除，1=已删除）         |
| author（作者表）   | author_id        | int              | 11   | 主键      | 是   | 作者唯一标识，自增                         |
|                    | author_name      | varchar          | 20   | -         | 是   | 作者姓名（译者姓名）                       |
|                    | author_intro     | text             | -    | -         | 否   | 作者简介                                   |
| book_author（图书-作者关联表） | book_isbn | varchar | 20 | 外键（关联book.isbn） | 是 | 图书ISBN |
|                    | author_id        | int              | 11   | 外键（关联author.author_id） | 是   | 作者ID |
| borrower（借阅者表/借书证） | borrower_id | varchar | 15 | 主键 | 是 | 借书证编号，唯一标识 |
|                    | borrower_name    | varchar          | 20   | -         | 是   | 借阅者姓名                                 |
|                    | unit             | varchar          | 50   | -         | 是   | 借阅者所在单位                             |
|                    | occupation       | varchar          | 20   | -         | 是   | 借阅者职业                                 |
|                    | phone            | varchar          | 11   | -         | 否   | 联系电话（用于逾期提醒）                   |
|                    | is_valid         | tinyint          | 1    | -         | 是   | 借书证有效标记（0=无效，1=有效）           |
| borrow_record（借阅记录表） | record_id | int | 11 | 主键 | 是 | 借阅记录ID，自增 |
|                    | borrower_id      | varchar          | 15   | 外键（关联borrower.borrower_id） | 是   | 借书证编号 |
|                    | book_isbn        | varchar          | 20   | 外键（关联book.isbn） | 是   | 图书ISBN |
|                    | borrow_date      | datetime         | -    | -         | 是   | 借阅日期                                   |
|                    | due_date         | datetime         | -    | -         | 是   | 应还日期（借阅日期+30天）                  |
|                    | return_date      | datetime         | -    | -         | 否   | 实际还书日期（未还则为null）               |
|                    | borrow_status    | tinyint          | 1    | -         | 是   | 借阅状态（0=未归还，1=已归还，2=逾期未还） |
|                    | fine_amount      | decimal(10,2)    | -    | -         | 否   | 逾期罚款金额（未逾期则为0）                 |

#### 2.  字段约束说明
-  唯一约束：`book.isbn`、`borrower.borrower_id` 确保数据唯一性
-  外键约束：`book_author`、`borrow_record` 关联核心表，保证数据一致性
-  逻辑删除：`book.is_delete`、`borrower.is_valid` 避免物理删除导致数据丢失
-  业务约束：`borrow_record.due_date` 由业务逻辑自动生成（借阅日期+30天）

### （四）数据库概念结构（E-R图）
#### 1.  核心实体
-  图书（Book）：属性为isbn、book_name、publisher、price、content_intro、is_delete
-  作者（Author）：属性为author_id、author_name、author_intro
-  借阅者（Borrower）：属性为borrower_id、borrower_name、unit、occupation、phone、is_valid
-  借阅记录（BorrowRecord）：属性为record_id、borrow_date、due_date、return_date、borrow_status、fine_amount

#### 2.  实体间关系
1.  图书（Book）与作者（Author）：**多对多关系**（一本图书可由多名作者编写，一名作者可编写多本图书），通过中间表`book_author`关联
2.  借阅者（Borrower）与图书（Book）：**多对多关系**（一名借阅者可借多本图书，一本图书可被多名借阅者借阅），通过中间表`borrow_record`关联（借阅记录同时存储业务状态信息）
3.  借阅者（Borrower）与借阅记录（BorrowRecord）：**一对多关系**（一名借阅者可产生多条借阅记录）
4.  图书（Book）与借阅记录（BorrowRecord）：**一对多关系**（一本图书可产生多条借阅记录）

#### 3.  E-R图简化示意图
```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│   Book      │       │ book_author  │       │   Author    │
├─────────────┤       ├──────────────┤       ├─────────────┤
│ isbn(PK)    │◄─────►│ book_isbn(FK)│       │ author_id(PK)│
│ book_name   │       │ author_id(FK)│◄─────►│ author_name │
│ publisher   │       └──────────────┘       │ author_intro│
│ price       │                               └─────────────┘
│ content_intro│
│ is_delete   │
└─────────────┘
       ▲
       │
       │
┌──────────────┐       ┌─────────────┐
│ borrow_record│       │  Borrower   │
├──────────────┤       ├─────────────┤
│ record_id(PK)│       │ borrower_id(PK)│
│ borrower_id(FK)│◄────►│ borrower_name │
│ book_isbn(FK) │       │ unit         │
│ borrow_date  │       │ occupation   │
│ due_date     │       │ phone        │
│ return_date  │       │ is_valid     │
│ borrow_status│       └─────────────┘
│ fine_amount │
└──────────────┘
```

### （五）数据库表、视图、存储过程SQL定义
#### 1.  数据库及表创建SQL（MySQL 8.0）
```sql
-- 1. 创建数据库
CREATE DATABASE IF NOT EXISTS book_borrow_system DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. 使用数据库
USE book_borrow_system;

-- 3. 创建图书表
CREATE TABLE IF NOT EXISTS book (
    isbn VARCHAR(20) NOT NULL COMMENT '图书ISBN编号',
    book_name VARCHAR(100) NOT NULL COMMENT '图书名称',
    publisher VARCHAR(50) NOT NULL COMMENT '出版社',
    price DECIMAL(10,2) NOT NULL COMMENT '图书定价',
    content_intro TEXT COMMENT '图书内容简介',
    is_delete TINYINT(1) NOT NULL DEFAULT 0 COMMENT '逻辑删除标记 0-未删除 1-已删除',
    PRIMARY KEY (isbn),
    INDEX idx_book_name (book_name),
    INDEX idx_publisher (publisher)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='图书信息表';

-- 4. 创建作者表
CREATE TABLE IF NOT EXISTS author (
    author_id INT(11) NOT NULL AUTO_INCREMENT COMMENT '作者唯一ID',
    author_name VARCHAR(20) NOT NULL COMMENT '作者姓名',
    author_intro TEXT COMMENT '作者简介',
    PRIMARY KEY (author_id),
    INDEX idx_author_name (author_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='作者信息表';

-- 5. 创建图书-作者关联表
CREATE TABLE IF NOT EXISTS book_author (
    book_isbn VARCHAR(20) NOT NULL COMMENT '图书ISBN',
    author_id INT(11) NOT NULL COMMENT '作者ID',
    PRIMARY KEY (book_isbn, author_id),
    FOREIGN KEY (book_isbn) REFERENCES book(isbn) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (author_id) REFERENCES author(author_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='图书-作者关联表（多对多）';

-- 6. 创建借阅者表（借书证信息）
CREATE TABLE IF NOT EXISTS borrower (
    borrower_id VARCHAR(15) NOT NULL COMMENT '借书证编号',
    borrower_name VARCHAR(20) NOT NULL COMMENT '借阅者姓名',
    unit VARCHAR(50) NOT NULL COMMENT '所在单位',
    occupation VARCHAR(20) NOT NULL COMMENT '职业',
    phone VARCHAR(11) COMMENT '联系电话',
    is_valid TINYINT(1) NOT NULL DEFAULT 1 COMMENT '借书证有效标记 0-无效 1-有效',
    PRIMARY KEY (borrower_id),
    INDEX idx_borrower_name (borrower_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='借阅者（借书证）信息表';

-- 7. 创建借阅记录表
CREATE TABLE IF NOT EXISTS borrow_record (
    record_id INT(11) NOT NULL AUTO_INCREMENT COMMENT '借阅记录ID',
    borrower_id VARCHAR(15) NOT NULL COMMENT '借书证编号',
    book_isbn VARCHAR(20) NOT NULL COMMENT '图书ISBN',
    borrow_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '借阅日期',
    due_date DATETIME NOT NULL COMMENT '应还日期（借阅+30天）',
    return_date DATETIME COMMENT '实际还书日期',
    borrow_status TINYINT(1) NOT NULL DEFAULT 0 COMMENT '借阅状态 0-未归还 1-已归还 2-逾期未还',
    fine_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '逾期罚款金额',
    PRIMARY KEY (record_id),
    FOREIGN KEY (borrower_id) REFERENCES borrower(borrower_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (book_isbn) REFERENCES book(isbn) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_borrower_id (borrower_id),
    INDEX idx_book_isbn (book_isbn),
    INDEX idx_borrow_status (borrow_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='图书借阅记录表';
```

#### 2.  数据库视图创建SQL
```sql
-- 视图1：当前未归还图书视图（含借阅者+图书信息）
CREATE VIEW v_unreturned_books AS
SELECT
    br.record_id,
    b.borrower_id,
    b.borrower_name,
    b.unit,
    book.isbn,
    book.book_name,
    book.publisher,
    br.borrow_date,
    br.due_date,
    br.borrow_status
FROM
    borrow_record br
    LEFT JOIN borrower b ON br.borrower_id = b.borrower_id
    LEFT JOIN book ON br.book_isbn = book.isbn
WHERE
    br.borrow_status IN (0, 2)
    AND book.is_delete = 0
    AND b.is_valid = 1;

-- 视图2：逾期图书视图（含逾期天数+罚款信息）
CREATE VIEW v_overdue_books AS
SELECT
    br.record_id,
    b.borrower_id,
    b.borrower_name,
    b.phone,
    book.isbn,
    book.book_name,
    br.borrow_date,
    br.due_date,
    br.fine_amount,
    DATEDIFF(CURRENT_TIMESTAMP, br.due_date) AS overdue_days
FROM
    borrow_record br
    LEFT JOIN borrower b ON br.borrower_id = b.borrower_id
    LEFT JOIN book ON br.book_isbn = book.isbn
WHERE
    br.borrow_status = 2
    AND book.is_delete = 0
    AND b.is_valid = 1;
```

#### 3.  数据库存储过程创建SQL
```sql
-- 存储过程1：借书操作（自动校验8本限额，生成应还日期）
DELIMITER //
CREATE PROCEDURE proc_borrow_book(
    IN p_borrower_id VARCHAR(15),
    IN p_book_isbn VARCHAR(20),
    OUT p_result INT -- 0-失败 1-成功 2-已借满8本 3-借书证无效 4-图书已删除
)
BEGIN
    DECLARE v_borrow_count INT DEFAULT 0;
    DECLARE v_is_valid TINYINT DEFAULT 0;
    DECLARE v_is_delete TINYINT DEFAULT 1;
    DECLARE v_due_date DATETIME;

    -- 1. 查询借书证有效性
    SELECT is_valid INTO v_is_valid FROM borrower WHERE borrower_id = p_borrower_id;
    -- 2. 查询图书是否未删除
    SELECT is_delete INTO v_is_delete FROM book WHERE isbn = p_book_isbn;
    -- 3. 查询当前未归还图书数量
    SELECT COUNT(*) INTO v_borrow_count FROM borrow_record WHERE borrower_id = p_borrower_id AND borrow_status IN (0, 2);

    -- 4. 业务校验
    IF v_is_valid != 1 THEN
        SET p_result = 3; -- 借书证无效
    ELSEIF v_is_delete != 0 THEN
        SET p_result = 4; -- 图书已删除
    ELSEIF v_borrow_count >= 8 THEN
        SET p_result = 2; -- 已借满8本
    ELSE
        -- 计算应还日期（借阅日期+30天）
        SET v_due_date = DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 30 DAY);
        -- 插入借阅记录
        INSERT INTO borrow_record (borrower_id, book_isbn, due_date)
        VALUES (p_borrower_id, p_book_isbn, v_due_date);
        SET p_result = 1; -- 借书成功
    END IF;
END //
DELIMITER ;

-- 存储过程2：还书操作（自动检测逾期，计算罚款，默认每天0.1元）
DELIMITER //
CREATE PROCEDURE proc_return_book(
    IN p_record_id INT,
    OUT p_result INT -- 0-失败 1-成功 2-记录不存在 3-已归还
)
BEGIN
    DECLARE v_borrow_status TINYINT DEFAULT -1;
    DECLARE v_due_date DATETIME;
    DECLARE v_overdue_days INT DEFAULT 0;
    DECLARE v_fine DECIMAL(10,2) DEFAULT 0.00;

    -- 1. 查询借阅记录状态
    SELECT borrow_status, due_date INTO v_borrow_status, v_due_date FROM borrow_record WHERE record_id = p_record_id;

    -- 2. 校验记录状态
    IF v_borrow_status = -1 THEN
        SET p_result = 2; -- 记录不存在
    ELSEIF v_borrow_status = 1 THEN
        SET p_result = 3; -- 已归还
    ELSE
        -- 3. 计算逾期天数及罚款
        SET v_overdue_days = DATEDIFF(CURRENT_TIMESTAMP, v_due_date);
        IF v_overdue_days > 0 THEN
            SET v_fine = v_overdue_days * 0.10; -- 每天0.1元罚款
            -- 更新为逾期已归还
            UPDATE borrow_record
            SET return_date = CURRENT_TIMESTAMP,
                borrow_status = 1,
                fine_amount = v_fine
            WHERE record_id = p_record_id;
        ELSE
            -- 更新为正常已归还
            UPDATE borrow_record
            SET return_date = CURRENT_TIMESTAMP,
                borrow_status = 1
            WHERE record_id = p_record_id;
        END IF;
        SET p_result = 1; -- 还书成功
    END IF;
END //
DELIMITER ;

-- 存储过程3：批量检测逾期图书（更新借阅状态为2-逾期未还）
DELIMITER //
CREATE PROCEDURE proc_check_overdue_books()
BEGIN
    UPDATE borrow_record
    SET borrow_status = 2
    WHERE
        borrow_status = 0
        AND due_date < CURRENT_TIMESTAMP
        AND return_date IS NULL;
END //
DELIMITER ;
```

## 二、程序设计报告
### （一）运行环境与开发环境
#### 1.  运行环境
| 环境类型       | 具体配置                                                                 |
|----------------|--------------------------------------------------------------------------|
| 客户端环境     | 操作系统：Windows 10/11 或 macOS Monterey+<br>浏览器：Chrome 90+/Edge 90+<br>分辨率：1366×768及以上 |
| 服务端环境     | 操作系统：Windows Server 2019 或 CentOS 7+/Ubuntu 20.04+<br>Web服务器：Tomcat 9.0 或 Nginx 1.20+<br>数据库服务：MySQL 8.0+<br>内存：8GB 及以上<br>硬盘：100GB 及以上 |
| 网络环境       | 局域网（内网部署）或公网（需配置端口映射/域名解析），带宽10Mbps及以上     |

#### 2.  开发环境
| 开发类别       | 具体选型                                                                 |
|----------------|--------------------------------------------------------------------------|
| 开发语言       | 后端：Java 8/17（主流稳定）或 Python 3.9+<br>前端：HTML5+CSS3+JavaScript+jQuery |
| 开发IDE        | 后端：IntelliJ IDEA 2023（Java）或 PyCharm 2023（Python）<br>前端：VS Code |
| 数据库工具     | Navicat 16 或 DBeaver（跨平台免费）                                      |
| 框架选型       | 后端：Spring Boot 2.7.x（Java）或 Flask 2.3.x（Python）<br>持久层：MyBatis 3.5.x（Java）或 SQLAlchemy 2.0.x（Python）<br>前端：Vue 3.0（可选，简化交互） |
| 版本控制       | Git + Gitee/GitHub（代码管理与版本回溯）                                  |

### （二）程序详细设计
#### 1.  模块之间的关系
各模块通过**数据库中间件**实现数据交互，形成闭环业务流程，核心关系如下：
1.  依赖关系：图书管理模块、借阅者管理模块为借阅业务模块提供基础数据支撑；借阅业务模块产生的借阅记录为逾期管理模块、统计分析模块提供数据源
2.  数据交互：所有模块通过操作数据库表/视图/存储过程实现数据读写，无直接模块耦合，便于维护扩展
3.  业务闭环：借书→借阅记录生成→逾期检测→还书→记录归档→统计分析，覆盖图书借阅全生命周期

#### 2.  各模块功能详细说明
| 模块名称         | 子功能         | 详细功能描述                                                                 |
|------------------|----------------|------------------------------------------------------------------------------|
| 图书管理模块     | 图书录入       | 录入ISBN、书名、出版社、定价、简介，关联作者（支持多选），校验ISBN唯一性     |
|                  | 图书修改/删除  | 按ISBN查询图书，修改非ISBN字段；执行逻辑删除（更新is_delete=1），不物理删除 |
|                  | 图书查询       | 支持按书名（模糊）、ISBN（精确）、出版社（模糊）、作者（模糊）组合查询       |
| 借阅者管理模块   | 借书证办理     | 录入借书证ID、姓名、单位、职业、电话，校验借书证ID唯一性，生成有效借书证     |
|                  | 信息修改/注销  | 按借书证ID查询借阅者，修改姓名/单位/电话；注销（更新is_valid=0），保留数据   |
|                  | 借阅者查询     | 支持按姓名（模糊）、借书证ID（精确）、单位（模糊）组合查询                   |
| 借阅业务模块     | 借书操作       | 输入借书证ID、图书ISBN，调用proc_borrow_book存储过程，返回操作结果（成功/失败原因） |
|                  | 还书操作       | 输入借阅记录ID，调用proc_return_book存储过程，自动计算逾期罚款，返回操作结果 |
|                  | 借阅记录查询   | 支持按借书证ID、图书ISBN、借阅日期范围、借阅状态组合查询                     |
| 逾期管理模块     | 逾期检测       | 定时调用proc_check_overdue_books存储过程（如每天凌晨1点），批量更新逾期状态   |
|                  | 逾期提醒       | 查询v_overdue_books视图，通过短信/系统消息向借阅者推送逾期提醒               |
|                  | 罚款登记       | 手动补充/修改逾期罚款金额（特殊情况），关联借阅记录存档                     |
| 统计分析模块     | 借阅排行       | 按图书被借阅次数排序，展示TOP10热门图书                                     |
|                  | 借阅统计       | 按借阅者借阅次数排序，统计借阅活跃度；按单位统计借阅总量                     |
|                  | 馆藏统计       | 按出版社/图书类型（可扩展book表增加type字段）统计馆藏数量                   |

#### 3.  主要功能实现的程序段
##### （1） 核心功能：借书操作（Java + Spring Boot 实现）
```java
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Service;
import javax.annotation.Resource;
import java.util.Map;

// 1. Mapper接口（调用存储过程）
public interface BorrowRecordMapper {
    // 调用借书存储过程
    void callProcBorrowBook(@Param("p_borrower_id") String borrowerId,
                            @Param("p_book_isbn") String bookIsbn,
                            @Param("p_result") Map<String, Integer> resultMap);
}

// 2. Service层（业务逻辑封装）
@Service
public class BorrowService {
    @Resource
    private BorrowRecordMapper borrowRecordMapper;

    /**
     * 借书业务处理
     * @param borrowerId 借书证ID
     * @param bookIsbn 图书ISBN
     * @return 操作结果提示
     */
    public String borrowBook(String borrowerId, String bookIsbn) {
        Map<String, Integer> resultMap = new HashMap<>();
        // 调用存储过程
        borrowRecordMapper.callProcBorrowBook(borrowerId, bookIsbn, resultMap);
        Integer result = resultMap.get("p_result");
        // 结果映射
        switch (result) {
            case 1:
                return "借书成功！";
            case 2:
                return "借书失败：当前已借满8本图书，无法继续借阅！";
            case 3:
                return "借书失败：借书证无效或已注销！";
            case 4:
                return "借书失败：该图书已下架（删除）！";
            default:
                return "借书失败：未知错误！";
        }
    }
}

// 3. Controller层（接口暴露）
@RestController
@RequestMapping("/borrow")
public class BorrowController {
    @Resource
    private BorrowService borrowService;

    @PostMapping("/doBorrow")
    public String doBorrow(@RequestParam String borrowerId,
                           @RequestParam String bookIsbn) {
        return borrowService.borrowBook(borrowerId, bookIsbn);
    }
}
```

##### （2） 核心功能：还书操作（Python + Flask 实现）
```python
import pymysql
from flask import Flask, request, jsonify

app = Flask(__name__)

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'book_borrow_system',
    'charset': 'utf8mb4'
}

# 还书接口
@app.route('/return/doReturn', methods=['POST'])
def do_return_book():
    record_id = request.form.get('record_id', type=int)
    if not record_id:
        return jsonify({"code": -1, "msg": "请输入借阅记录ID！"})

    # 连接数据库调用存储过程
    conn = None
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # 调用存储过程
        cursor.callproc('proc_return_book', (record_id, 0))
        # 获取输出参数
        cursor.execute("SELECT @_proc_return_book_1")
        result = cursor.fetchone()[0]

        # 结果映射
        result_map = {
            1: {"code": 0, "msg": "还书成功！"},
            2: {"code": -1, "msg": "还书失败：借阅记录不存在！"},
            3: {"code": -1, "msg": "还书失败：该图书已归还！"},
            0: {"code": -1, "msg": "还书失败：未知错误！"}
        }
        return jsonify(result_map.get(result, {"code": -1, "msg": "还书失败：未知错误！"}))
    except Exception as e:
        return jsonify({"code": -1, "msg": f"还书失败：{str(e)}"})
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

##### （3） 前端核心：借书页面（HTML + jQuery 实现）
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>图书借阅 - 借书操作</title>
    <script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
    <style>
        .form-box { margin: 50px auto; width: 400px; padding: 20px; border: 1px solid #ccc; }
        .form-item { margin: 15px 0; }
        label { display: inline-block; width: 100px; }
        input { width: 250px; padding: 5px; }
        button { width: 100px; padding: 8px; background: #007bff; color: #fff; border: none; border-radius: 4px; }
        #msg { margin-top: 20px; color: red; text-align: center; }
    </style>
</head>
<body>
    <div class="form-box">
        <h2 style="text-align: center;">图书借书操作</h2>
        <div class="form-item">
            <label for="borrowerId">借书证ID：</label>
            <input type="text" id="borrowerId" placeholder="请输入借书证编号">
        </div>
        <div class="form-item">
            <label for="bookIsbn">图书ISBN：</label>
            <input type="text" id="bookIsbn" placeholder="请输入图书ISBN">
        </div>
        <div style="text-align: center;">
            <button id="borrowBtn">确认借书</button>
        </div>
        <div id="msg"></div>
    </div>

    <script>
        $(function() {
            // 借书按钮点击事件
            $("#borrowBtn").click(function() {
                var borrowerId = $("#borrowerId").val().trim();
                var bookIsbn = $("#bookIsbn").val().trim();

                if (!borrowerId || !bookIsbn) {
                    $("#msg").text("请完整填写借书证ID和图书ISBN！");
                    return;
                }

                // 提交后端接口
                $.post("/borrow/doBorrow", {
                    borrowerId: borrowerId,
                    bookIsbn: bookIsbn
                }, function(res) {
                    $("#msg").text(res);
                }).error(function() {
                    $("#msg").text("网络异常，请稍后重试！");
                });
            });
        });
    </script>
</body>
</html>
```

### （三）程序模块关系图
```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  图书管理模块   │      │  借阅者管理模块 │      │  统计分析模块   │
│  （基础数据）   │      │  （身份数据）   │      │  （数据汇总）   │
└─────────┬───────┘      └─────────┬───────┘      └─────────┬───────┘
          │                        │                        │
          ▼                        ▼                        ▲
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  借阅业务模块   │◄────►│  数据库（核心） │◄────►│  逾期管理模块   │
│  （核心业务）   │      │  表/视图/存储过程 │      │  （风险管控）   │
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

## 三、系统源程序
### （一） 完整数据库脚本（含表/视图/存储过程）
见本方案「一、系统分析报告 - （五）数据库表、视图、存储过程SQL定义」，可直接复制到Navicat/DBeaver中执行，完成数据库初始化。

### （二） 后端核心源程序
1.  Java + Spring Boot 核心代码：见本方案「二、程序设计报告 - （三）主要功能实现的程序段」
2.  Python + Flask 核心代码：见本方案「二、程序设计报告 - （三）主要功能实现的程序段」
3.  补充：MyBatis 映射文件（借书存储过程调用）
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.book.mapper.BorrowRecordMapper">
    <!-- 调用借书存储过程 -->
    <select id="callProcBorrowBook" statementType="CALLABLE">
        {call proc_borrow_book(
            #{p_borrower_id, mode=IN, jdbcType=VARCHAR},
            #{p_book_isbn, mode=IN, jdbcType=VARCHAR},
            #{p_result.p_result, mode=OUT, jdbcType=INTEGER}
        )}
    </select>
</mapper>
```

### （三） 前端核心源程序
1.  借书页面：见本方案「二、程序设计报告 - （三）主要功能实现的程序段」
2.  还书页面（简化版）：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>图书借阅 - 还书操作</title>
    <script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
    <style>
        .form-box { margin: 50px auto; width: 400px; padding: 20px; border: 1px solid #ccc; }
        .form-item { margin: 15px 0; }
        label { display: inline-block; width: 100px; }
        input { width: 250px; padding: 5px; }
        button { width: 100px; padding: 8px; background: #28a745; color: #fff; border: none; border-radius: 4px; }
        #msg { margin-top: 20px; color: red; text-align: center; }
    </style>
</head>
<body>
    <div class="form-box">
        <h2 style="text-align: center;">图书还书操作</h2>
        <div class="form-item">
            <label for="recordId">借阅记录ID：</label>
            <input type="number" id="recordId" placeholder="请输入借阅记录编号">
        </div>
        <div style="text-align: center;">
            <button id="returnBtn">确认还书</button>
        </div>
        <div id="msg"></div>
    </div>

    <script>
        $(function() {
            $("#returnBtn").click(function() {
                var recordId = $("#recordId").val().trim();
                if (!recordId) {
                    $("#msg").text("请输入借阅记录ID！");
                    return;
                }

                $.post("/return/doReturn", {
                    record_id: recordId
                }, function(res) {
                    $("#msg").text(res.msg);
                }).error(function() {
                    $("#msg").text("网络异常，请稍后重试！");
                });
            });
        });
    </script>
</body>
</html>
```

## 四、系统部署与使用说明
1.  数据库部署：执行完整数据库SQL脚本，初始化`book_borrow_system`数据库
2.  后端部署：
    - Java：打包为JAR包，通过`java -jar book-borrow.jar`启动（需配置数据库连接）
    - Python：直接运行Flask脚本，或通过Gunicorn部署为生产环境
3.  前端部署：将HTML文件放入Web服务器根目录（如Tomcat/webapps/ROOT），或通过后端框架静态资源映射访问
4.  定时任务：配置Linux crontab或Windows任务计划程序，定时调用`proc_check_overdue_books`存储过程（检测逾期）
5.  功能测试：先录入图书、借阅者数据，再进行借书、还书操作，验证业务约束（8本限额、30天期限）是否生效

### 总结
本图书借阅管理系统完整覆盖了用户要求的系统分析报告、程序设计报告及源程序，严格遵循“8本借阅限额”“30天借阅期限”的业务约束，采用MySQL数据库实现数据持久化，支持管理员与借阅者双角色操作，具备完整的图书借阅全流程管控能力，可直接部署使用或根据实际需求扩展功能（如图书分类、短信提醒等）。
