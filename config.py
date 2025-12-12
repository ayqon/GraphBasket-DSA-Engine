"""
Configuration File for Market Basket Analysis System
Centralized settings for easy customization
"""

# ============================================================================
# DATASET CONFIGURATION
# ============================================================================

# Path to input CSV file
DATASET_PATH = "Supermarket_dataset_PAI (2).csv"

# CSV column names (must match your data)
CSV_COLUMN_MEMBER = "Member_number"
CSV_COLUMN_DATE = "Date"
CSV_COLUMN_ITEM = "itemDescription"

# Date format in CSV (e.g., "21-07-2015")
DATE_FORMAT = "%d-%m-%Y"


# ============================================================================
# ALGORITHM PARAMETERS
# ============================================================================

# Apriori Algorithm Configuration
APRIORI_MIN_SUPPORT = 0.02  # Minimum support threshold (0-1)
# Interpretation: Items must appear in at least 2% of transactions
# Lower = More itemsets (more computation)
# Higher = Faster analysis, fewer itemsets

# Association Rule Mining Configuration
RULE_MIN_CONFIDENCE = 0.3   # Minimum confidence threshold (0-1)
# Interpretation: If A is bought, B is bought at least 30% of the time
# Lower = More rules (more candidates)
# Higher = Fewer, higher-quality rules

RULE_MIN_LIFT = 1.0        # Minimum lift threshold (>0)
# Interpretation: Only show rules where B is at least 1.0x more likely with A
# Lift > 1: Positive correlation
# Lift = 1: No correlation
# Lift < 1: Negative correlation


# ============================================================================
# ANALYSIS PARAMETERS
# ============================================================================

# Number of top products to display
TOP_PRODUCTS_COUNT = 10

# Number of top association rules to display
TOP_RULES_COUNT = 15

# Number of top itemsets by size to display
TOP_ITEMSETS_COUNT = 5

# Minimum transaction size to include (0 = all)
MIN_TRANSACTION_SIZE = 0


# ============================================================================
# VISUALIZATION CONFIGURATION
# ============================================================================

# Output directory for visualizations
OUTPUT_DIRECTORY = "analysis_results"

# Figure size for plots (width, height) in inches
FIGURE_SIZE = (14, 10)

# DPI for saved images (300 = high quality, 150 = normal, 100 = low)
IMAGE_DPI = 300

# Color scheme preferences
COLOR_TOP_PRODUCTS = "steelblue"
COLOR_RULES_LIFT = "coral"
COLOR_RULES_CONFIDENCE = "skyblue"
COLOR_ITEMSETS = "mediumseagreen"
COLOR_TRANSACTION_SIZE = "skyblue"
COLOR_TRANSACTION_ITEMS = "lightcoral"
COLOR_STATISTICS = "wheat"
COLOR_DATES = "mediumpurple"

# Whether to display plots interactively (True = show, False = save only)
SHOW_PLOTS = False

# Whether to save plots as PNG
SAVE_PLOTS = True


# ============================================================================
# REPORTING CONFIGURATION
# ============================================================================

# Output file for text report
REPORT_OUTPUT_FILE = "analysis_results.txt"

# Number of rules to include in detailed report
REPORT_RULES_COUNT = 15

# Number of itemsets to include in detailed report
REPORT_ITEMSETS_COUNT = 5


# ============================================================================
# PERFORMANCE TUNING
# ============================================================================

# Maximum number of transactions to load (0 = load all)
MAX_TRANSACTIONS = 0

# Process transactions in batches (useful for large datasets)
# Set to 0 for all-at-once processing
BATCH_SIZE = 0

# Enable performance metrics reporting
REPORT_PERFORMANCE = True

# Enable verbose logging
VERBOSE = True


# ============================================================================
# DATA CLEANING & PREPROCESSING
# ============================================================================

# Convert item names to lowercase
NORMALIZE_TO_LOWERCASE = True

# Strip whitespace from item names
STRIP_WHITESPACE = True

# Remove duplicate items in same transaction
REMOVE_DUPLICATES = True

# Exclude transactions with fewer than N items (0 = no exclusion)
EXCLUDE_SMALL_TRANSACTIONS = 0

# Exclude transactions with more than N items (0 = no limit)
EXCLUDE_LARGE_TRANSACTIONS = 0

# Items to exclude from analysis (case-insensitive after normalization)
EXCLUDED_ITEMS = []

# Category mappings (empty dict = no categorization)
ITEM_CATEGORY_MAPPING = {}


# ============================================================================
# ANALYSIS TUNING
# ============================================================================

# Maximum itemset size to generate (0 = unlimited)
MAX_ITEMSET_SIZE = 5

# Whether to calculate support for all generated candidates
CALCULATE_ALL_SUPPORT = True

# Cache frequently used calculations
USE_CACHING = True

# Number of top products to analyze for correlation
TOP_PRODUCTS_FOR_CORRELATION = 20


# ============================================================================
# EXPORT & OUTPUT OPTIONS
# ============================================================================

# Export results to CSV files
EXPORT_TO_CSV = True

# Export frequent itemsets
EXPORT_ITEMSETS_CSV = "frequent_itemsets.csv"

# Export association rules
EXPORT_RULES_CSV = "association_rules.csv"

# Export product statistics
EXPORT_PRODUCTS_CSV = "product_statistics.csv"

# Generate markdown report in addition to text report
GENERATE_MARKDOWN_REPORT = True

# Markdown report filename
MARKDOWN_REPORT_FILE = "ANALYSIS_REPORT.md"


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def validate_parameters():
    """Validate configuration parameters for logical consistency"""
    
    issues = []
    
    if not (0 < APRIORI_MIN_SUPPORT <= 1):
        issues.append(f"APRIORI_MIN_SUPPORT must be between 0 and 1, got {APRIORI_MIN_SUPPORT}")
    
    if not (0 <= RULE_MIN_CONFIDENCE <= 1):
        issues.append(f"RULE_MIN_CONFIDENCE must be between 0 and 1, got {RULE_MIN_CONFIDENCE}")
    
    if RULE_MIN_LIFT <= 0:
        issues.append(f"RULE_MIN_LIFT must be greater than 0, got {RULE_MIN_LIFT}")
    
    if TOP_PRODUCTS_COUNT <= 0:
        issues.append(f"TOP_PRODUCTS_COUNT must be positive, got {TOP_PRODUCTS_COUNT}")
    
    if IMAGE_DPI <= 0:
        issues.append(f"IMAGE_DPI must be positive, got {IMAGE_DPI}")
    
    if BATCH_SIZE < 0:
        issues.append(f"BATCH_SIZE cannot be negative, got {BATCH_SIZE}")
    
    if MAX_ITEMSET_SIZE < 0:
        issues.append(f"MAX_ITEMSET_SIZE cannot be negative, got {MAX_ITEMSET_SIZE}")
    
    if issues:
        print("Configuration Validation Issues:")
        for issue in issues:
            print(f"  ✗ {issue}")
        raise ValueError(f"Invalid configuration: {len(issues)} issues found")
    
    print("✓ Configuration validated successfully")
    return True


def print_configuration():
    """Print current configuration for verification"""
    
    print("\n" + "="*80)
    print("MARKET BASKET ANALYSIS - ACTIVE CONFIGURATION")
    print("="*80)
    
    print("\nDATASET:")
    print(f"  File: {DATASET_PATH}")
    print(f"  Column Mapping: Member={CSV_COLUMN_MEMBER}, Date={CSV_COLUMN_DATE}, Item={CSV_COLUMN_ITEM}")
    
    print("\nALGORITHM PARAMETERS:")
    print(f"  Min Support: {APRIORI_MIN_SUPPORT} ({APRIORI_MIN_SUPPORT*100:.1f}%)")
    print(f"  Min Confidence: {RULE_MIN_CONFIDENCE} ({RULE_MIN_CONFIDENCE*100:.1f}%)")
    print(f"  Min Lift: {RULE_MIN_LIFT}")
    
    print("\nVISUALIZATION:")
    print(f"  Output Directory: {OUTPUT_DIRECTORY}")
    print(f"  Figure Size: {FIGURE_SIZE}")
    print(f"  DPI: {IMAGE_DPI}")
    print(f"  Show Plots: {SHOW_PLOTS}, Save Plots: {SAVE_PLOTS}")
    
    print("\nREPORTING:")
    print(f"  Report File: {REPORT_OUTPUT_FILE}")
    print(f"  Include Markdown: {GENERATE_MARKDOWN_REPORT}")
    
    print("\nDATA CLEANING:")
    print(f"  Normalize to Lowercase: {NORMALIZE_TO_LOWERCASE}")
    print(f"  Strip Whitespace: {STRIP_WHITESPACE}")
    print(f"  Remove Duplicates: {REMOVE_DUPLICATES}")
    
    print("\nPERFORMANCE:")
    print(f"  Max Transactions: {MAX_TRANSACTIONS if MAX_TRANSACTIONS > 0 else 'Unlimited'}")
    print(f"  Batch Size: {BATCH_SIZE if BATCH_SIZE > 0 else 'All at once'}")
    print(f"  Use Caching: {USE_CACHING}")
    print(f"  Verbose: {VERBOSE}")
    
    print("\n" + "="*80 + "\n")


# ============================================================================
# PRESET CONFIGURATIONS
# ============================================================================

class Presets:
    """Predefined configuration presets for common scenarios"""
    
    @staticmethod
    def quick_analysis():
        """Fast analysis with fewer results"""
        return {
            'APRIORI_MIN_SUPPORT': 0.05,
            'RULE_MIN_CONFIDENCE': 0.5,
            'TOP_PRODUCTS_COUNT': 5,
            'TOP_RULES_COUNT': 5,
        }
    
    @staticmethod
    def detailed_analysis():
        """Thorough analysis with many results"""
        return {
            'APRIORI_MIN_SUPPORT': 0.01,
            'RULE_MIN_CONFIDENCE': 0.3,
            'TOP_PRODUCTS_COUNT': 20,
            'TOP_RULES_COUNT': 30,
        }
    
    @staticmethod
    def aggressive_mining():
        """Find all significant patterns"""
        return {
            'APRIORI_MIN_SUPPORT': 0.005,
            'RULE_MIN_CONFIDENCE': 0.25,
            'TOP_PRODUCTS_COUNT': 50,
            'TOP_RULES_COUNT': 100,
            'MAX_ITEMSET_SIZE': 0,
        }
    
    @staticmethod
    def conservative_mining():
        """Only strong, clear patterns"""
        return {
            'APRIORI_MIN_SUPPORT': 0.1,
            'RULE_MIN_CONFIDENCE': 0.7,
            'RULE_MIN_LIFT': 2.0,
            'TOP_PRODUCTS_COUNT': 10,
            'TOP_RULES_COUNT': 10,
        }


if __name__ == "__main__":
    # Validate and print configuration
    validate_parameters()
    print_configuration()
    print("Configuration is ready to use!")
