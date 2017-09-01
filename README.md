---
title:   batman 测试框架用户使用手册1.0
tags: 接口测试,自动化测试,python
---


##  一 测试框架背景及目的
  

 - 传统的软件测试大多是白盒测试,单元测试和接口测试尤为明显,测试人员都是根据开发人员开发出一个功能,然后对任何合理的输入和不合理的输入	,进行鉴别和响应,最后对整个模块的测试结果进行分析.编写测试报告

- batman测试框架是针对公司需求基于python开发的自动化测试框架.主要功能是测试人员只针对某一个功能通过简单输入测试数据和期待数据等操作,然后系统会自动生成一份测试报告.这样把测试人员从繁琐的测试工作中解脱出来.



----------
##  二 框架的概念集合
 - 测试工程(project): 进行测试工作前要先创建一个测试工程,新建的测试工程会有框架的基本的配置和测试步骤模板.工程是根目录,测试集和测试步骤都在工程里创建

 -  测试集(collection):测试集可以包含测试步骤和测试子集，测试集类似文件夹，是一个自包含的结构测试集是涵盖整个工程.首先测试工程就是一个特殊测试集.普通测试集有特殊的命名 命名由前缀 ,索引 ,后缀组成.
	* 前缀(prefix) : 是定义测试集的类型
    * 索引号(index):是测试集创建的先后顺序的编号
    *  后缀(suffix):是代表测试集的简单说明
    
 - 测试步骤(step): 测试步骤一共有三种,普通的测试步骤,setup测试步骤,teardown测试步骤.命名前缀来判定测试步骤的类或者模板类型,索引号代表测试号,后缀表示测试步骤的说明.创建测试步骤一种是可以自己创建,自定义模板.另一种方式根据模板创建
	*  普通测试步骤 : 里面主要是由测试类组成.针对某一功能接口测试,例如 登录实体类,要进行鉴别和响应正确和错误的输入其中还有几类特殊的测试步骤
	*  setup测试步骤 : 这个步骤是每个测试集都有的测试步骤,直属文档路径最近的测试集.,对刚开始执行的测试集具有初始化的功能
	*  teardown测试步骤: 这个步骤是每个测试集都有的测试步骤,直属文档路径最近的测试集.,对执行完的测试集具有销毁的功能
 - 测试步骤模板 (template):  创建测试步骤可以根据模式序列号,创建模板
   *  001-通用测试模板: test一个基本测试类 例如测试登录接口
 
    * 002-HTTP测试模板模板: 包括HTTP录制过程的模板
    *  003-JSONRPC测试模板: 包括JSONRPC的录制模板

## 三 实例操作
 - 框架安装
    * 电脑配置要求:  64bit系统,linux或者windows.能够运行python程序
    * python的安装教程 http://jingyan.baidu.com/article/eb9f7b6da950c4869364e8f5.html python版本选择3.6.0以上 python安装完成后,需要新建虚拟环境命名为batman http://www.cnblogs.com/Finley/p/5925928.html
 
     *  执行 requirment.txt文件 安装测试框架 
-   create指令
	*  进入测试框架, 创建一个工程   语句 " batman create project " 然后一直按提示创建配置文件,以便适合自己的项目.
	例如" batman create-project"
		 - 请输入项目名称:  hello
		 - 请输入项目配置 "project.name" 的值，缺省为 [本人很懒项目]:first test
		 - 请输入项目配置 "http.url" 的值，缺省为 [http://www.pupuwang.com/]: 默认回车
		- 请输入项目配置 "project.description" 的值，缺省为 [如果没有写描述, 说明本人很懒]: first test
		- 请输入项目配置 "http.timeout" 的值，缺省为 [30]: ,默认回车
		- 请输入项目配置 "context.id" 的值，缺省为 [empty]: 默认回车
后来系统提示生成一个hello的project项目
	* 创建项目完成后,在项目路径下创建测试集 输入"batman create collection" 按提示创建适合自己的collection
	 	 -  请输入测试集类型：[suite, case, exp], 缺省值为 [suite]: suite   
		 -  请输入测试集的编号, -1 代表自动编号（缺省值：-1） [-1]: 
		- 请输入测试集的说明 []:firstcollection
生成的测试集的按前缀+索引号+后缀来生成的测试集文件名


	* 创建步骤完成后 输入"batman create step" 按提示创建需要的step
		 - 请输入模板的编号，缺省值为 [-1]: 001
		- 请输入测试步骤的类型：('step', 'setup', 'teardown'), 缺省值为 [step]: setup
		- 请输入测试步骤的编号, -1 代表自动编号，缺省值为 [-1]: 100
		 - 请输入测试步骤的说明 []: firststep
根据这样操作创建了一个完成的测试步骤
    *  每个新的测试集都要新建属于自己的steup测试步骤和teardown测试步骤 .所以创建测试集的时候需要按照操作创建自己的setup测试步骤和teardown测试步骤.
    
   * run指令
	  *  run指令是运行测试步骤或者测试集的指令 指令 "batman run suite-001-firststep.py" 然后会出来运行结果或者运行测试集 "batman run "
	 
* record 
  *  record指令是记录测试步骤从客户端到服务器的时间和过程的指令 "batman record suite-001-firststep.py",比如HTTP传输时间,JSONRPC传输过程的报告
* dump
  *  dump指令是打印目录结构的指令,指令是"batman dump hello".打印出目录结构使人们可以更加清晰看清楚工程的目录结构
*  server指令
	 * server指令是 建立本地服务器，用于查看测试文档 指令"batman server"
*   clean  
    *  clean 清除文件指令 clean指令是用来清除不需要的文件 指令格式"batman clean suite-001-firststep"
  * find  
    * find 查找包含指定接口的测试集,指令格式
    "batman find login"查找跟登录接口所有想的测试集
*  benchmark  
	  *   benchmark  压力测试,是成百上千次对某一接口进行测试,然后测试返回结果

## 四、 测试报告


* 通过运行测试可以生存测试报告，测试报告中包含：
  *  每个测试案例的执行时间，及测试案例中每次 JSONRPC 交互执行时间
  * 每个测试集、测试案例的运行情况（成功、失败，失败原因）
  *  统计 测试过程中 的接口覆盖率
  *  统计 测试过程中 的接口调用次数

* 测试集：用户端商品测试集


	* case001-购买商品
        - setup/001-用户登录.py             2s
		- case001-购买商品/001-购买商品.py   5s
		- case001-购买商品/002-评价商品.py   3.2s
		- teardown/001-用户注销.py          2s结果：成功，用时：3.36s

	 * case001-退回商品：
		- ...
		- ...
		- ...
		- 结果：失败
		- 失败步骤：case002-退回商品/002-退回商品.py
		- 失败原因：
	 assertEquals(RESP['result']['code'], 0, "成功退回商品时应该返回 0")



*  本次测试用时最多的10个接口有：
   * product_buy:     30s
   *  user_login:      18s
   * user_logout:     3s
...

 * 本次测试接口覆盖如下：

   - 接口             次数  平均调用时间    
   -  user_login      7次   3.2s
   -  user_logout     7次   1.2s
   -  product_buy     3次   0.8s
   -  product_rate    2次   0.3s
....

* 未被覆盖到的接口有：
  user_profile, user_change_avatar ...


 本次测试 10个成功，1 个失败，失败案例有：
     case002-退回商品/002-退回商品.py
	     

