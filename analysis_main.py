"""
Market Basket Analysis - Main Analysis Script with Visualization
Performs comprehensive analysis on supermarket dataset
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from market_basket_system import (
    MarketBasketAnalysisSystem,
    SupermarketDataProcessor
)
import os


class AnalysisVisualizer:
    """Creates visualizations for market basket analysis results"""
    
    def __init__(self, figsize=(14, 10)):
        """Initialize visualizer with figure size"""
        self.figsize = figsize
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = figsize
    
    def plot_top_products(self, system, top_k=15):
        """Plot top products by frequency"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        top_products = system.get_top_products(top_k)
        products = [p[0].name for p in top_products]
        frequencies = [p[1] for p in top_products]
        
        bars = ax.barh(products, frequencies, color='steelblue')
        ax.set_xlabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_ylabel('Product', fontsize=12, fontweight='bold')
        ax.set_title(f'Top {top_k} Most Purchased Products', fontsize=14, fontweight='bold')
        
        # Add value labels
        for i, bar in enumerate(bars):
            ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2, 
                   f' {int(frequencies[i])}', va='center', fontsize=10)
        
        plt.tight_layout()
        return fig
    
    def plot_association_rules(self, rules, top_k=10):
        """Plot top association rules by lift"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if not rules:
            ax.text(0.5, 0.5, 'No association rules found', 
                   ha='center', va='center', fontsize=12)
            return fig
        
        top_rules = rules[:top_k]
        rule_labels = [
            f"{', '.join(r['antecedent'])} → {', '.join(r['consequent'])}" 
            for r in top_rules
        ]
        lifts = [r['lift'] for r in top_rules]
        confidences = [r['confidence'] for r in top_rules]
        
        x_pos = range(len(top_rules))
        bars1 = ax.bar([i - 0.2 for i in x_pos], lifts, 0.4, 
                       label='Lift', color='coral', alpha=0.8)
        bars2 = ax.bar([i + 0.2 for i in x_pos], confidences, 0.4, 
                       label='Confidence', color='skyblue', alpha=0.8)
        
        ax.set_ylabel('Value', fontsize=12, fontweight='bold')
        ax.set_title(f'Top {top_k} Association Rules (by Lift)', fontsize=14, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels([f"Rule {i+1}" for i in range(len(top_rules))], fontsize=10)
        ax.legend(fontsize=11)
        ax.axhline(y=1, color='red', linestyle='--', linewidth=1, label='Lift = 1')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig
    
    def plot_frequent_itemsets(self, system):
        """Plot distribution of frequent itemset sizes"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        all_itemsets = system.get_frequent_itemsets()
        sizes = Counter(len(itemset) for itemset in all_itemsets.keys())
        
        if not sizes:
            ax.text(0.5, 0.5, 'No frequent itemsets found', 
                   ha='center', va='center', fontsize=12)
            return fig
        
        size_labels = sorted(sizes.keys())
        counts = [sizes[s] for s in size_labels]
        
        bars = ax.bar(size_labels, counts, color='mediumseagreen', alpha=0.7, edgecolor='black')
        ax.set_xlabel('Itemset Size', fontsize=12, fontweight='bold')
        ax.set_ylabel('Count', fontsize=12, fontweight='bold')
        ax.set_title('Distribution of Frequent Itemset Sizes', fontsize=14, fontweight='bold')
        ax.set_xticks(size_labels)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def plot_transaction_analysis(self, system):
        """Plot transaction statistics"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Transaction sizes
        sizes = [t.size() for t in system.transactions]
        axes[0, 0].hist(sizes, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
        axes[0, 0].set_xlabel('Items per Transaction', fontsize=11, fontweight='bold')
        axes[0, 0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
        axes[0, 0].set_title('Distribution of Transaction Sizes', fontsize=12, fontweight='bold')
        
        # Top items
        item_counter = Counter()
        for transaction in system.transactions:
            item_counter.update(transaction.items)
        
        top_10_items = item_counter.most_common(10)
        items = [item[0][:20] for item in top_10_items]  # Truncate long names
        counts = [item[1] for item in top_10_items]
        
        axes[0, 1].barh(items, counts, color='lightcoral', alpha=0.7, edgecolor='black')
        axes[0, 1].set_xlabel('Frequency', fontsize=11, fontweight='bold')
        axes[0, 1].set_title('Top 10 Items Purchased', fontsize=12, fontweight='bold')
        
        # Summary stats
        summary = system.get_summary()
        stats_text = f"""
        Total Transactions: {summary['total_transactions']}
        Unique Products: {summary['total_products']}
        Frequent Itemsets: {summary['frequent_itemsets_count']}
        Association Rules: {summary['association_rules_count']}
        Avg Items/Transaction: {summary['avg_items_per_transaction']:.2f}
        """
        axes[1, 0].text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                       family='monospace', fontweight='bold')
        axes[1, 0].axis('off')
        
        # Transaction dates distribution
        date_counter = Counter(t.date for t in system.transactions)
        top_dates = date_counter.most_common(10)
        if top_dates:
            dates = [d[0] for d in top_dates]
            trans_count = [d[1] for d in top_dates]
            axes[1, 1].bar(range(len(dates)), trans_count, color='mediumpurple', alpha=0.7, edgecolor='black')
            axes[1, 1].set_xticks(range(len(dates)))
            axes[1, 1].set_xticklabels(dates, rotation=45, ha='right', fontsize=9)
            axes[1, 1].set_ylabel('Transaction Count', fontsize=11, fontweight='bold')
            axes[1, 1].set_title('Top 10 Transaction Dates', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def save_all_plots(self, system, output_dir='analysis_results'):
        """Save all visualizations to files"""
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"Generating visualizations and saving to {output_dir}/...")
        
        # Plot 1: Top Products
        fig1 = self.plot_top_products(system)
        fig1.savefig(os.path.join(output_dir, '01_top_products.png'), dpi=300, bbox_inches='tight')
        print("✓ Saved: 01_top_products.png")
        plt.close(fig1)
        
        # Plot 2: Association Rules
        rules = system.get_association_rules()
        fig2 = self.plot_association_rules(rules)
        fig2.savefig(os.path.join(output_dir, '02_association_rules.png'), dpi=300, bbox_inches='tight')
        print("✓ Saved: 02_association_rules.png")
        plt.close(fig2)
        
        # Plot 3: Frequent Itemsets
        fig3 = self.plot_frequent_itemsets(system)
        fig3.savefig(os.path.join(output_dir, '03_frequent_itemsets.png'), dpi=300, bbox_inches='tight')
        print("✓ Saved: 03_frequent_itemsets.png")
        plt.close(fig3)
        
        # Plot 4: Transaction Analysis
        fig4 = self.plot_transaction_analysis(system)
        fig4.savefig(os.path.join(output_dir, '04_transaction_analysis.png'), dpi=300, bbox_inches='tight')
        print("✓ Saved: 04_transaction_analysis.png")
        plt.close(fig4)


def generate_analysis_report(system, rules, output_file='analysis_results.txt'):
    """Generate detailed text report of analysis"""
    
    summary = system.get_summary()
    
    with open(output_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("MARKET BASKET ANALYSIS - COMPREHENSIVE REPORT\n")
        f.write("=" * 80 + "\n\n")
        
        # Summary Statistics
        f.write("SUMMARY STATISTICS\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total Transactions Analyzed: {summary['total_transactions']}\n")
        f.write(f"Unique Products: {summary['total_products']}\n")
        f.write(f"Frequent Itemsets Found: {summary['frequent_itemsets_count']}\n")
        f.write(f"Association Rules Mined: {summary['association_rules_count']}\n")
        f.write(f"Average Items per Transaction: {summary['avg_items_per_transaction']:.2f}\n\n")
        
        # Top Products
        f.write("TOP 10 MOST PURCHASED PRODUCTS\n")
        f.write("-" * 80 + "\n")
        top_products = system.get_top_products(10)
        for idx, (product, freq) in enumerate(top_products, 1):
            f.write(f"{idx:2d}. {product.name:30s} - Frequency: {freq:5d}\n")
        f.write("\n")
        
        # Top Association Rules
        if rules:
            f.write("TOP 15 ASSOCIATION RULES\n")
            f.write("-" * 80 + "\n")
            f.write(f"{'Rule':<50} | {'Conf':>6} | {'Lift':>6} | {'Supp':>6}\n")
            f.write("-" * 80 + "\n")
            
            for idx, rule in enumerate(rules[:15], 1):
                antecedent_str = ', '.join(sorted(rule['antecedent']))[:25]
                consequent_str = ', '.join(sorted(rule['consequent']))[:20]
                rule_str = f"{antecedent_str} → {consequent_str}"
                
                f.write(f"{rule_str:<50} | {rule['confidence']:6.3f} | "
                       f"{rule['lift']:6.3f} | {rule['support']:6.3f}\n")
            f.write("\n")
        
        # Frequent Itemsets
        f.write("FREQUENT ITEMSETS ANALYSIS\n")
        f.write("-" * 80 + "\n")
        frequent_sets = system.get_frequent_itemsets()
        
        # Group by size
        itemsets_by_size = {}
        for itemset, support in frequent_sets.items():
            size = len(itemset)
            if size not in itemsets_by_size:
                itemsets_by_size[size] = []
            itemsets_by_size[size].append((itemset, support))
        
        for size in sorted(itemsets_by_size.keys())[:5]:  # Show first 5 sizes
            f.write(f"\n{size}-Itemsets (Total: {len(itemsets_by_size[size])})\n")
            for itemset, support in itemsets_by_size[size][:5]:  # Show top 5 in each size
                items_str = ', '.join(sorted(itemset))
                f.write(f"  {items_str:<50} Support: {support:.4f}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 80 + "\n")
    
    print(f"\n✓ Analysis report saved to {output_file}")


def main():
    """Main analysis execution"""
    
    # Dataset path
    dataset_path = "Supermarket_dataset_PAI (2).csv"
    
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset '{dataset_path}' not found!")
        return
    
    print("=" * 80)
    print("MARKET BASKET ANALYSIS SYSTEM")
    print("=" * 80)
    print(f"\nLoading data from: {dataset_path}")
    
    # Initialize system with tuned parameters
    system = MarketBasketAnalysisSystem(min_support=0.02, min_confidence=0.3)
    
    print("Analyzing transactions...")
    system.load_data(dataset_path)
    
    # Get results
    print("Mining frequent itemsets...")
    frequent_sets = system.get_frequent_itemsets()
    
    print("Generating association rules...")
    rules = system.get_association_rules()
    
    # Display summary
    summary = system.get_summary()
    print("\n" + "=" * 80)
    print("ANALYSIS RESULTS")
    print("=" * 80)
    print(f"✓ Transactions processed: {summary['total_transactions']}")
    print(f"✓ Unique products: {summary['total_products']}")
    print(f"✓ Frequent itemsets found: {summary['frequent_itemsets_count']}")
    print(f"✓ Association rules generated: {summary['association_rules_count']}")
    print(f"✓ Average items per transaction: {summary['avg_items_per_transaction']:.2f}")
    
    # Display top products
    print("\n" + "-" * 80)
    print("TOP 10 PRODUCTS")
    print("-" * 80)
    top_products = system.get_top_products(10)
    for idx, (product, freq) in enumerate(top_products, 1):
        print(f"{idx:2d}. {product.name:30s} : {freq:5d} purchases")
    
    # Display sample rules
    if rules:
        print("\n" + "-" * 80)
        print("SAMPLE ASSOCIATION RULES (Top 5)")
        print("-" * 80)
        for idx, rule in enumerate(rules[:5], 1):
            antecedent = ', '.join(sorted(rule['antecedent']))
            consequent = ', '.join(sorted(rule['consequent']))
            print(f"\n{idx}. If customer buys: {antecedent}")
            print(f"   Then likely buys: {consequent}")
            print(f"   Confidence: {rule['confidence']:.1%} | Lift: {rule['lift']:.2f}")
    
    # Generate visualizations
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATIONS...")
    print("=" * 80)
    
    visualizer = AnalysisVisualizer()
    visualizer.save_all_plots(system)
    
    # Generate report
    generate_analysis_report(system, rules)
    
    print("\n" + "=" * 80)
    print("✓ ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\nOutput files:")
    print("  - analysis_results/ (directory with visualizations)")
    print("  - analysis_results.txt (detailed report)")


if __name__ == "__main__":
    main()
