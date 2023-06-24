from flask import Flask, render_template, request, send_file
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
import numpy as np
from textblob import TextBlob
import networkx as nx

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('upload.html')
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file_path = 'path/to/save/' + file.filename
        file.save(file_path)
        result2 = leaderboard(file_path)
        return render_template('results.html', result2=result2)
def leaderboard(file_path):
    data = pd.read_csv(file_path)
    data = data.astype(str)
    data[["Posted", "Replied"]] = data[["Posted", "Replied"]].astype(int)
    polarity = []
    sentiment = []
    sentiment = [0 for i in range(6)]
    TextBlob(data['Text'][0]).sentiment.polarity
    for i in range(data.shape[0]):
        polarity.append(TextBlob(data['Text'][i]).sentiment.polarity)
        sentiment[data['Posted'][i]-1] += polarity[i]
    import matplotlib.colors as mcolors
    G = nx.DiGraph()
    with open(file_path, 'r') as file:
        next(file) 
        for line in file:
            to_node, from_node = line.strip().split(',')[:2]
            G.add_edge(from_node, to_node)
    num_nodes = G.number_of_nodes()
    degree_centrality = nx.degree_centrality(G)
    edge_freq = {}
    for edge in G.edges:
        if edge in edge_freq:
            edge_freq[edge] += 1
        else:
            edge_freq[edge] = 1
    import math
    points = []
    count = 0
    for node in G.nodes:
        points.append(degree_centrality[node]*1000)
        points[count] += sentiment[count]*1000
        points[count] = math.trunc(points[count])
        count += 1
    return points
def network(file_path):
    data = pd.read_csv(file_path)
    data = data.astype(str)
    data[["Posted", "Replied"]] = data[["Posted", "Replied"]].astype(int)
    polarity = []
    sentiment = []
    sentiment = [0 for i in range(6)]
    TextBlob(data['Text'][0]).sentiment.polarity
    for i in range(data.shape[0]):
        polarity.append(TextBlob(data['Text'][i]).sentiment.polarity)
        sentiment[data['Posted'][i]-1] += polarity[i]
    import matplotlib.colors as mcolors
    G = nx.DiGraph()
    with open(file_path, 'r') as file:
        next(file) 
        for line in file:
            to_node, from_node = line.strip().split(',')[:2]
            G.add_edge(from_node, to_node)
    num_nodes = G.number_of_nodes()
    edge_freq = {}
    for edge in G.edges:
        if edge in edge_freq:
            edge_freq[edge] += 1
        else:
            edge_freq[edge] = 1
    degree_centrality = nx.degree_centrality(G)
    cmap = mcolors.LinearSegmentedColormap.from_list('CustomColors', ['red', 'green'])
    norm = mcolors.Normalize(vmin=-1, vmax=1)
    node_colors = [cmap(norm(value)) for value in sentiment]
    layout = nx.circular_layout(G)
    line_colors = [edge_freq[edge] for edge in G.edges]
    node_sizes = [degree_centrality[node] * 1000 for node in G.nodes]
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos=layout, with_labels=True, node_size=node_sizes, node_color=node_colors, edge_color='gray', width=0.5, arrows=True)
    plt.show()
    return plt.gcf()
if __name__ == '__main__':
    app.run(debug=True)
