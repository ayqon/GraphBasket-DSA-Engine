# GraphBasket-DSA-Engine
## High-Performance Graph Data Structures & Apriori Association Rule Mining

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-emerald.svg)](https://graphbasket-dsa-engine.onrender.com)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Test Suite](https://img.shields.io/badge/pytest-23%2F23%20passed-emerald.svg)](test_market_basket.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-slate.svg)](LICENSE)
[![Dataset](https://img.shields.io/badge/Dataset-14%2C963%20Baskets-blue.svg)](data/supermarket_transactions.csv)

> **Live Interactive Platform**: [https://graphbasket-dsa-engine.onrender.com](https://graphbasket-dsa-engine.onrender.com)

An end-to-end, high-performance Market Basket Analysis and Real-Time Product Recommendation System. The platform couples custom graph data structures (Adjacency List representation) with the Apriori association rule mining algorithm to discover multi-item affinities, cross-selling opportunities, and bundle synergy metrics across 14,963 customer shopping transactions.

---

## Dataset Access & Information

The benchmark dataset consists of real-world transactional purchase records from a retail supermarket chain:
* **Online Repository File**: [`data/supermarket_transactions.csv`](data/supermarket_transactions.csv)
* **Web UI Direct Download**: Accessible via the "Download Dataset (CSV)" button in the live dashboard header.
* **Volume**: 14,963 unique customer shopping baskets across 38,765 item purchase events.
* **Catalog**: 167 distinct product stock-keeping units (SKUs) spanning 8 categories (Dairy, Fresh Produce, Bakery, Beverages, Meat, Snacks, Household, Pantry).
* **Format**:
  * `Member_number`: Customer identifier
  * `Date`: Transaction timestamp (DD-MM-YYYY)
  * `itemDescription`: Standardized item name

---

## Key Highlights

* **Custom Graph Architecture (O(V + E))**: Undirected weighted graph representing item co-purchase frequency. Eliminates the memory overhead of dense adjacency matrices, achieving a **55.2% memory reduction** on retail transaction sparsity.
* **Apriori Association Rule Mining**: Generates support, confidence, lift, and leverage metrics across 167 unique supermarket products with level-wise downward-closure candidate pruning.
* **Real-Time Recommendation Engine**: Multi-item graph neighborhood traversal calculating aggregated synergy lift for dynamic shopping cart bundles.
* **Interactive Standalone Web Platform**: Zero-dependency frontend providing an interactive Force-Directed Graph Visualizer, Rule Filter Engine, Shopping Cart Simulator, and DSA Complexity Benchmarks.
* **Test-Driven Architecture**: 23/23 passing automated unit tests covering data parsing, graph mutations, edge traversals, and rule evaluation.

---

## Architectural & Algorithmic Complexity

| Operation | Data Structure | Time Complexity | Space Complexity | Practical Note |
|:---|:---|:---:|:---:|:---|
| **Vertex Insertion** | `ProductGraph` (Hash Map) | O(1) avg | O(1) | Constant-time product catalog indexing |
| **Edge Insertion / Update** | `ProductGraph` (Adjacency List) | O(1) | O(1) | Efficient pointer linkage for co-purchases |
| **Neighbor Traversal (Affinity)** | `ProductGraph` | O(deg(v)) | O(1) aux | Optimal for sparse graphs (55.2% sparsity) |
| **Basket Membership Check** | `Transaction` (Hash Set) | O(1) avg | O(k) | Constant-time verification of candidate items |
| **Association Rule Generation** | `AprioriAnalyzer` | O(2^k * |T|) worst | O(|L_k|) | Bounded by average basket size (k_avg = 2.54) |

---

## Data Structure Memory Comparison: Retail Graph Sparsity

On retail purchase graphs with |V| = 167 vertices and |E| = 6,260 undirected co-occurrence edges (sparsity = 55.2%):

```
Adjacency List Entries = |V| + 2|E| = 167 + 2(6,260) = 12,687 pointers (approx 99.1 KB)
Adjacency Matrix Entries = |V|^2 = 167^2 = 27,889 cells (approx 221.3 KB)
Memory Reduction = 1 - (12,687 / 27,889) = 55.2% Space Saved
```

---

## Mathematical Formulation of Mining Metrics

Given transactions T and itemsets X, Y:

1. **Support (S)**: Fraction of total baskets containing X union Y:
   $$\text{Support}(X \to Y) = \frac{\sigma(X \cup Y)}{|T|}$$

2. **Confidence (C)**: Conditional probability that basket contains Y given X:
   $$\text{Confidence}(X \to Y) = \frac{\text{Support}(X \cup Y)}{\text{Support}(X)} = P(Y \mid X)$$

3. **Lift (L)**: Ratio of observed joint frequency to expected frequency under independence:
   $$\text{Lift}(X \to Y) = \frac{\text{Confidence}(X \to Y)}{\text{Support}(Y)} = \frac{P(X \cap Y)}{P(X) \cdot P(Y)}$$
   * Lift > 1.0: Positive synergy and complementary cross-selling potential.
   * Lift = 1.0: Independent purchasing behavior.
   * Lift < 1.0: Negative affinity or substitute products.

4. **Leverage**: Absolute difference between joint co-occurrence and independent expectations:
   $$\text{Leverage}(X \to Y) = \text{Support}(X \to Y) - (\text{Support}(X) \cdot \text{Support}(Y))$$

---

## Project Structure

```
.
├── market_basket_system.py    # Core Graph Data Structures & Apriori Mining Engine
├── test_market_basket.py      # Automated Pytest Test Suite (23 Test Cases)
├── requirements.txt           # Environment Dependencies
├── data/                      # Transactional Dataset
│   └── supermarket_transactions.csv # 14,963 Clean Customer Baskets
├── web/                       # Standalone Web Analytics UI
│   ├── index.html             # UI Structure & 4-Tab Navigation
│   ├── style.css              # Clean Slate/White High-Contrast Styling
│   ├── app.js                 # Force-Directed Graph, Cart Simulator & Rule Filter
│   ├── real_data.json         # Pre-indexed Graph Nodes, Edges & 1,924 Rules
│   └── supermarket_transactions.csv # Direct Web Download Asset
└── README.md                  # System Documentation
```

---

## Quickstart & Local Execution

### 1. Environment Setup & Testing

```bash
# Clone the repository
git clone https://github.com/ayqon/GraphBasket-DSA-Engine.git
cd GraphBasket-DSA-Engine

# Install dependencies
pip install -r requirements.txt

# Run full automated test suite
pytest test_market_basket.py -v
```

### 2. Launch Web Analytics UI

```bash
# Serve the web application locally
python -m http.server 8090 --directory web
```
Navigate to `http://localhost:8090/` in your browser (or visit the live deployment at [https://graphbasket-dsa-engine.onrender.com](https://graphbasket-dsa-engine.onrender.com)).

---

## Web Platform Modules

1. **Interactive Product Affinity Graph**: Physics-driven network canvas displaying item frequency nodes and co-purchase edges with degree centrality inspection.
2. **Apriori Rule Discovery**: Real-time slider filtering across 1,924 association rules by Support, Confidence, and Lift thresholds.
3. **Smart Basket Recommender**: E-commerce cart simulator that computes real-time multi-item neighborhood lift and bundle cross-sell potential.
4. **DSA Complexity Benchmarks**: Visual and mathematical comparison of Adjacency List memory efficiency vs Adjacency Matrices and downward-closure pruning rates.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
