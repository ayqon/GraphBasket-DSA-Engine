"""
Market Basket Analysis System
Implements graph-based data structures and Apriori algorithm for market basket analysis
"""

from collections import defaultdict, deque
from datetime import datetime
from typing import Set, Dict, List, Tuple, FrozenSet
import pandas as pd
from itertools import combinations


# ============ DATA STRUCTURES ============

class Product:
    """Represents a single product in the supermarket"""
    
    def __init__(self, name: str, category: str):
        """
        Initialize a product
        
        Args:
            name: Product name
            category: Product category (e.g., Dairy, Fresh, Bakery)
        """
        self.name = name
        self.category = category
    
    def __eq__(self, other):
        """Check equality based on name and category"""
        if not isinstance(other, Product):
            return False
        return self.name == other.name and self.category == other.category
    
    def __hash__(self):
        """Make product hashable for use in sets and dicts"""
        return hash((self.name, self.category))
    
    def __repr__(self):
        return f"Product({self.name}, {self.category})"
    
    def __lt__(self, other):
        """For sorting products"""
        return self.name < other.name


class Transaction:
    """Represents a single customer transaction"""
    
    def __init__(self, member_id: int, date: str, items: Set[Product]):
        """
        Initialize a transaction
        
        Args:
            member_id: Customer member ID
            date: Transaction date (DD-MM-YYYY)
            items: Set of products purchased
        """
        self.member_id = member_id
        self.date = date
        self.items = items
    
    def add_item(self, product: Product):
        """Add a product to transaction"""
        self.items.add(product)
    
    def size(self) -> int:
        """Get number of items in transaction"""
        return len(self.items)
    
    def __repr__(self):
        return f"Transaction(Member: {self.member_id}, Items: {len(self.items)})"


class ProductGraph:
    """
    Graph data structure representing product relationships
    Nodes: Products
    Edges: Co-purchase relationships with frequency as weight
    
    Computational Complexity:
    - Add product: O(1)
    - Add edge: O(1)
    - Find neighbors: O(degree of node)
    - Get edge weight: O(1)
    """
    
    def __init__(self):
        """Initialize empty product graph"""
        self.products: Set[Product] = set()
        self.graph: Dict[Product, Dict[Product, int]] = defaultdict(dict)
        self.product_frequency: Dict[Product, int] = defaultdict(int)
        self.category_index: Dict[str, Set[Product]] = defaultdict(set)
    
    def add_product(self, product: Product):
        """
        Add a product node to the graph
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if product not in self.products:
            self.products.add(product)
            self.category_index[product.category].add(product)
    
    def add_edge(self, product1: Product, product2: Product, weight: int = 1):
        """
        Add or update an edge between two products
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if product1 not in self.products:
            self.add_product(product1)
        if product2 not in self.products:
            self.add_product(product2)
        
        # Add edge in both directions (undirected graph)
        self.graph[product1][product2] = self.graph[product1].get(product2, 0) + weight
        self.graph[product2][product1] = self.graph[product2].get(product1, 0) + weight
    
    def get_neighbors(self, product: Product) -> List[Product]:
        """
        Get all products frequently bought together with given product
        
        Time Complexity: O(degree)
        Space Complexity: O(degree)
        """
        return list(self.graph.get(product, {}).keys())
    
    def get_edge_weight(self, product1: Product, product2: Product) -> int:
        """
        Get co-purchase frequency between two products
        
        Time Complexity: O(1)
        """
        return self.graph.get(product1, {}).get(product2, 0)
    
    def update_product_frequency(self, product: Product, count: int):
        """
        Update how many times a product appears in transactions
        
        Time Complexity: O(1)
        """
        self.product_frequency[product] += count
    
    def get_product_frequency(self, product: Product) -> int:
        """
        Get frequency of a product
        
        Time Complexity: O(1)
        """
        return self.product_frequency.get(product, 0)
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """
        Get all products in a specific category
        
        Time Complexity: O(k) where k is number of products in category
        """
        return list(self.category_index.get(category, set()))
    
    def get_top_products(self, k: int) -> List[Tuple[Product, int]]:
        """
        Get top k most frequent products
        
        Time Complexity: O(n log k) where n is number of products
        """
        return sorted(
            self.product_frequency.items(),
            key=lambda x: x[1],
            reverse=True
        )[:k]
    
    def get_highly_connected_products(self, min_neighbors: int = 5) -> List[Product]:
        """
        Find products with many co-purchase relationships (hub products)
        
        Time Complexity: O(n) where n is number of products
        """
        return [p for p in self.products if len(self.get_neighbors(p)) >= min_neighbors]


# ============ ALGORITHMS ============

class AprioriAnalyzer:
    """
    Implements Apriori algorithm for frequent itemset mining
    
    Time Complexity: O(2^m * n) where m is items and n is transactions
    Space Complexity: O(2^m) for storing candidate sets
    """
    
    def __init__(self, min_support: float = 0.1):
        """
        Initialize Apriori analyzer
        
        Args:
            min_support: Minimum support threshold (0-1)
        """
        self.min_support = min_support
        self.transactions: List[Set[str]] = []
        self.num_transactions = 0
    
    def add_transaction(self, items: Set[str]):
        """
        Add a transaction
        
        Time Complexity: O(m) where m is number of items
        """
        self.transactions.append(items)
        self.num_transactions += 1
    
    def _get_support(self, itemset: FrozenSet[str]) -> float:
        """
        Calculate support for an itemset
        
        Time Complexity: O(n*m) where n is transactions, m is itemset size
        """
        count = 0
        for transaction in self.transactions:
            if itemset.issubset(transaction):
                count += 1
        return count / self.num_transactions if self.num_transactions > 0 else 0
    
    def _generate_candidates(self, prev_itemsets: Dict[FrozenSet[str], float]) -> Dict[FrozenSet[str], float]:
        """
        Generate candidate itemsets from previous level itemsets
        (Apriori principle: if an itemset is frequent, all subsets are frequent)
        
        Time Complexity: O(k^2) where k is number of itemsets
        """
        candidates = {}
        itemsets = list(prev_itemsets.keys())
        
        for i in range(len(itemsets)):
            for j in range(i + 1, len(itemsets)):
                union = itemsets[i] | itemsets[j]
                if len(union) == len(itemsets[i]) + 1:
                    support = self._get_support(union)
                    if support >= self.min_support:
                        candidates[union] = support
        
        return candidates
    
    def find_frequent_itemsets(self, k: int = None) -> Dict[FrozenSet[str], float]:
        """
        Find frequent itemsets up to size k using Apriori algorithm
        
        Args:
            k: Maximum itemset size (None for all sizes)
        
        Returns:
            Dictionary mapping itemsets to their support values
        
        Time Complexity: O(2^m * n) in worst case
        """
        if self.num_transactions == 0:
            return {}
        
        all_frequent = {}
        
        # Find 1-itemsets
        itemset_support = {}
        all_items = set()
        for transaction in self.transactions:
            for item in transaction:
                all_items.add(item)
        
        for item in all_items:
            itemset = frozenset([item])
            support = self._get_support(itemset)
            if support >= self.min_support:
                itemset_support[itemset] = support
                all_frequent[itemset] = support
        
        # Find k-itemsets
        current_itemsets = itemset_support.copy()
        itemset_size = 1
        
        while current_itemsets and (k is None or itemset_size < k):
            candidates = self._generate_candidates(current_itemsets)
            if not candidates:
                break
            
            current_itemsets = candidates
            all_frequent.update(candidates)
            itemset_size += 1
        
        return all_frequent
    
    def get_frequent_itemsets_by_size(self, k: int) -> Dict[FrozenSet[str], float]:
        """Get only k-sized frequent itemsets"""
        all_frequent = self.find_frequent_itemsets(k)
        return {itemset: support for itemset, support in all_frequent.items() 
                if len(itemset) == k}


class AssociationRuleMiner:
    """
    Mines association rules from frequent itemsets
    
    Time Complexity: O(n * 2^m) for generating rules
    Space Complexity: O(2^m)
    """
    
    def __init__(self, min_confidence: float = 0.5, min_lift: float = 1.0):
        """
        Initialize rule miner
        
        Args:
            min_confidence: Minimum confidence threshold
            min_lift: Minimum lift threshold
        """
        self.min_confidence = min_confidence
        self.min_lift = min_lift
        self.transactions: List[Set[str]] = []
        self.analyzer = None
    
    def add_transaction(self, items: Set[str]):
        """Add transaction for analysis"""
        self.transactions.append(items)
    
    def _calculate_confidence(self, antecedent: FrozenSet[str], 
                             consequent: FrozenSet[str]) -> float:
        """
        Calculate confidence: P(consequent | antecedent)
        
        Time Complexity: O(n) where n is number of transactions
        """
        antecedent_count = 0
        both_count = 0
        
        for transaction in self.transactions:
            if antecedent.issubset(transaction):
                antecedent_count += 1
                if consequent.issubset(transaction):
                    both_count += 1
        
        return both_count / antecedent_count if antecedent_count > 0 else 0
    
    def _calculate_lift(self, antecedent: FrozenSet[str], 
                       consequent: FrozenSet[str]) -> float:
        """
        Calculate lift: P(A and B) / (P(A) * P(B))
        
        Time Complexity: O(n)
        """
        n = len(self.transactions)
        antecedent_count = sum(1 for t in self.transactions if antecedent.issubset(t))
        consequent_count = sum(1 for t in self.transactions if consequent.issubset(t))
        both_count = sum(1 for t in self.transactions 
                        if antecedent.issubset(t) and consequent.issubset(t))
        
        p_a = antecedent_count / n
        p_b = consequent_count / n
        p_ab = both_count / n
        
        if p_a * p_b == 0:
            return 0
        return p_ab / (p_a * p_b)
    
    def generate_association_rules(self) -> List[Dict]:
        """
        Generate association rules from transactions
        
        Returns:
            List of rules with antecedent, consequent, confidence, support, lift
        
        Time Complexity: O(n * 2^m)
        """
        if not self.transactions:
            return []
        
        # Find frequent itemsets first
        self.analyzer = AprioriAnalyzer(min_support=0.01)
        for transaction in self.transactions:
            self.analyzer.add_transaction(transaction)
        
        frequent_itemsets = self.analyzer.find_frequent_itemsets()
        rules = []
        
        # Generate rules from itemsets with 2+ items
        for itemset, support in frequent_itemsets.items():
            if len(itemset) < 2:
                continue
            
            # Generate all possible antecedent-consequent pairs
            itemset_list = list(itemset)
            for i in range(1, len(itemset_list)):
                for antecedent_items in combinations(itemset_list, i):
                    antecedent = frozenset(antecedent_items)
                    consequent = itemset - antecedent
                    
                    confidence = self._calculate_confidence(antecedent, consequent)
                    if confidence >= self.min_confidence:
                        lift = self._calculate_lift(antecedent, consequent)
                        if lift >= self.min_lift:
                            rules.append({
                                'antecedent': set(antecedent),
                                'consequent': set(consequent),
                                'support': support,
                                'confidence': confidence,
                                'lift': lift
                            })
        
        # Sort by confidence and lift
        return sorted(rules, key=lambda x: (x['confidence'], x['lift']), reverse=True)


class SupermarketDataProcessor:
    """
    Processes supermarket CSV data into transaction format
    """
    
    @staticmethod
    def load_from_csv(filepath: str) -> List[Transaction]:
        """
        Load transactions from CSV file
        
        CSV Format: Member_number, Date, itemDescription
        
        Time Complexity: O(n) where n is number of rows
        """
        try:
            df = pd.read_csv(filepath)
            transactions_dict = defaultdict(lambda: {'items': set(), 'date': None})
            
            for _, row in df.iterrows():
                member = row['Member_number']
                date = row['Date']
                item = row['itemDescription'].strip().lower()
                
                # Group by member and date
                key = (member, date)
                if key not in transactions_dict:
                    transactions_dict[key] = {'items': set(), 'date': date, 'member': member}
                
                transactions_dict[key]['items'].add(item)
            
            # Convert to Transaction objects
            transactions = []
            for (member, date), data in transactions_dict.items():
                if len(data['items']) > 0:  # Only include non-empty transactions
                    transactions.append(
                        Transaction(member, date, data['items'])
                    )
            
            return transactions
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return []
    
    @staticmethod
    def group_by_member_and_date(filepath: str) -> List[Transaction]:
        """
        Load and group transactions by member and date
        
        Time Complexity: O(n)
        """
        return SupermarketDataProcessor.load_from_csv(filepath)
    
    @staticmethod
    def get_statistics(transactions: List[Transaction]) -> Dict:
        """
        Calculate statistics about transactions
        
        Time Complexity: O(n*m) where n is transactions, m is average items
        """
        if not transactions:
            return {}
        
        sizes = [t.size() for t in transactions]
        all_items = set()
        for t in transactions:
            all_items.update(t.items)
        
        return {
            'total_transactions': len(transactions),
            'total_unique_items': len(all_items),
            'avg_items_per_transaction': sum(sizes) / len(sizes),
            'min_items': min(sizes),
            'max_items': max(sizes),
            'unique_items': all_items
        }


# ============ ANALYSIS SYSTEM ============

class MarketBasketAnalysisSystem:
    """
    Main system integrating all components for market basket analysis
    """
    
    def __init__(self, min_support: float = 0.05, min_confidence: float = 0.5):
        """Initialize the analysis system"""
        self.graph = ProductGraph()
        self.apriori = AprioriAnalyzer(min_support=min_support)
        self.rule_miner = AssociationRuleMiner(min_confidence=min_confidence)
        self.transactions: List[Transaction] = []
    
    def load_data(self, filepath: str):
        """Load data from CSV file"""
        self.transactions = SupermarketDataProcessor.load_from_csv(filepath)
        self._build_structures()
    
    def _build_structures(self):
        """Build graph and prepare for analysis"""
        # Standardize item names for analysis
        transaction_sets = []
        
        for transaction in self.transactions:
            items = {item.lower().strip() for item in transaction.items}
            transaction_sets.append(items)
            
            # Add to Apriori analyzer
            self.apriori.add_transaction(items)
            self.rule_miner.add_transaction(items)
            
            # Build product graph
            for item in items:
                product = Product(item, "General")
                self.graph.add_product(product)
                self.graph.update_product_frequency(product, 1)
                
                # Add edges for co-purchases
                for item2 in items:
                    if item != item2:
                        product2 = Product(item2, "General")
                        self.graph.add_product(product2)
                        self.graph.add_edge(product, product2, weight=1)
    
    def get_frequent_itemsets(self, k: int = None) -> Dict:
        """Get frequent itemsets"""
        return self.apriori.find_frequent_itemsets(k)
    
    def get_association_rules(self) -> List[Dict]:
        """Get association rules"""
        return self.rule_miner.generate_association_rules()
    
    def get_top_products(self, k: int = 10) -> List[Tuple[Product, int]]:
        """Get top k products by frequency"""
        return self.graph.get_top_products(k)
    
    def get_summary(self) -> Dict:
        """Get analysis summary"""
        frequent_sets = self.apriori.find_frequent_itemsets()
        rules = self.rule_miner.generate_association_rules()
        
        return {
            'total_transactions': len(self.transactions),
            'total_products': len(self.graph.products),
            'frequent_itemsets_count': len(frequent_sets),
            'association_rules_count': len(rules),
            'top_products': self.get_top_products(5),
            'avg_items_per_transaction': (
                sum(t.size() for t in self.transactions) / len(self.transactions)
                if self.transactions else 0
            )
        }


if __name__ == "__main__":
    print("Market Basket Analysis System initialized")
