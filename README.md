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

运行结果 \(与**BPRMF**以及**BUIR**算法进行对比, 运行参数相同 \(若有同种参数\) \)
|Dataset                     |Method|HR@5   |NDCG@5 |HR@10  |NDCG@10|HR@20  |NDCG@20|HR@50  |NDCG@50|
|:---:                       |:---: |:---:  |:---:  |:---:  |:---:  |:---:  |:---:  |:---:  |:---:  |
|                            |ANS   |0.3171 |0.2180 |0.4209 |0.2516 |0.5314 |0.2795 |0.7408 |0.3206 |
|**Grocery_and_Gourmet_Food**|BPRMF |0.3191 |0.2195 |0.4222 |0.2529 |0.5304 |0.2801 |0.7412 |0.3216 |
|                            |BUIR  |0.3635 |0.2453 |0.4876 |0.2856 |0.6058 |0.3154 |0.8056 |0.3547 |
|                            |      |       |       |       |       |       |       |       |       |
|                            |ANS   |0.3987 |0.2659 |0.5658 |0.3195 |0.7599 |0.3683 |0.9530 |0.4073 |
|**MovieLens_1M**            |BPRMF |0.3859 |0.2625 |0.5536 |0.3162 |0.7526 |0.3665 |0.9489 |0.4060 |
|                            |BUIR  |0.3132 |0.2117 |0.4690 |0.2619 |0.6660 |0.3118 |0.8981 |0.3581 |
