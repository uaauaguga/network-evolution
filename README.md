# network-evolution
Simulation to illustrate how does gene duplication leads to the scale-free property of biological network

- Random network: node i and j are connected with probability p, and degrees should follows a binomial distribution of degrees
- Scale free network: distribution of degree follows power law distribution: P(k)~k^(-γ)
  - The smaller the value of γ, the more important the role of the hubs is in the network.
  - 2<γ<3: there is a hierarchy of hubs
  - γ>3: behaves like a random one
- Refers to 2002,[Evolving protein interaction networks through gene duplication](https://www.sciencedirect.com/science/article/pii/S0022519303000286?via%3Dihub)
  - Start from 100 randomly connected nodes
  - Simulate duplicate events for 1000 times 
    - One node of the graph is selected at random and duplicated
    - Edges of the duplicated is removed with probability **p(delete)**
    - Add new edge (not previously present) to duplicated node with probability **p(add)**
- Run simulation


```bash
bash scripts/run.sh > results.txt
 cat results.txt | awk '(NR==1)||($5>2&&$5<3&&$6<-0.9){print}' > results-scale-free.txt
 scripts/simulate.py -dp 0.9 -ap 0.001 -cp 0.01 -n 200 --figure figures/dp-0.9-ap-0.001-cp-0.01-n-200.png
```
