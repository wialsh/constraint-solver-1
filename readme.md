

商旅问题(TSP)
---

##### 一、背景

**旅行商问题**（最短路径问题）（英语：**travelling salesman problem**, **TSP**）是这样一个问题：给定一系列城市和每对城市之间的距离，求解访问每一座城市一次并回到起始城市的最短回路。它是[组合优化](https://zh.wikipedia.org/wiki/组合优化)中的一个[NP困难](https://zh.wikipedia.org/wiki/NP困难)问题，在[运筹学](https://zh.wikipedia.org/wiki/运筹学)和[理论计算机科学](https://zh.wikipedia.org/wiki/理論計算機科學)中非常重要。

<img src="./data/images/440px-GLPK_solution_of_a_travelling_salesman_problem.svg.png" style="zoom:50%;" />

商旅问题在[组合优化](https://en.wikipedia.org/wiki/Combinatorial_optimization)中是 **NP-hard问题**；

<center> 
  <img src="./data/images/600px-P_np_np-complete_np-hard.svg.png" style="zoom:67%;" /> 
  <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d9;
    display: inline-block;
    color: #999;
    padding: 2px;">NP-completeness</div>
</center>

关于 *P、NP、NP-hard、NP-C问题*，做了如下总结；

- **P问题**：计算时间与计算复杂度/样本成倍数关系；

- **NP问题**：计算时间与复杂度/样本成指数关系（复杂度/样本量越大，计算量/时间越大）；
  或目前上，无法对其做一般性的归纳总结，如百度百科找出[最大质数问题](https://baike.baidu.com/item/NP完全问题/4934286?fr=aladdin)等等；

  > 本人了解的 **NP问题** 更多的是 *探讨计算时间与复杂度/样本成指数关系*；

- **NP-hard问题**：简单的示例是[子集集合问题](https://en.wikipedia.org/wiki/Subset_sum_problem)，是在 *N=NP* 条件下，*NP问题* 是 *NP-hard问题* 的子集；

- **NP完全问题**：满足 *NP问题* 和 *NP-hard 问题*，在特定条件下，众多 *NP问题* 可归纳为某一类 *NP问题*，解决了归纳的 *NP问题*，就解决了该集合内的所有 *NP问题*；



商旅问题（*travelling salesman problem, tsp*）在给定的城市列表情况下，寻找一条最短且有效的路径是巨大挑战的，因为：



<center> 
  <img src="./data/images/Bruteforce.gif" style="zoom:67%;" /> 
  <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d9;
    display: inline-block;
    color: #999;
    padding: 2px;">Travelling salesman problem</div>
</center>



- 10个候选城市且从同一个地方出发（有固定起点）有 $(10 - 1)! = 9 \times 8 \times ... \times 1 = 362880$ 种路径方案，若路径无顺序之分（a-b-c与c-b-a属同一种路径方案）则有 *362880/2 = 181440* 种路径方案；
- 假如候选城市达到15个，以有固定起点方案计算，路径方案高达870亿种，即使以无顺序方式计算，仍有435亿种；

若，候选城市15个，采用暴力方式搜索，如下图所示，即使每秒搜索100万次，也要超过12小时不间断的搜索，才能搜索到最佳路径，这个在算法上是“不可接受的事”，平常中基本上没有人会为等机器反馈结果，而等上12个小时，除非等人，在平常等待机器反馈结果，可忍受时间是3秒左右；

因此，需要一种搜索算法，在候选城市30个内，计算时间是秒级的，甚至可以牺牲最优路径，在规定的时间内，搜索到全局最优或接近于全局最优的解；

上文讲到 商旅问题在组合优化中是 **NP-hard问题**，而 [*蚁群算法（Ant Colony Algorithm）*](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms)是解决 *NP问题* 的一种选择方法；

关于商旅问题更详细的说明，请阅读

[优化 | 浅谈旅行商问题（TSP）的启发式算法](https://zhuanlan.zhihu.com/p/102709464)

[“旅行商问题”太棘手？用图神经网络寻找最优解](https://zhuanlan.zhihu.com/p/65943056)

##### 二、蚁群算法原理

**蚁群算法的原理和实现基于：[蚁群算法原理及其应用](http://www.ecsponline.com/yz/B676AB9119BF04182AD772E52B7C7451F000.pdf)**[^1]

<center> 
  <img src="./data/images/twinbridge_test.jpg" style="zoom:30%;" /> 
  <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d9;
    display: inline-block;
    color: #999;
    padding: 2px;">蚁群觅食的“双桥”实验</div>
</center>

*蚁群算法（Ant Colony Algorithm）* 最开始由意大利学者通过观察蚂蚁觅食，得到的仿生算法；

> 仿生算法：蚁群算法、遗传算法、粒子群算法等；

当一只蚂蚁寻找到食物，返回蚁巢呼叫群体，为什么**蚁群**从洞穴出发搬运食物，总能找到一条蚁巢与食物之间的最优路径？

因为在自然界中，蚂蚁会分泌一种化学刺激物 —— **信息素（pheromone）**；

蚂蚁在移动过程中，能够在其经过的路径上留下 *信息素*，且蚁群内能感知到这种物质的存在及其*强度*，并以此指导自己行走的方向，蚂蚁更倾向于 *信息素浓度高* 的方向移动；

在同等的时间内蚁群在搬运食物过程中，越短的路径上留下的 *信息素* 就越多多，则后续搬运中，最短路径的蚂蚁越来越多（如上图蚁群觅食的“双桥”实验）；

本文所说“最短路径”，并非一定是路程最短的路径，而是接近于全局最优的“最短路径”；

所以，在商旅问题（*tsp*）中，可以模拟蚂蚁在两两城市之间所留下信息素，来搜索最短路径，且最短路径是一个[有向图（Directed Acyclic Graph，DAG）](https://en.wikipedia.org/wiki/Directed_acyclic_graph)（或有向环图），如下图；

<center> 
  <img src="./data/images/500px-Shortest_path_with_direct_weights.svg.png" style="zoom:50%;" /> 
  <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d9;
    display: inline-block;
    color: #999;
    padding: 2px;">Shortest path problem</div>
</center>
我们先简单的计算一下蚂蚁是如何利用信息素找到最短路径的；

假设，蚁群从洞穴A点出发，到达食物F点，三条路径（A-C-E-D-F、A-B-D-F和A-B-C-E-D-F）均有相同数据量蚂蚁访问；
设：

- A-C-E-D-F路径长度为$L_1$、A-B-D-F路径长度为$L_2$和A-B-C-E-D-F路径长度为$L_3$；
- 三条路径访问蚂蚁数各为1，即 $n_{L_1}=n_{L_2}=n_{L_3}=1$；
- 初始化城市之间的信息素相同（如，初始化为1），那么每个节点被访问的概率是相同的（如，A点出发，B、C点被选择的概率均为0.5）；

那么，三条路径，三只蚂蚁访问后，每个节点留下的信息素如下：

- A-C有一只蚂蚁访问，留下信息素为$\dfrac{1}{L_1}\times n_{L_1}=\dfrac{1}{20} \times 1 = 0.05$

- A-B有两只蚂蚁访问，留下信息素为$\dfrac{1}{L_2}\times n_{L_2} +\dfrac{1}{L_3}\times n_{L_3} =\dfrac{1}{25} \times 1 + \dfrac{1}{27} \times 1 = 0.077$
- B-C有一只蚂蚁访问，留下信息素为$\dfrac{1}{L_3}\times n_{L_3}=\dfrac{1}{27} \times 1 = 0.037$
- B-D有一只蚂蚁访问，留下信息素为$\dfrac{1}{L_2}\times n_{L_2}=\dfrac{1}{25} \times 1 = 0.04$
- C-E有两只蚂蚁访问，留下信息素为$\dfrac{1}{L_1}\times n_{L_1} +\dfrac{1}{L_3}\times n_{L_3} =\dfrac{1}{20} \times 1 + \dfrac{1}{27} \times 1 = 0.087$
- E-D有两只蚂蚁访问，留下信息素为$\dfrac{1}{L_1}\times n_{L_1} +\dfrac{1}{L_3}\times n_{L_3} =\dfrac{1}{20} \times 1 + \dfrac{1}{27} \times 1 = 0.087$
- D-F有三只蚂蚁访问，留下信息素为$\dfrac{1}{L_1}\times n_{L_1} + \dfrac{1}{L_2}\times n_{L_2} + \dfrac{1}{L_3}\times n_{L_3} =\dfrac{1}{20} \times 1 + \dfrac{1}{25} \times 1 + \dfrac{1}{27} \times 1 = 0.127$

有了信息素，在下一个单位时间内，每一只蚂蚁访问的节点，可进行[赌轮盘选择](https://en.wikipedia.org/wiki/Fitness_proportionate_selection)，如从A点出发，B、C点被选择的概率为：$\dfrac{0.077}{0.05+0.077}=0.61$、$\dfrac{0.05}{0.05+0.077}=0.39$，以此类推；

我们发现一个问题，最优路径是A-C-E-D-F，而A点出发，B点被选择的概率远大于C点被选择的概率，因此计算信息素时就要加入两个城市之间的距离信息 $\eta$ 和一些因子，如$\alpha$（信息素加权因子） 和 $\beta$（距离加权因子），一般设置 $\beta > \alpha$ 来降低B点被选择的概率与C点被选择的概率的概率差；
若$\beta >> \alpha$，则蚁群搜索容易陷入局部最优值，比如A-C节点长度从2增加到5，A-C-E-D-F总长度为23，仍为最短路径，此时从A点到B点，不但距离短，而且蚂蚁数还多，那么搜索的最优路径就可能是A-B-C-E-D-F；
此时，可能我们还有一个疑问，只要经过同一条路径（如，A-C-E-D-F）的蚂蚁，分母都是相同的，因为它们除以的是该路径的总长度 $L_k$，是不是可以只除以局部路径的长度（如，A-C路径的长度 $d_{A-C}$），答案是可以的；
因此，按照信息素留下的方式不同，可以得到不同的蚁群模型，同时蚂蚁访问两两城市之间留下的信息素计算尤其重要，将直接影响算法的寻优能力，下文将列出信息素的计算公式，最后给出不同蚁群模型寻优能力的总结；

接下来就是更新信息素，更新方式和[凸优化](https://zhuanlan.zhihu.com/p/37108430)相同，采用学习率的方式更新，只不过蚁群算法的学习率（$\rho$）设的比较大，一般设置为0.5，A-C初始化的信息素为1，第一个单位时间内该路径被蚂蚁访问过并留下信息素为0.05，那么A-C的信息素为：$(1-0.5) * 1 + 0.05 = 0.55$，A-B的信息素为：$(1-0.5) * 1 + 0.077 = 0.577$，以此类推；

至此，蚁群算法做了简略的数值讲解，接下来将对蚁群算法做出详细定义和实现；

##### 三、定义

对此做如下定义；

**定义 TSP** ：在给定 *n* 个城市中，从指定起点（一般情况下商旅问题存在固定起点）城市出发，访问依次每个城市一次（访问不重复不遗漏）；

- 设 *C* 是 *n* 个城市的集合，如下；
  $C=\{c_1, c_2, ..., c_n\}$
- *城市 $c_i$* 与 *城市 $c_j$* 之间的距离记 $d_{ij}$，距离可用欧式距离（*Euclidean*）计算得到，如下；
  $d_{ij} = \sqrt{(x_i-x_j)^2 + (y_i - y_j)^2}$
- 信息素（pheromone）状态转移概率计算方式如下；
  $$\rho_{ij}^k(t) = \begin{cases}
   \dfrac{[\tau_{ij}(t)]^\alpha\cdot [\eta_{ik}(t)]^\beta}{\sum\limits_{s \subset allowed_k}[\tau_{is}(t)]^\alpha\cdot [\eta_{is}(t)]^\beta} & \text{ 若 } j \in allowed_k \\ 
   0 & \text{ 否则 }
  \end{cases}$$
  
  - $allowed_k$ 表示蚂蚁k下一步允许选择的城市；
  - $\alpha$ 为信息启发式因子（常量），表示轨迹的相对重要性；
  - $\beta$ 为期望启发式因子（常量），表示能见度的相对重要性；
  - $\eta_{ij}$ 启发函数（适应度评分函数），与距离成反比，一般性定义：$\eta_{ij} = \dfrac{1}{d_{ij}}$，$d_{ij}$表示两个城市之间的距离，因此 $[\eta_{ik}(t)]^\beta$ 是一个常量；
- $\tau$ 更新策略，如下；
  $$\begin{align*}
   \tau_{ij}(t+n) &= (1-\rho) \cdot \tau_{ij}(t) + \Delta\tau_{ij}(t) \\ 
   \Delta\tau_{ij}(t) &= \sum\limits_{k=1}^{m}\Delta\tau_{ij}^k(t)
  \end{align*}$$
  
  - $\rho$ 表示信息素挥发系数，$1-\rho$ 表示信息素残留因子，$\rho \subset [0, 1)$；
- $\Delta\tau_{ij}$ 表示第 *k* 只蚂蚁在本初循环留在路径 (i, j) 上的信息量，其中 $\Delta\tau_{ij}(0)=0$ （初始时刻）；
  
- $\Delta\tau_{ij}$ 更新策略，如下；

  - Ant-Cycle模型
    $$\Delta\tau_{ij}^k(t) = \begin{cases}
    \dfrac{Q}{L_k} & \text{ 若第k只蚂蚁在本次循环中经过(i,j) } \\ 
     0 & \text{ 否则 }
    \end{cases}$$

  - Ant-Quantity模型
    $$\Delta\tau_{ij}^k(t) = \begin{cases}
    \dfrac{Q}{d_{ij}} & \text{ 若第k只蚂蚁在 t 和 t+1 之间经过(i,j) } \\ 
     0 & \text{ 否则 }
    \end{cases}$$

  - Ant-Density模型

    $$\Delta\tau_{ij}^k(t) = \begin{cases}
    \dfrac{Q}{1} & \text{ 若第k只蚂蚁在 t 和 t+1 之间经过(i,j) } \\ 
     0 & \text{ 否则 }
    \end{cases}$$

    - $Q$ 信息强度（常量）；
    - $L_k$ 表示第 k 只蚂蚁在本次循环中所走路径的总长度
    - $d_{ij}$ 表示 *城市 i* 到 *城市 j* 的距离；

##### 四、实现

1、tsp数据源主要来自于：[TSPLIB](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/)；

2、Ant-Density模型由于分母是1，因此在实现中，忽略了该模型；

3、采用python的numpy实现；



##### 五、可视化结果

$\Delta\tau_{ij}$ 更新策略基于Ant-Cycle模型，结果如下：

| 城市数 | 路径图                                                       | 最优路径走势图                                               |
| ------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| a280   | <img src="./outputs/cycle/a280_best_route.png" style="zoom:14%;" /> | <img src="./outputs/cycle/a280_distance.png" style="zoom:14%;" /> |
| ch130  | <img src="./outputs/cycle/ch130_best_route.png" style="zoom:14%;" /> | <img src="./outputs/cycle/ch130_distance.png" style="zoom:14%;" /> |
| ch150  | <img src="./outputs/cycle/ch150_best_route.png" style="zoom:14%;" /> | <img src="./outputs/cycle/ch150_distance.png" style="zoom:14%;" /> |
| rd400  | <img src="./outputs/cycle/rd400_best_route.png" style="zoom:14%;" /> | <img src="./outputs/cycle/rd400_distance.png" style="zoom:14%;" /> |
| pr299  | <img src="./outputs/cycle/pr299_best_route.png" style="zoom:14%;" /> | <img src="./outputs/cycle/pr299_distance.png" style="zoom:14%;" /> |

$\Delta\tau_{ij}$ 更新策略基于Ant-Quantity模型，结果如下：

| 城市数 | 路径图                                                       | 最优路径走势图                                               |
| ------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| a280   | <img src="./outputs/quantity/a280_best_route.png" style="zoom:14%;" /> | <img src="./outputs/quantity/a280_distance.png" style="zoom:14%;" /> |
| ch130  | <img src="./outputs/quantity/ch130_best_route.png" style="zoom:14%;" /> | <img src="./outputs/quantity/ch130_distance.png" style="zoom:14%;" /> |
| ch150  | <img src="./outputs/quantity/ch150_best_route.png" style="zoom:14%;" /> | <img src="./outputs/quantity/ch150_distance.png" style="zoom:14%;" /> |
| rd400  | <img src="./outputs/quantity/rd400_best_route.png" style="zoom:14%;" /> | <img src="./outputs/quantity/rd400_distance.png" style="zoom:14%;" /> |
| pr299  | <img src="./outputs/quantity/pr299_best_route.png" style="zoom:14%;" /> | <img src="./outputs/quantity/pr299_distance.png" style="zoom:14%;" /> |

Ant-Cycle模型和Ant-Quantity模型耗时统计

| 城市数（去重） | Ant-Cycle模型耗时（单位：秒） | Ant-Quantity模型耗时（单位：秒） |
| -------------- | ----------------------------- | -------------------------------- |
| 14             | 0.169                         | 0.131                            |
| 16             | 0.163                         | 0.127                            |
| 17             | 0.185                         | 0.131                            |
| 22             | 0.169                         | 0.147                            |
| 27             | 0.322                         | 0.223                            |
| 29             | 0.26                          | 0.26                             |
| 42             | 0.546                         | 1.253                            |
| 48             | 0.846                         | 0.753                            |
| 49             | 0.616                         | 0.521                            |
| 51             | 1.068                         | 0.996                            |
| 52             | 0.746                         | 1.217                            |
| 53             | 1.082                         | 0.672                            |
| 57             | 1.227                         | 0.775                            |
| 70             | 1.939                         | 1.227                            |
| 76             | 2.423                         | 1.999                            |
| 96             | 2.774                         | 2.661                            |
| 99             | 5.789                         | 7.506                            |
| 100            | 4.417                         | 3.836                            |
| 101            | 7.747                         | 4.335                            |
| 105            | 6.553                         | 3.456                            |
| 107            | 8.121                         | 3.7                              |
| 120            | 10.86                         | 5.95                             |
| 124            | 6.029                         | 8.537                            |
| 127            | 6.488                         | 12.371                           |
| 130            | 6.928                         | 6.88                             |
| 136            | 7.716                         | 11.108                           |
| 137            | 6.795                         | 10.075                           |
| 144            | 11.532                        | 7.414                            |
| 150            | 13.865                        | 11.939                           |
| 152            | 11.445                        | 11.888                           |
| 159            | 22.105                        | 11.59                            |
| 195            | 16.684                        | 16.328                           |
| 198            | 42.924                        | 32.777                           |
| 200            | 32.316                        | 45.198                           |
| 202            | 30.745                        | 23.205                           |
| 225            | 46.248                        | 36.723                           |
| 226            | 54.407                        | 47.803                           |
| 229            | 32.636                        | 66.762                           |
| 262            | 74.31                         | 53.994                           |
| 264            | 43.133                        | 39.101                           |
| 280            | 94.898                        | 120.658                          |
| 299            | 108.203                       | 60.459                           |
| 318            | 152.503                       | 114.811                          |
| 400            | 311.058                       | 224.999                          |
| 417            | 238.785                       | 310.78                           |
| 431            | 224.9                         | 238.356                          |
| 439            | 427.962                       | 392.967                          |
| 442            | 400.314                       | 323.85                           |
| 493            | 885.625                       | 464.68                           |



Ant-Cycle模型和Ant-Quantity模型路径长度统计

| 城市数           | Ant-Cycle模型 | Ant-Quantity模型 |
| ---------------- | ------------- | ---------------- |
| a280             | 2870.8        | 2916.2           |
| att48            | 34405.3       | 34901.9          |
| bayg29           | 8926.1        | 8914.5           |
| bays29           | 8830.1        | 8968.7           |
| berlin52         | 7631.9        | 7573.1           |
| bier127          | 118559.2      | 119056.5         |
| burma14          | 27.2          | 27.6             |
| ch130            | 6448.6        | 6429.2           |
| ch150            | 6793.6        | 6785.4           |
| circuit_board280 | 2854.1        | 2893.8           |
| d198             | 14017.3       | 13943.0          |
| d493             | 35589.7       | 36363.7          |
| dantzig42        | 657.0         | 686.5            |
| eil101           | 701.9         | 691.1            |
| eil51            | 437.5         | 443.8            |
| eil76            | 549.3         | 559.9            |
| fl417            | 12896.2       | 12729.0          |
| gil262           | 2559.9        | 2544.2           |
| gr120            | 1757.6        | 1759.8           |
| gr137            | 758.4         | 769.1            |
| gr202            | 477.2         | 501.2            |
| gr229            | 1731.3        | 1701.8           |
| gr431            | 2127.7        | 2128.4           |
| gr96             | 528.6         | 518.4            |
| kroA100          | 22688.9       | 22913.0          |
| kroA150          | 29051.7       | 29045.0          |
| kroA200          | 31110.8       | 31447.3          |
| kroB100          | 22490.1       | 23133.6          |
| kroB150          | 28138.4       | 28080.5          |
| kroB200          | 32185.0       | 32475.7          |
| kroC100          | 21552.5       | 21250.5          |
| kroD100          | 22505.8       | 22594.4          |
| kroE100          | 23372.3       | 23728.1          |
| lin105           | 15071.5       | 15122.3          |
| lin318           | 95059.0       | 94520.1          |
| pcb442           | 59020.5       | 58710.4          |
| pr107            | 39059.3       | 38745.6          |
| pr124            | 61598.9       | 62496.0          |
| pr136            | 106640.3      | 109443.4         |
| pr144            | 59321.7       | 59033.4          |
| pr152            | 67871.6       | 67800.8          |
| pr226            | 80226.7       | 81795.0          |
| pr264            | 49895.7       | 48859.2          |
| pr299            | 53071.6       | 53673.1          |
| pr439            | 116797.0      | 115405.9         |
| pr76             | 115420.6      | 115456.5         |
| rat195           | 2446.2        | 2493.7           |
| rat99            | 1284.7        | 1293.8           |
| rd100            | 8567.7        | 8492.5           |
| rd400            | 17218.0       | 17141.8          |
| st70             | 704.0         | 704.7            |
| ts225            | 132417.8      | 131921.0         |
| tsp225           | 4186.2        | 4157.7           |
| u159             | 44469.2       | 44433.3          |
| ulysses16.tsp    | 55.1          | 57.9             |
| ulysses22.tsp    | 57.4          | 57.2             |



##### 六、总结

1. 在调参上，基本参考 蚁群算法原理及其应用[^1]；
2. 设置了早熟停止迭代，因此可能出现城市数与耗时不成正比的情况；
3. Ant-Cycle模型耗时比Ant-Quantity模型耗时短，但Ant-Quantity模型更容易陷入局部最优值，所以，更容易出发早熟停止迭代机制（本文未提供结果对比说明，感兴趣的同学，可以利用提供的源码自行验证）；
   Ant-Cycle模型信息素的更新是以整条路径 $L_k$ 为基础，路径中的某段路长短不影响其路径的信息素计算；
   Ant-Quantity模型信息素的更新是以路径中的某段路 $d_{ij}$ 为基础，整条路径长短不影响其路径的信息素计算；
   Ant-Cycle模型处理“病态问题”[^2]（P113）比Ant-Quantity模型优，因为Ant-Cycle模型信息素的计算是不受路径中的某段路长短的影响，但现实中很少有这种奇怪性质的“病态问题”；
4. 算法实现是比较粗糙的，如最后评价函数应该是：模型寻优次数+寻优迭代步数+运行时间，因此关于细节方面，感兴趣的同学可详读下文提供的参考文献；

##### 七、优化方向

1. 蚁群算法在性能和局部寻优能力，远胜于遗传算法，上文提到，寻优30个候选城市耗时要求是3秒（同事使用Scala10个线程），而本人利用python实现的蚁群算法寻优90个候选城市耗时也不到3秒，但工业应用上使用遗传算法远高于蚁群算法（本人了解的），主要是因为遗传算法拥有超强的扩展性灵和活性强，使得其应用非常广泛：函数优化、组合优化、生产调度、自动控制、机器人学、图像处理、人工生命、遗传编程、机器学习等，就其路径规划根据染色体交叉方式不同得到不同启发式遗传算法：单点交叉、双点交叉、均匀交叉、匹配交叉、顺序交叉、循环交叉、贪婪式交叉、旋转交叉、混合蛙跳[^4]、DPX[^5]等等，数不胜数；
   其中贪婪式交叉、旋转交叉、混合蛙跳、DPX本人均实现过，性能远不及蚁群算法，寻优能力与蚁群算法略差，而且遗传算法组合能力是非常强的，比较容易跳出局部最优值，因此个人认为寻优能力上启发式遗传算法略胜一筹（仍在研究中），但启发式遗传算法需要有非常强和广的相关知识，不易实现，这可能就是本人实现启发式遗传算法不如蚁群算法优的原因（ps，在路径规划专项任务下，还是蚁群算法简单好用，易于实现）；
2. 蚁群算法容易陷于局部最优值（下图），A、B、C均为局部最优值，假设B点为全局最优；
   若蚁群算法根据信息素从O点到达A点时，可能是无法跳出局部最优，因为蚁群在t时刻游走的路线受t-1时刻信息素的限制，而t-1时刻游走的线路受t-2时刻信息素的限制等等，因此t时刻要想跳出局部最优值A点，很难通过调参解决，这也可以解析每一次蚁群算法跑出来的结果有差异，且根据路径图做前后对比的话，每次结果路径可能有明显差异，遗传算法也有类似情况（但比较稳定）；
   第5点提到，启发式遗传算法比较容易跳出局部最优值，是因为启发式遗传算法中的适应度越高的染色体交叉属于局部搜索（即在A区域内搜索），适应度一般的染色体可能在[鞍点](https://en.wikipedia.org/wiki/Saddle_point)或C点，其交叉可能就是全局搜索，关键就是如何设置适应度高的染色体交叉和适应度较高、一般染色体交叉，太过于随机，则会降低收敛速度，还有一个关键点就是在染色体交叉后如何保留种群的多样性，详看请看参考文献[^2]；
   启发式，根据优化目标调整算法或多算法组合，蚁群算法根据优化目标调整算法可能性不大，不可能把蚂蚁调整为会飞，那就是粒子群算法了，多算法组合是蚁群算法的一个优化方向，如[模拟退火](https://en.wikipedia.org/wiki/Simulated_annealing)+蚁群算法、[爬山算法](https://en.wikipedia.org/wiki/Hill_climbing)+蚁群算法，模拟退火和爬山算法跳出局部最优值的好帮手，而且计算快，算法组合后，性能受影响小，笔者用类似的方法解决了背包问题+商旅问题； 


<center> 
  <img src="./data/images/nonconvex.png" style="zoom:67%;" /> 
  <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d9;
    display: inline-block;
    color: #999;
    padding: 2px;">https://waveopt-lab.uic.edu/guaranteed-non-convex-optimization-for-signal-processing/</div>
</center>

参考文献：

[^1]: 段海滨. 蚁群算法原理及其应用[M]. 北京: 科学出版社, 2005.

[^2]: 运筹学, 树栋, 遗传学. 遗传算法原理及应用[M]. 国防工业出版社, 1999.

[^3]:谢建, 朱建军. 等式约束对病态问题的影响及约束正则化方法[J]. 武汉大学学报● 信息科学版, 2015, 40(10): 1344-1348.
[^4]:罗雪晖, 杨烨, 李霞. 改进混合蛙跳算法求解旅行商问题[J]. 通信学报, 2009, 30(7): 130-135.
[^5]: New Genetic Local Search Operators for the Traveling Salesman Problem
[^6]:一种改进的遗传算法求解旅行商问题