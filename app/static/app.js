// App state
let currentQuery = '';
let debounceTimer = null;
const productsMap = new Map();

document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('search-input');
  
  // Input clear button toggle
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const clearBtn = document.getElementById('clear-btn');
      if (clearBtn) clearBtn.style.display = e.target.value ? 'flex' : 'none';
    });
  }

  // Keyboard shortcut ESC to close PDP modal
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closePDP();
    }
  });

  // Handle browser Back / Forward buttons
  window.addEventListener('popstate', (event) => {
    if (event.state && event.state.pdp) {
      openPDP(event.state.pdp, false);
    } else if (window.location.pathname.startsWith('/pdp/')) {
      const skuFromUrl = decodeURIComponent(window.location.pathname.replace('/pdp/', ''));
      if (skuFromUrl) openPDP(skuFromUrl, false);
    } else {
      closePDP(false);
    }
  });

  // Check if page was loaded directly with PDP URL /pdp/{sku}
  const path = window.location.pathname;
  if (path.startsWith('/pdp/')) {
    const directSku = decodeURIComponent(path.replace('/pdp/', ''));
    if (directSku) {
      openPDP(directSku, false);
    }
  }

  // Auto trigger default search
  performSearch();
});

function setQuery(queryText) {
  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.value = queryText;
    const clearBtn = document.getElementById('clear-btn');
    if (clearBtn) clearBtn.style.display = 'flex';
  }
  performSearch();
}

function clearSearch() {
  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.value = '';
    const clearBtn = document.getElementById('clear-btn');
    if (clearBtn) clearBtn.style.display = 'none';
    searchInput.focus();
  }
}

async function performSearch() {
  const searchInput = document.getElementById('search-input');
  const query = searchInput ? searchInput.value.trim() : '';
  if (!query) return;

  const gridContainer = document.getElementById('products-grid');
  const insightsPanel = document.getElementById('insights-panel');

  // Show loading skeleton
  if (gridContainer) {
    gridContainer.innerHTML = `
      <div class="loading-state">
        <div class="spinner"></div>
        <p style="color: var(--text-muted); font-size: 0.95rem;">Retrieving semantic vector embeddings & re-ranking...</p>
      </div>
    `;
  }

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
    if (gridContainer) {
      gridContainer.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon">⚠️</div>
          <h3 style="margin-bottom: 8px; color: #f87171;">Search Request Failed</h3>
          <p style="color: var(--text-dim); font-size: 0.9rem;">${error.message || 'Unable to connect to search service'}</p>
        </div>
      `;
    }
    if (insightsPanel) insightsPanel.classList.remove('visible');
  }
}

function renderInsights(data) {
  const insightsPanel = document.getElementById('insights-panel');
  if (!insightsPanel) return;

  const intentBadge = document.getElementById('intent-badge');
  const countStat = document.getElementById('count-stat');
  const latencyBadge = document.getElementById('latency-badge');
  const filtersContainer = document.getElementById('filters-container');
  const termsContainer = document.getElementById('terms-container');
  const normalizedQuery = document.getElementById('normalized-query');

  insightsPanel.classList.add('visible');

  // Intent badge
  const intent = data.intent || 'BUY';
  if (intentBadge) {
    intentBadge.textContent = intent;
    intentBadge.className = `intent-badge intent-${intent}`;
  }

  // Count & Timing
  if (countStat) countStat.textContent = data.count || (data.results ? data.results.length : 0);
  const elapsedMs = (data.elapsed_ms !== undefined) ? data.elapsed_ms.toFixed(1) : '0.0';
  if (latencyBadge) latencyBadge.textContent = `⚡ ${elapsedMs} ms`;

  // Normalized Query
  if (normalizedQuery) normalizedQuery.textContent = data.normalized_query || data.query || '-';

  // Filters
  if (filtersContainer) {
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
  }

  // Expanded terms
  if (termsContainer) {
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
}

function renderResults(results) {
  const gridContainer = document.getElementById('products-grid');
  if (!gridContainer) return;

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

  // Cache items in productsMap
  results.forEach(item => {
    const payload = item.payload || {};
    const sku = payload.sku || item.id;
    if (sku) {
      productsMap.set(sku, item);
    }
  });

  gridContainer.innerHTML = results.map(item => renderCardHtml(item, false)).join('');
}

// Single Card Renderer HTML Generator
function renderCardHtml(item, isRecommendation = false) {
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
  const discountPercent = mrp > price ? Math.round(((mrp - price) / mrp) * 100) : 0;

  // Search doc preview
  const searchDoc = payload.search_document || payload.technical_document || '';
  const docCleaned = searchDoc.replace(/&amp;/g, '&').replace(/\n/g, ' • ');

  // Score calculations
  const vectorScore = item.score !== undefined ? item.score.toFixed(3) : '-';
  const rerankScore = item.rerank_score !== undefined ? item.rerank_score.toFixed(2) : '-';
  const recScoreObj = item.recommendation_score || {};
  const recFinalScore = recScoreObj.final !== undefined ? recScoreObj.final.toFixed(3) : (item.score !== undefined ? item.score.toFixed(3) : '-');

  // Image HTML
  const imageHtml = imageUrl
    ? `<div class="product-image-wrapper">
         <img src="${escapeHtml(imageUrl)}" alt="${escapeHtml(title)}" class="product-image-img" loading="lazy" referrerpolicy="no-referrer" onerror="handleImageError(this)" />
       </div>`
    : `<div class="card-image-placeholder">
         <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
           <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
         </svg>
       </div>`;

  const cardClass = isRecommendation ? 'product-card rec-card' : 'product-card';

  return `
    <div class="${cardClass}">
      <div class="card-image-header">
        ${imageHtml}
        <div class="card-badges">
          <span class="stock-tag">${stockStatus}</span>
          ${discountPercent > 0 ? `<span class="discount-tag">-${discountPercent}% OFF</span>` : ''}
        </div>
      </div>

      <div class="card-body">
        <div class="card-category">${escapeHtml(category)}</div>
        <h3 class="card-title" title="${escapeHtml(title)}">
          ${productUrl 
            ? `<a href="${escapeHtml(productUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(title)}</a>` 
            : escapeHtml(title)}
        </h3>
        <div class="card-sku">SKU: ${escapeHtml(sku)}</div>

        <div class="card-pricing">
          <span class="price-current">${formattedPrice}</span>
          ${formattedMrp ? `<span class="price-mrp">${formattedMrp}</span>` : ''}
          ${formattedSavings ? `<span class="price-savings">${formattedSavings}</span>` : ''}
        </div>

        ${(!isRecommendation && docCleaned) ? `<div class="card-doc-preview">${escapeHtml(docCleaned)}</div>` : ''}

        <div class="card-footer">
          <div class="score-group">
            ${isRecommendation ? `
              <span class="score-pill rec-score-pill" title="Recommendation Score">
                Score: <strong>${recFinalScore}</strong>
              </span>
            ` : `
              <span class="score-pill" title="Vector Similarity Score">
                Sim: <strong>${vectorScore}</strong>
              </span>
              <span class="score-pill" title="Business Re-ranker Score">
                Rank: <strong>${rerankScore}</strong>
              </span>
            `}
          </div>

          <div class="card-actions">
            ${productUrl ? `
              <a href="${escapeHtml(productUrl)}" target="_blank" rel="noopener noreferrer" class="view-url-btn" title="View on original store page">
                <span>View Product</span>
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                  <polyline points="15 3 21 3 21 9"></polyline>
                  <line x1="10" y1="14" x2="21" y2="3"></line>
                </svg>
              </a>
            ` : ''}
            <button class="pdp-btn" onclick="openPDP('${escapeHtml(sku)}')" title="Open Product Page & Recommendations">
              <span>⚡ View PDP</span>
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="9" y1="9" x2="15" y2="9"></line>
                <line x1="9" y1="13" x2="15" y2="13"></line>
              </svg>
            </button>
            ${!isRecommendation ? `<button class="action-btn" onclick="toggleTechDetails('${sku}')">Specs</button>` : ''}
          </div>
        </div>

        ${!isRecommendation ? `
          <div id="tech-${sku}" class="tech-details">
            <strong>Technical Details:</strong><br/>
            ${escapeHtml(payload.technical_document || 'N/A')}<br/><br/>
            ${productUrl ? `<strong>Product URL:</strong> <a href="${escapeHtml(productUrl)}" target="_blank" style="color:var(--secondary);">${escapeHtml(productUrl)}</a><br/><br/>` : ''}
            <strong>Keywords:</strong> ${(payload.keywords || []).join(', ')}
          </div>
        ` : ''}
      </div>
    </div>
  `;
}

// ---------------------------------------------------------
// PDP (Product Details Page) & Recommendations Logic
// ---------------------------------------------------------

async function openPDP(sku, updateHistory = true) {
  const modal = document.getElementById('pdp-modal');
  const heroContainer = document.getElementById('pdp-product-content');
  if (!modal || !heroContainer) return;

  // Update browser URL route to /pdp/{sku}
  if (updateHistory && window.location.pathname !== `/pdp/${sku}`) {
    history.pushState({ pdp: sku }, '', `/pdp/${encodeURIComponent(sku)}`);
  }

  // Retrieve cached item or fetch via PDP API
  let item = productsMap.get(sku);
  if (!item) {
    try {
      const pdpRes = await fetch(`/api/pdp/${encodeURIComponent(sku)}`);
      if (pdpRes.ok) {
        const pdpData = await pdpRes.json();
        if (pdpData.product) {
          item = { id: sku, payload: pdpData.product };
          productsMap.set(sku, item);
        }
      }
    } catch (e) {
      console.warn("Failed to load direct PDP endpoint:", e);
    }
  }

  if (!item) {
    item = {
      id: sku,
      payload: { sku: sku, title: sku, category: 'Product', price: 0 }
    };
  }

  const payload = item.payload || {};
  const title = payload.title || sku;
  const category = payload.category || 'General';
  const subcategory = payload.subcategory || '';
  const price = payload.price ? payload.price : 0;
  const mrp = payload.mrp ? payload.mrp : price;
  const stockStatus = payload.stock_status || 'In stock';
  const imageUrl = payload.image || payload.image_url || payload.img_url || payload.product_image || payload.thumbnail || '';
  const productUrl = payload.url || payload.product_url || payload.link || '';
  const formattedPrice = `₹${price.toLocaleString('en-IN')}`;
  const formattedMrp = mrp > price ? `₹${mrp.toLocaleString('en-IN')}` : '';
  const savings = mrp > price ? mrp - price : 0;
  const formattedSavings = savings > 0 ? `Save ₹${savings.toLocaleString('en-IN')}` : '';
  const discountPercent = mrp > price ? Math.round(((mrp - price) / mrp) * 100) : 0;
  const searchDoc = payload.search_document || payload.technical_document || '';

  // Render Product Page Layout inside PDP Modal
  heroContainer.innerHTML = `
    <div class="pdp-hero-card">
      <div class="pdp-breadcrumbs">
        <span>Store</span> &gt;
        <span>${escapeHtml(category)}</span>
        ${subcategory ? `&gt; <span>${escapeHtml(subcategory)}</span>` : ''}
        &gt; <span class="current">${escapeHtml(title)}</span>
      </div>

      <!-- Left Column: Gallery & Trust Badges -->
      <div class="pdp-gallery-column">
        <div class="pdp-hero-image-box">
          ${imageUrl 
            ? `<img src="${escapeHtml(imageUrl)}" alt="${escapeHtml(title)}" referrerpolicy="no-referrer" onerror="handleImageError(this)" />` 
            : `<div class="card-image-placeholder"><svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div>`}
          <div class="card-badges">
            <span class="stock-tag">${escapeHtml(stockStatus)}</span>
            ${discountPercent > 0 ? `<span class="discount-tag">-${discountPercent}% OFF</span>` : ''}
          </div>
        </div>

        <div class="pdp-trust-badges">
          <div class="trust-badge-pill"><span>⚡</span> Energy Saver</div>
          <div class="trust-badge-pill"><span>🛡️</span> 2Y Warranty</div>
          <div class="trust-badge-pill"><span>🚚</span> Free Express</div>
          <div class="trust-badge-pill"><span>🔄</span> Easy Returns</div>
        </div>
      </div>

      <!-- Right Column: Product Page Details -->
      <div class="pdp-details-column">
        <div class="pdp-category-bar">
          <span class="pdp-category-tag">${escapeHtml(category)} ${subcategory ? `• ${escapeHtml(subcategory)}` : ''}</span>
          <span class="pdp-sku-tag">SKU: ${escapeHtml(sku)}</span>
        </div>

        <h1 class="pdp-hero-title">${escapeHtml(title)}</h1>

        <div class="pdp-rating-row">
          <span class="stars-rating">★★★★★</span>
          <strong>4.8 / 5.0</strong>
          <span class="rating-count">• (128 Customer Reviews)</span>
        </div>

        <div class="pdp-hero-price-panel">
          <span class="pdp-price-selling">${formattedPrice}</span>
          ${formattedMrp ? `<span class="pdp-price-mrp">${formattedMrp}</span>` : ''}
          ${formattedSavings ? `<span class="pdp-price-save">${formattedSavings}</span>` : ''}
        </div>

        <!-- Key Product Attributes -->
        <div class="pdp-attributes-grid">
          <div class="attr-card">
            <span class="attr-key">Category</span>
            <span class="attr-val">${escapeHtml(category)}</span>
          </div>
          ${subcategory ? `
            <div class="attr-card">
              <span class="attr-key">Subcategory</span>
              <span class="attr-val">${escapeHtml(subcategory)}</span>
            </div>
          ` : ''}
          <div class="attr-card">
            <span class="attr-key">Stock Status</span>
            <span class="attr-val">${escapeHtml(stockStatus)}</span>
          </div>
          <div class="attr-card">
            <span class="attr-key">Selling Price</span>
            <span class="attr-val">${formattedPrice}</span>
          </div>
        </div>

        ${searchDoc ? `
          <div class="pdp-specs-box">
            <strong>Product Overview & Technical Description</strong>
            ${escapeHtml(searchDoc)}
          </div>
        ` : ''}

        <div class="pdp-hero-actions">
          ${productUrl ? `
            <a href="${escapeHtml(productUrl)}" target="_blank" rel="noopener noreferrer" class="view-url-btn" style="padding: 10px 22px; font-size: 0.92rem;">
              <span>View Product on Store</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                <polyline points="15 3 21 3 21 9"></polyline>
                <line x1="10" y1="14" x2="21" y2="3"></line>
              </svg>
            </a>
          ` : ''}
          <button class="btn-secondary-action" onclick="copySkuToClipboard('${escapeHtml(sku)}')">
            <span>📋 Copy SKU</span>
          </button>
        </div>
      </div>
    </div>
  `;

  // Show Modal Overlay
  modal.style.display = 'flex';
  setTimeout(() => modal.classList.add('active'), 10);
  document.body.style.overflow = 'hidden';

  // Scroll PDP body to top
  const modalBody = modal.querySelector('.pdp-modal-body');
  if (modalBody) modalBody.scrollTop = 0;

  // Set Loading skeletons for the 3 recommendation sections
  setRecGridLoading('rec-similar-grid', 'Similar');
  setRecGridLoading('rec-trending-grid', 'Trending');
  setRecGridLoading('rec-complementary-grid', 'Complementary');

  // Fetch recommendations in parallel
  fetchRecommendations(sku);
}

function setRecGridLoading(gridId, typeLabel) {
  const grid = document.getElementById(gridId);
  if (grid) {
    grid.innerHTML = `
      <div class="rec-loading-placeholder">
        <div class="spinner" style="width:24px; height:24px; margin:0;"></div>
        <span>Loading ${typeLabel} recommendations...</span>
      </div>
    `;
  }
}

async function fetchRecommendations(sku) {
  const endpoints = [
    { key: 'similar', gridId: 'rec-similar-grid', url: `/recommendations/similar/${encodeURIComponent(sku)}` },
    { key: 'trending', gridId: 'rec-trending-grid', url: `/recommendations/trending/${encodeURIComponent(sku)}` },
    { key: 'complementary', gridId: 'rec-complementary-grid', url: `/recommendations/complementary/${encodeURIComponent(sku)}` }
  ];

  await Promise.all(endpoints.map(async ({ key, gridId, url }) => {
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      renderRecommendationGrid(gridId, data);
    } catch (err) {
      console.warn(`Failed to fetch ${key} recommendations:`, err);
      const grid = document.getElementById(gridId);
      if (grid) {
        grid.innerHTML = `<div style="padding:12px; color:var(--text-dim); font-size:0.85rem;">No ${key} recommendations found for this item.</div>`;
      }
    }
  }));
}

function renderRecommendationGrid(gridId, items) {
  const grid = document.getElementById(gridId);
  if (!grid) return;

  if (!items || items.length === 0) {
    grid.innerHTML = `<div style="padding:12px; color:var(--text-dim); font-size:0.85rem;">No items available.</div>`;
    return;
  }

  // Cache recommended products into productsMap
  items.forEach(item => {
    const payload = item.payload || {};
    const sku = payload.sku || item.id;
    if (sku) {
      productsMap.set(sku, item);
    }
  });

  grid.innerHTML = items.map(item => renderCardHtml(item, true)).join('');
}

function closePDP(updateHistory = true) {
  const modal = document.getElementById('pdp-modal');
  if (modal) {
    modal.classList.remove('active');
    setTimeout(() => {
      modal.style.display = 'none';
    }, 300);
  }
  document.body.style.overflow = '';
  if (updateHistory && window.location.pathname.startsWith('/pdp/')) {
    history.pushState(null, '', '/');
  }
}

function handleModalBackdropClick(event) {
  if (event.target && event.target.id === 'pdp-modal') {
    closePDP();
  }
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
  const wrapper = imgElem.closest('.product-image-wrapper') || imgElem.closest('.pdp-hero-image-box');
  if (wrapper) {
    wrapper.className = 'card-image-placeholder';
    wrapper.innerHTML = `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>`;
  }
}

function copySkuToClipboard(sku) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(sku).then(() => {
      alert(`SKU '${sku}' copied to clipboard!`);
    }).catch(err => {
      console.warn("Could not copy SKU:", err);
    });
  }
}

