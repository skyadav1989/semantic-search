// App state
let currentQuery = '';
let debounceTimer = null;

document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('search-input');
  
  // Input clear button toggle
  searchInput.addEventListener('input', (e) => {
    const clearBtn = document.getElementById('clear-btn');
    clearBtn.style.display = e.target.value ? 'flex' : 'none';
  });

  // Auto trigger default search
  performSearch();
});

function setQuery(queryText) {
  const searchInput = document.getElementById('search-input');
  searchInput.value = queryText;
  document.getElementById('clear-btn').style.display = 'flex';
  performSearch();
}

function clearSearch() {
  const searchInput = document.getElementById('search-input');
  searchInput.value = '';
  document.getElementById('clear-btn').style.display = 'none';
  searchInput.focus();
}

async function performSearch() {
  const query = document.getElementById('search-input').value.trim();
  if (!query) return;

  const gridContainer = document.getElementById('products-grid');
  const insightsPanel = document.getElementById('insights-panel');

  // Show loading skeleton
  gridContainer.innerHTML = `
    <div class="loading-state">
      <div class="spinner"></div>
      <p style="color: var(--text-muted); font-size: 0.95rem;">Retrieving semantic vector embeddings & re-ranking...</p>
    </div>
  `;

  try {
    const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
    if (!response.ok) {
      throw new Error(`API response error (${response.status})`);
    }

    const data = await response.json();
    renderInsights(data);
    renderResults(data.results || []);

  } catch (error) {
    console.error("Search error:", error);
    gridContainer.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">⚠️</div>
        <h3 style="margin-bottom: 8px; color: #f87171;">Search Request Failed</h3>
        <p style="color: var(--text-dim); font-size: 0.9rem;">${error.message || 'Unable to connect to search service'}</p>
      </div>
    `;
    insightsPanel.classList.remove('visible');
  }
}

function renderInsights(data) {
  const insightsPanel = document.getElementById('insights-panel');
  const intentBadge = document.getElementById('intent-badge');
  const countStat = document.getElementById('count-stat');
  const latencyBadge = document.getElementById('latency-badge');
  const filtersContainer = document.getElementById('filters-container');
  const termsContainer = document.getElementById('terms-container');
  const normalizedQuery = document.getElementById('normalized-query');

  insightsPanel.classList.add('visible');

  // Intent badge
  const intent = data.intent || 'BUY';
  intentBadge.textContent = intent;
  intentBadge.className = `intent-badge intent-${intent}`;

  // Count & Timing
  countStat.textContent = data.count || (data.results ? data.results.length : 0);
  const elapsedMs = (data.elapsed_ms !== undefined) ? data.elapsed_ms.toFixed(1) : '0.0';
  latencyBadge.textContent = `⚡ ${elapsedMs} ms`;

  // Normalized Query
  normalizedQuery.textContent = data.normalized_query || data.query || '-';

  // Filters
  filtersContainer.innerHTML = '';
  if (data.filters && Object.keys(data.filters).length > 0) {
    for (const [key, val] of Object.entries(data.filters)) {
      let filterText = key;
      if (typeof val === 'object' && val !== null) {
        if (val.lte !== undefined) filterText += ` ≤ ₹${val.lte.toLocaleString()}`;
        if (val.gte !== undefined) filterText += ` ≥ ₹${val.gte.toLocaleString()}`;
        if (val.eq !== undefined) filterText += ` = ${val.eq}`;
      } else {
        filterText += `: ${val}`;
      }
      const span = document.createElement('span');
      span.className = 'filter-pill';
      span.textContent = filterText;
      filtersContainer.appendChild(span);
    }
  } else {
    filtersContainer.innerHTML = '<span class="tag-pill">No filter constraints detected</span>';
  }

  // Expanded terms
  termsContainer.innerHTML = '';
  if (data.expanded_terms && data.expanded_terms.length > 0) {
    data.expanded_terms.forEach(term => {
      const span = document.createElement('span');
      span.className = 'tag-pill';
      span.textContent = term;
      termsContainer.appendChild(span);
    });
  } else {
    termsContainer.innerHTML = '<span class="tag-pill">None</span>';
  }
}

function renderResults(results) {
  const gridContainer = document.getElementById('products-grid');

  if (!results || results.length === 0) {
    gridContainer.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🔍</div>
        <h3>No Products Found</h3>
        <p style="color: var(--text-dim); margin-top: 8px;">Try broadening your query keywords or adjusting price limits.</p>
      </div>
    `;
    return;
  }

  gridContainer.innerHTML = results.map(item => {
    const payload = item.payload || {};
    const title = payload.title || 'Product Item';
    const sku = payload.sku || item.id || '';
    const category = payload.category || 'General';
    const price = payload.price ? payload.price : 0;
    const mrp = payload.mrp ? payload.mrp : price;
    const stockStatus = payload.stock_status || 'In stock';
    const imageUrl = payload.image || payload.image_url || payload.img_url || payload.product_image || payload.thumbnail || '';
    const productUrl = payload.url || payload.product_url || payload.link || '';

    // Format currency
    const formattedPrice = `₹${price.toLocaleString('en-IN')}`;
    const formattedMrp = mrp > price ? `₹${mrp.toLocaleString('en-IN')}` : '';
    const savings = mrp > price ? mrp - price : 0;
    const formattedSavings = savings > 0 ? `Save ₹${savings.toLocaleString('en-IN')}` : '';
    
    // Discount percentage
    const discountPercent = mrp > price ? Math.round(((mrp - price) / mrp) * 100) : 0;

    // Doc preview
    const searchDoc = payload.search_document || payload.technical_document || '';
    const docCleaned = searchDoc.replace(/&amp;/g, '&').replace(/\n/g, ' • ');

    const vectorScore = item.score !== undefined ? item.score.toFixed(3) : '-';
    const rerankScore = item.rerank_score !== undefined ? item.rerank_score.toFixed(2) : '-';

    // Image element rendering with referrer policy & safe error handling
    const imageHtml = imageUrl
      ? `<div class="product-image-wrapper">
           <img src="${escapeHtml(imageUrl)}" alt="${escapeHtml(title)}" class="product-image-img" loading="lazy" referrerpolicy="no-referrer" onerror="handleImageError(this)" />
         </div>`
      : `<div class="card-image-placeholder">
           <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
             <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
           </svg>
         </div>`;

    // Title link rendering
    const titleHtml = productUrl
      ? `<a href="${escapeHtml(productUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(title)}</a>`
      : escapeHtml(title);

    return `
      <div class="product-card">
        <div class="card-top">
          ${imageHtml}
          <div class="card-badges">
            <span class="stock-tag">${stockStatus}</span>
            ${discountPercent > 0 ? `<span class="discount-tag">-${discountPercent}% OFF</span>` : ''}
          </div>
        </div>

        <div class="card-body">
          <div class="card-category">${escapeHtml(category)}</div>
          <h3 class="card-title">${titleHtml}</h3>
          <div class="card-sku">SKU: ${escapeHtml(sku)}</div>

          <div class="card-pricing">
            <span class="price-current">${formattedPrice}</span>
            ${formattedMrp ? `<span class="price-mrp">${formattedMrp}</span>` : ''}
            ${formattedSavings ? `<span class="price-savings">${formattedSavings}</span>` : ''}
          </div>

          ${docCleaned ? `<div class="card-doc-preview">${escapeHtml(docCleaned)}</div>` : ''}

          <div class="card-footer">
            <div class="score-group">
              <span class="score-pill" title="Vector Similarity Score">
                Sim: <strong>${vectorScore}</strong>
              </span>
              <span class="score-pill" title="Business Re-ranker Score">
                Rank: <strong>${rerankScore}</strong>
              </span>
            </div>

            <div class="card-actions">
              ${productUrl ? `
                <a href="${escapeHtml(productUrl)}" target="_blank" rel="noopener noreferrer" class="view-url-btn">
                  <span>View Product</span>
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                    <polyline points="15 3 21 3 21 9"></polyline>
                    <line x1="10" y1="14" x2="21" y2="3"></line>
                  </svg>
                </a>
              ` : ''}
              <button class="action-btn" onclick="toggleTechDetails('${sku}')">Specs</button>
            </div>
          </div>

          <div id="tech-${sku}" class="tech-details">
            <strong>Technical Details:</strong><br/>
            ${escapeHtml(payload.technical_document || 'N/A')}<br/><br/>
            ${productUrl ? `<strong>Product URL:</strong> <a href="${escapeHtml(productUrl)}" target="_blank" style="color:var(--secondary);">${escapeHtml(productUrl)}</a><br/><br/>` : ''}
            <strong>Keywords:</strong> ${(payload.keywords || []).join(', ')}
          </div>
        </div>
      </div>
    `;
  }).join('');
}

function toggleTechDetails(sku) {
  const elem = document.getElementById(`tech-${sku}`);
  if (elem) {
    elem.classList.toggle('visible');
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function handleImageError(imgElem) {
  const wrapper = imgElem.closest('.product-image-wrapper');
  if (wrapper) {
    wrapper.className = 'card-image-placeholder';
    wrapper.innerHTML = `<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>`;
  }
}
