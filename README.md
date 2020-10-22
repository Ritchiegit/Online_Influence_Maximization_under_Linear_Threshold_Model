# Online Inﬂuence Maximization under Linear  Threshold Model

This repository is the official implementation of **Online Inﬂuence Maximization under Linear Threshold Model**. 



## Requirements

To install requirements:

### step 1

```setup
conda install --yes --file requirements.txt
```

### step 2 (If you want to generate the ER graph.)

```setup
pip install python-igraph=0.8.0
```



## Run Our Algorithm

To run the algorithm in the paper, run this command:

```Run
python Main.py --is_bipartite --seed_size 5 --iterationTimes 22000 --save_address <path_to_save> --G_address <path_to_graph> --weight_address <path_to_weight>
```

You can reproduce the four examples in the paper.

```Run
python Main.py --seed_size 3 --iterationTimes 11000 --save_address SimulationResults/gaussian_9_ER --G_address Datasets/ER_node9_p_0.2.G --weight_address Datasets/ER_node9_p_0.2EWTrue.dic
```

```Run
python Main.py --seed_size 3 --iterationTimes 6000 --save_address SimulationResults/gaussian_12_ER --G_address Datasets//ER_node12_p_0.2.G --weight_address Datasets/ER_node12_p_0.2EWTrue.dic
```

```Run
python Main.py --is_bipartite --seed_size 3 --iterationTimes 30000 --save_address SimulationResults/BinarySelect2_2010_2d --G_address Datasets//DIY_Binary_RandomSelect2_20_10.G --weight_address Datasets/DIY_Binary_RandomSelect2_20_10EWTrue.dic
```

```Run
python Main.py --is_bipartite --seed_size 5 --iterationTimes 22000 --save_address SimulationResults/BinarySelect2_100100_2d --G_address Datasets//DIY_Binary_RandomSelect2_100_100.G --weight_address Datasets/DIY_Binary_RandomSelect2_100_100EWTrue.dic
```



## Results

To evaluate my model, we draw the average reward of algs.

<img src="\SimulationResults\BinarySelect2_2010_2d_paper\Reward\Average2WithErrorBar.png" style="zoom:50%;" /> <img src="\SimulationResults\BinarySelect2_100100_2d_paper\Reward\Average2WithErrorBar.png" style="zoom:50%;" />

<img src="\SimulationResults\gaussian_9_ER_paper\Reward\Average2WithErrorBar.png" style="zoom:50%;" /> <img src="\SimulationResults\gaussian_12_ER_paper\Reward\Average2WithErrorBar.png" style="zoom:50%;" />



