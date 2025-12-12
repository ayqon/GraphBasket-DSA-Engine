"""
Test-Driven Development Tests for Market Basket Analysis System
Tests written FIRST, before implementation
"""

import pytest
from datetime import datetime
from market_basket_system import (
    Product,
    Transaction,
    ProductGraph,
    AprioriAnalyzer,
    AssociationRuleMiner,
    SupermarketDataProcessor
)


# ============ Product Tests ============
class TestProduct:
    """Test Product class"""
    
    def test_product_creation(self):
        """Test creating a product with valid data"""
        product = Product("whole milk", "Dairy")
        assert product.name == "whole milk"
        assert product.category == "Dairy"
    
    def test_product_equality(self):
        """Test product comparison"""
        p1 = Product("whole milk", "Dairy")
        p2 = Product("whole milk", "Dairy")
        assert p1 == p2
    
    def test_product_hash(self):
        """Test product hashing for set operations"""
        p1 = Product("whole milk", "Dairy")
        product_set = {p1}
        assert len(product_set) == 1


# ============ Transaction Tests ============
class TestTransaction:
    """Test Transaction class"""
    
    def test_transaction_creation(self):
        """Test creating a transaction"""
        products = {
            Product("whole milk", "Dairy"),
            Product("bread", "Bakery")
        }
        trans = Transaction(1001, "21-07-2015", products)
        assert trans.member_id == 1001
        assert len(trans.items) == 2
    
    def test_transaction_add_item(self):
        """Test adding items to transaction"""
        trans = Transaction(1001, "21-07-2015", set())
        product = Product("apple", "Fresh")
        trans.add_item(product)
        assert product in trans.items
    
    def test_transaction_size(self):
        """Test transaction size"""
        products = {
            Product("milk", "Dairy"),
            Product("bread", "Bakery"),
            Product("apple", "Fresh")
        }
        trans = Transaction(1001, "21-07-2015", products)
        assert trans.size() == 3


# ============ ProductGraph Tests ============
class TestProductGraph:
    """Test ProductGraph (Graph-based data structure)"""
    
    @pytest.fixture
    def graph(self):
        """Create a sample product graph"""
        g = ProductGraph()
        products = [
            Product("whole milk", "Dairy"),
            Product("bread", "Bakery"),
            Product("butter", "Dairy"),
            Product("apple", "Fresh")
        ]
        for p in products:
            g.add_product(p)
        return g
    
    def test_add_product(self, graph):
        """Test adding products to graph"""
        assert len(graph.products) == 4
    
    def test_add_edge(self, graph):
        """Test adding edges (co-purchases) between products"""
        p1 = Product("whole milk", "Dairy")
        p2 = Product("bread", "Bakery")
        graph.add_edge(p1, p2, weight=5)
        
        neighbors = graph.get_neighbors(p1)
        assert p2 in neighbors
    
    def test_get_neighbors(self, graph):
        """Test retrieving neighbors of a product"""
        p1 = Product("whole milk", "Dairy")
        p2 = Product("bread", "Bakery")
        p3 = Product("butter", "Dairy")
        
        graph.add_edge(p1, p2, weight=3)
        graph.add_edge(p1, p3, weight=2)
        
        neighbors = graph.get_neighbors(p1)
        assert len(neighbors) == 2
    
    def test_get_edge_weight(self, graph):
        """Test retrieving edge weight (co-purchase frequency)"""
        p1 = Product("whole milk", "Dairy")
        p2 = Product("bread", "Bakery")
        graph.add_edge(p1, p2, weight=15)
        
        weight = graph.get_edge_weight(p1, p2)
        assert weight == 15
    
    def test_product_frequency(self, graph):
        """Test getting product frequency"""
        graph.update_product_frequency(Product("whole milk", "Dairy"), 10)
        freq = graph.get_product_frequency(Product("whole milk", "Dairy"))
        assert freq == 10
    
    def test_get_products_by_category(self, graph):
        """Test filtering products by category"""
        dairy_products = graph.get_products_by_category("Dairy")
        assert len(dairy_products) == 2
        assert all(p.category == "Dairy" for p in dairy_products)


# ============ AprioriAnalyzer Tests ============
class TestAprioriAnalyzer:
    """Test Apriori Algorithm implementation"""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer with sample transactions"""
        analyzer = AprioriAnalyzer(min_support=0.3)
        transactions = [
            {"milk", "bread", "butter"},
            {"milk", "bread"},
            {"milk", "butter"},
            {"bread", "butter"},
        ]
        for trans in transactions:
            analyzer.add_transaction(trans)
        return analyzer
    
    def test_add_transaction(self, analyzer):
        """Test adding transactions"""
        assert len(analyzer.transactions) == 4
    
    def test_find_frequent_items_k1(self, analyzer):
        """Test finding 1-itemsets"""
        frequent_1 = analyzer.find_frequent_itemsets(k=1)
        assert len(frequent_1) > 0
        # milk should be frequent (appears 3/4 = 75% > 30%)
        assert frozenset(["milk"]) in frequent_1
    
    def test_find_frequent_itemsets_k2(self, analyzer):
        """Test finding 2-itemsets"""
        frequent_2 = analyzer.find_frequent_itemsets(k=2)
        assert isinstance(frequent_2, dict)
    
    def test_min_support_threshold(self, analyzer):
        """Test that min_support is respected"""
        analyzer2 = AprioriAnalyzer(min_support=0.9)  # Very high threshold
        for trans in analyzer.transactions:
            analyzer2.add_transaction(trans)
        
        frequent = analyzer2.find_frequent_itemsets(k=1)
        # With 90% threshold, unlikely to find frequent items
        assert len(frequent) <= len(analyzer.find_frequent_itemsets(k=1))


# ============ AssociationRuleMiner Tests ============
class TestAssociationRuleMiner:
    """Test Association Rule Mining"""
    
    @pytest.fixture
    def miner(self):
        """Create a rule miner with sample data"""
        miner = AssociationRuleMiner(min_confidence=0.5)
        transactions = [
            {"milk", "bread", "butter"},
            {"milk", "bread"},
            {"milk", "butter"},
            {"bread", "butter"},
        ]
        for trans in transactions:
            miner.add_transaction(trans)
        return miner
    
    def test_generate_rules(self, miner):
        """Test generating association rules"""
        rules = miner.generate_association_rules()
        assert isinstance(rules, list)
    
    def test_rule_confidence(self, miner):
        """Test that generated rules meet min_confidence"""
        rules = miner.generate_association_rules()
        for rule in rules:
            assert rule['confidence'] >= 0.5
    
    def test_rule_structure(self, miner):
        """Test rule has correct structure"""
        rules = miner.generate_association_rules()
        if rules:
            rule = rules[0]
            assert 'antecedent' in rule
            assert 'consequent' in rule
            assert 'confidence' in rule
            assert 'support' in rule
            assert 'lift' in rule


# ============ SupermarketDataProcessor Tests ============
class TestSupermarketDataProcessor:
    """Test data loading and processing"""
    
    def test_load_csv(self, tmp_path):
        """Test loading CSV file"""
        # Create a test CSV
        csv_file = tmp_path / "test_data.csv"
        csv_file.write_text(
            "Member_number,Date,itemDescription\n"
            "1808,21-07-2015,tropical fruit\n"
            "2552,05-01-2015,whole milk\n"
            "1808,21-07-2015,bread\n"
        )
        
        processor = SupermarketDataProcessor()
        transactions = processor.load_from_csv(str(csv_file))
        assert len(transactions) > 0
    
    def test_group_by_member(self, tmp_path):
        """Test grouping items by member and date"""
        csv_file = tmp_path / "test_data.csv"
        csv_file.write_text(
            "Member_number,Date,itemDescription\n"
            "1808,21-07-2015,tropical fruit\n"
            "1808,21-07-2015,bread\n"
            "2552,05-01-2015,milk\n"
        )
        
        processor = SupermarketDataProcessor()
        grouped = processor.group_by_member_and_date(str(csv_file))
        # Member 1808 on 21-07-2015 should have 2 items
        assert any(len(trans.items) == 2 for trans in grouped 
                   if trans.member_id == 1808)


# ============ Integration Tests ============
class TestIntegration:
    """Integration tests for complete workflow"""
    
    def test_end_to_end_analysis(self):
        """Test complete workflow from transactions to rules"""
        # Create analyzer
        analyzer = AprioriAnalyzer(min_support=0.3)
        
        # Add transactions
        transactions = [
            {"milk", "bread", "butter"},
            {"milk", "bread"},
            {"milk", "butter"},
            {"bread", "butter"},
        ]
        for trans in transactions:
            analyzer.add_transaction(trans)
        
        # Find frequent itemsets
        frequent = analyzer.find_frequent_itemsets(k=1)
        assert len(frequent) > 0
        
        # Generate rules
        miner = AssociationRuleMiner(min_confidence=0.5)
        for trans in transactions:
            miner.add_transaction(trans)
        rules = miner.generate_association_rules()
        assert isinstance(rules, list)
    
    def test_graph_construction_from_transactions(self):
        """Test building product graph from transactions"""
        graph = ProductGraph()
        
        transactions = [
            {Product("milk", "Dairy"), Product("bread", "Bakery")},
            {Product("milk", "Dairy"), Product("butter", "Dairy")},
        ]
        
        for trans in transactions:
            for p1 in trans:
                if p1 not in graph.products:
                    graph.add_product(p1)
                for p2 in trans:
                    if p1 != p2 and p2 not in graph.products:
                        graph.add_product(p2)
                    if p1 != p2:
                        graph.add_edge(p1, p2, weight=1)
        
        assert len(graph.products) >= 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
