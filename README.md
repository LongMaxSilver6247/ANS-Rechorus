# ANS-Rechorus
## 基于[Rechorus](https://github.com/THUwangcy/ReChorus)框架的[ANS](https://arxiv.org/pdf/2308.05972)算法复现
### Getting Started

```bash
git clone https://github.com/LongMaxSilver6247/ANS-Rechorus.git
cd ANS-Rechorus
```

在**ANS-Rechorus**目录下创建虚拟环境

```bash
pip install -r requirements.txt
```
  
运行模型

```bash
cd src
python main.py --model_name ANS --dataset Grocery_and_Gourmet_Food
```

运行结果 \(与**BPRMF**以及**BUIR**算法进行对比, 运行参数相同 \(l2 = 1e-5, 其余均为默认\) \)
|Dataset                     |Method|HR@5   |NDCG@5 |HR@10  |NDCG@10|HR@20  |NDCG@20|HR@50  |NDCG@50|
|:---:                       |:---: |:---:  |:---:  |:---:  |:---:  |:---:  |:---:  |:---:  |:---:  |
|                            |ANS   |0.3828 |0.2633 |0.5107 |0.3048 |0.6203 |0.3325 |0.8220 |0.3723 |
|**Grocery_and_Gourmet_Food**|BPRMF |0.3795 |0.2601 |0.5050 |0.3008 |0.6170 |0.3291 |0.8226 |0.3696 |
|                            |BUIR  |0.3765 |0.2618 |0.4968 |0.3009 |0.6088 |0.3291 |0.8002 |0.3670 |
|                            |      |       |       |       |       |       |       |       |       |
|                            |ANS   |0.3817 |0.2590 |0.5564 |0.3152 |0.7436 |0.3627 |0.9562 |0.4056 |
|**MovieLens_1M**            |BPRMF |0.3587 |0.2414 |0.5216 |0.2935 |0.7022 |0.3391 |0.8984 |0.3786 |
|                            |BUIR  |0.3389 |0.2252 |0.4836 |0.2719 |0.6604 |0.3166 |0.8848 |0.3615 |
