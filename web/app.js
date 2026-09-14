// GraphBasket Analytics - Interactive Logic
document.addEventListener('DOMContentLoaded', async () => {
  let appData = null;
  let cart = [];
  let sortColumn = 'lift';
  let sortAsc = false;
  let network = null;

  // Category Color Palette
  const categoryColors = {
    'Dairy & Eggs': '#2563eb',
    'Fresh Produce': '#059669',
    'Bakery & Grains': '#d97706',
    'Beverages': '#0284c7',
    'Meat & Seafood': '#dc2626',
    'Snacks & Sweets': '#7c3aed',
    'Household & Care': '#475569',
    'Pantry & Groceries': '#65a30d'
  };

  // 1. Fetch Real Data
  try {
    const res = await fetch('real_data.json');
    appData = await res.json();
    console.log('Loaded Market Basket Data:', appData);
  } catch (err) {
    console.error('Failed to load real_data.json:', err);
    return;
  }

  // 2. Initialize UI Tabs
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      const targetPane = document.getElementById(btn.dataset.tab);
      if (targetPane) targetPane.classList.add('active');
      if (btn.dataset.tab === 'tab-graph' && network) {
        network.fit();
      }
    });
  });

  // 3. Initialize Top Metrics
  document.getElementById('m-baskets').textContent = appData.summary.total_transactions.toLocaleString();
  document.getElementById('m-items').textContent = appData.summary.total_unique_items.toLocaleString();
  document.getElementById('m-edges').textContent = appData.dsa_benchmarks.num_edges.toLocaleString();
  document.getElementById('m-rules').textContent = appData.summary.total_rules.toLocaleString();
  document.getElementById('m-eff').textContent = appData.dsa_benchmarks.memory_saving_pct + '%';

  // 4. TAB 1: Vis-Network Force Graph
  function initVisGraph() {
    const container = document.getElementById('vis-graph');
    if (!container || typeof vis === 'undefined') {
      console.warn('vis-network not loaded or container missing');
      return;
    }

    const rawNodes = appData.graph_data.nodes;
    const rawEdges = appData.graph_data.edges;

    const visNodes = new vis.DataSet(rawNodes.map(n => ({
      id: n.id,
      label: n.label,
      value: n.count,
      color: {
        background: categoryColors[n.category] || '#2563eb',
        border: '#0f172a',
        highlight: {
          background: '#0f172a',
          border: '#2563eb'
        }
      },
      font: {
        color: '#0f172a',
        size: 12,
        face: 'Inter, sans-serif'
      },
      title: `${n.label} (${n.category})
Frequency: ${n.count} baskets (${n.frequency}%)`
    })));

    const visEdges = new vis.DataSet(rawEdges.map(e => ({
      from: e.source,
      to: e.target,
      value: e.weight,
      color: { color: '#cbd5e1', highlight: '#2563eb' },
      title: `Co-purchases: ${e.weight} | Lift: ${e.lift}x | Jaccard: ${e.jaccard}`
    })));

    const data = { nodes: visNodes, edges: visEdges };
    const options = {
      nodes: {
        shape: 'dot',
        scaling: {
          min: 10,
          max: 32
        },
        borderWidth: 1.5
      },
      edges: {
        scaling: { min: 0.5, max: 4 },
        smooth: { type: 'continuous' }
      },
      physics: {
        barnesHut: {
          gravitationalConstant: -3500,
          centralGravity: 0.3,
          springLength: 95,
          springConstant: 0.04,
          damping: 0.09
        },
        stabilization: { iterations: 120 }
      },
      interaction: {
        hover: true,
        tooltipDelay: 100,
        zoomView: true
      }
    };

    network = new vis.Network(container, data, options);

    // Node selection interaction
    network.on('selectNode', params => {
      if (params.nodes.length > 0) {
        const nodeId = params.nodes[0];
        const node = rawNodes.find(n => n.id === nodeId);
        if (node) {
          showNodeDetails(node);
        }
      }
    });

    // Populate Category Legend
    const legendEl = document.getElementById('category-legend');
    legendEl.innerHTML = Object.entries(categoryColors).map(([cat, color]) => `
      <div class="legend-item">
        <span class="legend-dot" style="background-color: ${color}"></span>
        <span>${cat}</span>
      </div>
    `).join('');
  }

  function showNodeDetails(node) {
    const rawEdges = appData.graph_data.edges;
    const connectedEdges = rawEdges.filter(e => e.source === node.id || e.target === node.id);
    connectedEdges.sort((a, b) => b.weight - a.weight);

    const detailsEl = document.getElementById('node-details');
    detailsEl.className = 'node-inspector-content';
    detailsEl.innerHTML = `
      <div class="stat-row"><span class="stat-lbl">Product</span><span class="stat-val">${node.label}</span></div>
      <div class="stat-row"><span class="stat-lbl">Category</span><span class="stat-val">${node.category}</span></div>
      <div class="stat-row"><span class="stat-lbl">Transaction Frequency</span><span class="stat-val">${node.count} baskets (${node.frequency}%)</span></div>
      <div class="stat-row"><span class="stat-lbl">Degree Centrality</span><span class="stat-val">${connectedEdges.length} connections</span></div>
      <div class="mt-4"><span class="stat-lbl" style="font-weight: 600;">Top Co-Purchase Affinities:</span></div>
      <div style="margin-top: 6px;">
        ${connectedEdges.slice(0, 8).map(e => {
          const neighborId = e.source === node.id ? e.target : e.source;
          const neighbor = appData.graph_data.nodes.find(n => n.id === neighborId) || { label: neighborId };
          return `<span class="neighbor-tag"><strong>${neighbor.label}</strong> (x${e.weight}, Lift ${e.lift})</span>`;
        }).join('')}
      </div>
    `;
  }

  initVisGraph();

  document.getElementById('btn-fit-graph').addEventListener('click', () => {
    if (network) network.fit();
  });

  document.getElementById('graph-search').addEventListener('input', e => {
    const q = e.target.value.toLowerCase().trim();
    if (!q || !network) return;
    const match = appData.graph_data.nodes.find(n => n.id.includes(q) || n.label.toLowerCase().includes(q));
    if (match) {
      network.selectNodes([match.id]);
      network.focus(match.id, { scale: 1.2, animation: true });
      showNodeDetails(match);
    }
  });

  // 5. TAB 2: Apriori Association Rules Table
  const minLiftSlider = document.getElementById('min-lift-slider');
  const minConfSlider = document.getElementById('min-conf-slider');
  const minSupSlider = document.getElementById('min-sup-slider');
  const searchRulesInput = document.getElementById('search-rules');
  const rulesTbody = document.getElementById('rules-tbody');
  const rulesCountDisplay = document.getElementById('rules-count-display');

  function renderRules() {
    const minLift = parseFloat(minLiftSlider.value);
    const minConf = parseFloat(minConfSlider.value);
    const minSup = parseFloat(minSupSlider.value);
    const query = searchRulesInput.value.toLowerCase().trim();

    document.getElementById('val-min-lift').textContent = minLift.toFixed(2);
    document.getElementById('val-min-conf').textContent = minConf.toFixed(1) + '%';
    document.getElementById('val-min-sup').textContent = minSup.toFixed(2) + '%';

    let filtered = appData.rules.filter(r => {
      if (r.lift < minLift) return false;
      if (r.confidence < minConf) return false;
      if (r.support < minSup) return false;
      if (query && !r.antecedent.toLowerCase().includes(query) && !r.consequent.toLowerCase().includes(query)) {
        return false;
      }
      return true;
    });

    // Sort
    filtered.sort((a, b) => {
      const valA = a[sortColumn];
      const valB = b[sortColumn];
      return sortAsc ? (valA > valB ? 1 : -1) : (valA < valB ? 1 : -1);
    });

    rulesCountDisplay.textContent = `Showing ${filtered.length} mined association rules (Filtered from ${appData.summary.total_rules})`;

    if (!filtered.length) {
      rulesTbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding: 24px; color: var(--text-muted);">No rules match the current threshold filters. Adjust sliders to expand candidate space.</td></tr>`;
      return;
    }

    rulesTbody.innerHTML = filtered.slice(0, 100).map(r => `
      <tr>
        <td><strong>${r.antecedent}</strong></td>
        <td class="text-center" style="color: var(--accent-blue); font-weight: 700;">&rarr;</td>
        <td><strong>${r.consequent}</strong></td>
        <td>${r.support.toFixed(3)}%</td>
        <td>${r.confidence.toFixed(2)}%</td>
        <td><span class="badge-val" style="background: var(--accent-blue-subtle); color: var(--accent-blue); font-weight:700;">${r.lift.toFixed(2)}</span></td>
        <td>${r.leverage.toFixed(2)}</td>
        <td>${r.co_count.toLocaleString()}</td>
      </tr>
    `).join('');
  }

  [minLiftSlider, minConfSlider, minSupSlider, searchRulesInput].forEach(el => el.addEventListener('input', renderRules));

  document.querySelectorAll('#rules-table th.sortable').forEach(th => {
    th.addEventListener('click', () => {
      const col = th.dataset.sort;
      if (sortColumn === col) {
        sortAsc = !sortAsc;
      } else {
        sortColumn = col;
        sortAsc = false;
      }
      renderRules();
    });
  });

  document.querySelectorAll('.rule-quick-presets button').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.rule-quick-presets button').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const preset = btn.dataset.preset;
      if (preset === 'high-lift') {
        minLiftSlider.value = 1.4;
        minConfSlider.value = 2.0;
      } else if (preset === 'high-conf') {
        minLiftSlider.value = 1.0;
        minConfSlider.value = 12.0;
      } else {
        minLiftSlider.value = 1.0;
        minConfSlider.value = 2.0;
      }
      renderRules();
    });
  });

  renderRules();

  // 6. TAB 3: Smart Shopping Cart Simulator
  const productSelect = document.getElementById('product-select');
  const quickTagsContainer = document.getElementById('quick-tags-container');
  const cartItemsList = document.getElementById('cart-items-list');
  const cartItemCount = document.getElementById('cart-item-count');
  const recList = document.getElementById('rec-list');

  // Populate Dropdown
  appData.all_products.forEach(p => {
    const opt = document.createElement('option');
    opt.value = p.id;
    opt.textContent = `${p.name} (${p.category})`;
    productSelect.appendChild(opt);
  });

  // Populate Starter Tags
  const starterItems = ['whole milk', 'rolls/buns', 'other vegetables', 'soda', 'yogurt', 'sausage', 'tropical fruit'];
  starterItems.forEach(item => {
    const btn = document.createElement('button');
    btn.className = 'quick-tag-btn';
    btn.textContent = '+ ' + item.split('/').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join('/');
    btn.addEventListener('click', () => addItemToCart(item));
    quickTagsContainer.appendChild(btn);
  });

  document.getElementById('btn-add-item').addEventListener('click', () => {
    const val = productSelect.value;
    if (val) {
      addItemToCart(val);
      productSelect.value = '';
    }
  });

  document.getElementById('btn-clear-cart').addEventListener('click', () => {
    cart = [];
    updateCartUI();
  });

  function addItemToCart(itemId) {
    if (cart.includes(itemId)) return;
    cart.push(itemId);
    updateCartUI();
  }

  function removeFromCart(itemId) {
    cart = cart.filter(id => id !== itemId);
    updateCartUI();
  }

  let categoryChart = null;

  function updateCartUI() {
    cartItemCount.textContent = cart.length;

    if (!cart.length) {
      cartItemsList.innerHTML = '<div class="empty-cart-msg">Your basket is empty. Select items above to see graph affinity recommendations.</div>';
      recList.innerHTML = '<div class="empty-rec-msg">Add items to the basket to unlock affinity recommendations.</div>';
      document.getElementById('b-avg-lift').textContent = '1.00x';
      document.getElementById('b-max-pair').textContent = 'None';
      document.getElementById('b-potential').textContent = 'Base';
      if (categoryChart) categoryChart.destroy();
      return;
    }

    // Render Cart Items
    cartItemsList.innerHTML = cart.map(id => {
      const p = appData.all_products.find(x => x.id === id) || { name: id, category: 'General' };
      return `
        <div class="cart-item-row">
          <div class="cart-item-info">
            <span class="legend-dot" style="background-color: ${categoryColors[p.category] || '#64748b'}"></span>
            <strong>${p.name}</strong>
            <span class="neighbor-tag">${p.category}</span>
          </div>
          <button class="btn-remove-item" onclick="window.removeCartItem('${id}')">&times;</button>
        </div>
      `;
    }).join('');

    // Compute Multi-Item Graph Recommendations
    const recScores = new Map();
    const cartSet = new Set(cart);

    cart.forEach(item => {
      const neighbors = appData.adj_map[item] || [];
      neighbors.forEach(n => {
        if (cartSet.has(n.item)) return;
        if (!recScores.has(n.item)) {
          recScores.set(n.item, {
            item: n.item,
            label: n.label,
            category: n.category,
            totalLift: 0,
            count: 0,
            maxLift: 0,
            bestConf: 0
          });
        }
        const entry = recScores.get(n.item);
        entry.totalLift += n.lift;
        entry.count += 1;
        entry.maxLift = Math.max(entry.maxLift, n.lift);
        entry.bestConf = Math.max(entry.bestConf, n.confidence);
      });
    });

    const recommendations = Array.from(recScores.values());
    recommendations.sort((a, b) => (b.totalLift * b.count) - (a.totalLift * a.count));

    if (!recommendations.length) {
      recList.innerHTML = '<div class="empty-rec-msg">No high-confidence associations found for this combination.</div>';
    } else {
      recList.innerHTML = recommendations.slice(0, 5).map(r => `
        <div class="rec-card">
          <div class="rec-card-info">
            <div class="rec-name">${r.label} <span class="neighbor-tag">${r.category}</span></div>
            <div class="rec-stats">Synergy Lift: <strong>${r.maxLift.toFixed(2)}x</strong> | Linked with ${r.count} basket item(s)</div>
          </div>
          <button class="btn btn-primary" style="padding: 4px 10px; font-size: 11px;" onclick="window.addCartItem('${r.item}')">+ Add to Cart</button>
        </div>
      `).join('');
    }

    // Basket Synergy Metrics
    let totalPairLift = 0;
    let pairCount = 0;
    let maxLift = 0;
    let maxPair = 'None';

    for (let i = 0; i < cart.length; i++) {
      for (let j = i + 1; j < cart.length; j++) {
        const u = cart[i];
        const v = cart[j];
        const nList = appData.adj_map[u] || [];
        const match = nList.find(n => n.item === v);
        if (match) {
          totalPairLift += match.lift;
          pairCount++;
          if (match.lift > maxLift) {
            maxLift = match.lift;
            maxPair = `${u.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')} + ${v.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')} (${match.lift}x)`;
          }
        }
      }
    }

    const avgLift = pairCount > 0 ? (totalPairLift / pairCount).toFixed(2) : '1.00';
    document.getElementById('b-avg-lift').textContent = avgLift + 'x';
    document.getElementById('b-max-pair').textContent = maxPair;
    document.getElementById('b-potential').textContent = pairCount > 2 ? 'Very High Synergy' : (pairCount > 0 ? 'Positive Synergy' : 'Independent');

    // Update Cart Category Doughnut Chart
    const catCounts = {};
    cart.forEach(id => {
      const p = appData.all_products.find(x => x.id === id);
      const cat = p ? p.category : 'Other';
      catCounts[cat] = (catCounts[cat] || 0) + 1;
    });

    if (categoryChart) categoryChart.destroy();
    const ctxCat = document.getElementById('cart-category-chart').getContext('2d');
    categoryChart = new Chart(ctxCat, {
      type: 'doughnut',
      data: {
        labels: Object.keys(catCounts),
        datasets: [{
          data: Object.values(catCounts),
          backgroundColor: Object.keys(catCounts).map(k => categoryColors[k] || '#64748b'),
          borderWidth: 2,
          borderColor: '#ffffff'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'right', labels: { boxWidth: 10, font: { size: 10, family: 'Inter' } } }
        }
      }
    });
  }

  window.addCartItem = addItemToCart;
  window.removeCartItem = removeFromCart;

  // 7. TAB 4: DSA Complexity Charts
  const ctxMem = document.getElementById('dsa-memory-chart').getContext('2d');
  new Chart(ctxMem, {
    type: 'bar',
    data: {
      labels: ['Adjacency List O(V + 2E)', 'Adjacency Matrix O(V^2)'],
      datasets: [{
        label: 'Memory Footprint (KB)',
        data: [appData.dsa_benchmarks.adj_list_memory_kb, appData.dsa_benchmarks.adj_matrix_memory_kb],
        backgroundColor: ['#2563eb', '#cbd5e1'],
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, grid: { color: '#f1f5f9' }, title: { display: true, text: 'Kilobytes (KB)' } },
        x: { grid: { display: false } }
      }
    }
  });

  const ctxPrune = document.getElementById('dsa-pruning-chart').getContext('2d');
  new Chart(ctxPrune, {
    type: 'bar',
    data: {
      labels: ['Theoretical 2-Itemsets (C_2)', 'Mined Frequent Pairs (L_2)'],
      datasets: [{
        label: 'Itemset Combinations',
        data: [appData.dsa_benchmarks.apriori_c2_theoretical, appData.dsa_benchmarks.apriori_c2_mined],
        backgroundColor: ['#94a3b8', '#059669'],
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, grid: { color: '#f1f5f9' }, title: { display: true, text: 'Combinations Count' } },
        x: { grid: { display: false } }
      }
    }
  });

});
