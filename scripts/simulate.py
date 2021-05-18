#!/usr/bin/env python
import numpy as np
import argparse
import networkx as nx
from scipy.stats import bernoulli 
from matplotlib import pyplot as plt
from scipy.stats import linregress


def plot_degree_hist(G,path):
    fig,axes = plt.subplots(1,2,figsize=(8,3))
    degrees = np.array(list(dict(G.degree()).values()))
    axes[0].hist(degrees,bins=np.arange(degrees.max()+1))
    axes[0].set_xlabel("$degrees$",fontsize=12)
    axes[0].set_ylabel("$frequency$",fontsize=12)
    deg,freq = np.unique(degrees,return_counts=True)
    freq = freq[deg>0]
    deg = deg[deg>0]
    probs = freq/freq.sum()
    axes[1].scatter(np.log(deg), np.log(probs))
    axes[1].set_xlabel("$ln(degree)$",fontsize=12)
    axes[1].set_ylabel("$ln(frequency)$",fontsize=12)
    plt.savefig(path,bbox_inches="tight")


def simulate(p_connected = 0.01,p_deletion = 0.9,p_addition = 0.001,n_init_nodes = 100,iteration=1000):
    adj_matrix = bernoulli(p_connected).rvs((n_init_nodes,n_init_nodes))
    adj_matrix = adj_matrix*(1-np.eye(n_init_nodes))
    G = nx.convert_matrix.from_numpy_matrix(adj_matrix)
    for t in range(iteration):
        # n: current index of node to add
        n = G.number_of_nodes()
        # Random select a node to duplicate it
        node_to_duplicate = np.random.randint(n)
        # Copy edges of duplicated node
        links = np.array(list(G[node_to_duplicate]))
        G.add_node(n)
        for link in links:
            G.add_edge(n, link)
            
        # Delete edges of newly added node with probability p_deletion
        deleted_links = bernoulli(p_deletion).rvs(len(links))
        deleted_links = links[np.where(deleted_links>0)[0]]
        for link in deleted_links:
            G.remove_edge(n,link)
            
        # Add edges to newly added node with probability p_addition
        no_links = np.setdiff1d(np.arange(n),links)
        added_links = bernoulli(p_addition).rvs(len(no_links))
        added_links = no_links[np.where(added_links>0)[0]]
        for link in added_links:
            G.add_edge(n, link)
    return G


def get_parameter(G):
    degrees = np.array(list(dict(G.degree()).values()))
    deg,freq = np.unique(degrees,return_counts=True)
    freq = freq[deg>0]
    deg = deg[deg>0]
    probs = freq/freq.sum()
    slope, intercept, r, p, se = linregress(np.log(deg), np.log(probs))
    return -slope, r


def main():
    parser = argparse.ArgumentParser(description="Simulate protein-protein interaction network under different parameter setting")
    parser.add_argument("--connect-probability",'-cp',type=float,default=0.01,help="Probability that two node is connected in the inital network")
    parser.add_argument("--delete-probability","-dp",type=float,default=0.9,help="Probability that a edge of the duplicated gene is lost")
    parser.add_argument("--add-probability","-ap",type=float,default=0.001,help="Probability that a new edge is genrated for the duplicated gene")
    parser.add_argument("--nodes-number","-n",type=int,default=100,help="Number of nodes in the inital network")
    parser.add_argument("--duplication-events","-e",type=int,default=1000,help="Number of duplication events")
    parser.add_argument("--figure",help="Where to save figure")
    args = parser.parse_args()
    G = simulate(p_connected =args.connect_probability,
                 p_deletion = args.delete_probability,
                 p_addition = args.add_probability,
                 n_init_nodes = args.nodes_number,
                 iteration= args.duplication_events)
    
    slope, r = get_parameter(G)
    slope = np.round(slope,3)
    r = np.round(r,3)
    print(f"{args.connect_probability}\t{args.delete_probability}\t{args.add_probability}\t{slope}\t{r}")
    if args.figure is not None:
        plot_degree_hist(G,args.figure)



if __name__ == "__main__":
    main()