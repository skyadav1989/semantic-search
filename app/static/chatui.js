const state = {
  busy: false,
  products: [],
};

const els = {};

document.addEventListener('DOMContentLoaded', () => {
  els.messages = document.getElementById('messages');
  els.form = document.getElementById('chat-form');
  els.input = document.getElementById('chat-input');
  els.send = document.getElementById('send-btn');
  els.session = document.getElementById('session-id');
  els.clear = document.getElementById('clear-session-btn');
  els.newSession = document.getElementById('new-session-btn');
  els.products = document.getElementById('products');
  els.productCount = document.getElementById('product-count');
  els.filters = document.getElementById('filters');
  els.followups = document.getElementById('followups');

  const savedSession = window.localStorage.getItem('semantic_chat_session_id');
  if (savedSession) els.session.value = savedSession;

  els.session.addEventListener('input', () => {
    window.localStorage.setItem('semantic_chat_session_id', cleanSessionId());
  });

  els.form.addEventListener('submit', (event) => {
    event.preventDefault();
    submitMessage(els.input.value.trim());
  });

  els.clear.addEventListener('click', clearSession);
  els.newSession.addEventListener('click', startNewSession);

  renderWelcome();
  renderProducts([]);
});

function cleanSessionId() {
  const value = (els.session.value || '').trim();
  if (value) return value;
  els.session.value = 'session-' + Date.now();
  return els.session.value;
}

function renderWelcome() {
  els.messages.innerHTML = '';
  addMessage('assistant', 'Hi. Tell me what you are shopping for, your budget, or the feature you care about. I will keep the conversation context in this session.');
}

async function submitMessage(query) {
  if (!query || state.busy) return;

  const sessionId = cleanSessionId();
  window.localStorage.setItem('semantic_chat_session_id', sessionId);

  setBusy(true);
  clearFollowups();
  addMessage('user', query);
  els.input.value = '';
  const loadingId = addMessage('assistant', 'Searching and preparing recommendations...', true);

  try {
    const response = await fetch('/chat/v2', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId,
        query,
        limit: 10,
      }),
    });

    if (!response.ok) {
      const detail = await safeJson(response);
      throw new Error(detail.detail || `Request failed with HTTP ${response.status}`);
    }

    const data = await response.json();
    replaceMessage(loadingId, data.answer || 'I found results, but no answer text was returned.');
    renderProducts(data.products || []);
    renderFilters(data.filters || {});
    renderFollowups(data.follow_up_questions || []);
  } catch (error) {
    replaceMessage(loadingId, `Sorry, the chat request failed: ${error.message}`);
    renderProducts([]);
    renderFilters({});
  } finally {
    setBusy(false);
    els.input.focus();
  }
}

function addMessage(role, content, isStatus = false) {
  const id = 'msg-' + Date.now() + '-' + Math.random().toString(16).slice(2);
  const row = document.createElement('div');
  row.className = `message ${role}`;
  row.dataset.messageId = id;

  const avatar = document.createElement('div');
  avatar.className = 'avatar';
  avatar.textContent = role === 'user' ? 'You' : 'AI';

  const bubble = document.createElement('div');
  bubble.className = isStatus ? 'bubble status-line' : 'bubble';
  bubble.textContent = content;

  row.append(avatar, bubble);
  els.messages.appendChild(row);
  scrollMessages();
  return id;
}

function replaceMessage(id, content) {
  const row = els.messages.querySelector(`[data-message-id="${id}"]`);
  if (!row) return;
  const bubble = row.querySelector('.bubble');
  bubble.classList.remove('status-line');
  bubble.textContent = content;
  scrollMessages();
}

function scrollMessages() {
  els.messages.scrollTop = els.messages.scrollHeight;
}

function renderProducts(products) {
  state.products = products;
  els.productCount.textContent = `${products.length} ${products.length === 1 ? 'product' : 'products'}`;

  if (!products.length) {
    els.products.innerHTML = '<div class="empty-state">Product matches will appear here after each chat response.</div>';
    return;
  }

  els.products.innerHTML = '';
  products.forEach((product) => {
    els.products.appendChild(productCard(product));
  });
}

function productCard(product) {
  const card = document.createElement('article');
  card.className = 'product-card';

  const art = document.createElement('div');
  art.className = 'product-art';
  if (product.image) {
    const img = document.createElement('img');
    img.src = product.image;
    img.alt = product.title || product.sku || 'Product image';
    img.loading = 'lazy';
    img.referrerPolicy = 'no-referrer';
    img.onerror = () => {
      art.textContent = 'Item';
    };
    art.appendChild(img);
  } else {
    art.textContent = 'Item';
  }

  const body = document.createElement('div');
  body.className = 'product-body';

  const title = document.createElement('h3');
  title.className = 'product-title';
  if (product.url) {
    const link = document.createElement('a');
    link.href = product.url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.textContent = product.title || product.sku || 'Product';
    title.appendChild(link);
  } else {
    title.textContent = product.title || product.sku || 'Product';
  }

  const meta = document.createElement('div');
  meta.className = 'product-meta';
  [product.sku, product.brand, product.category, product.subcategory].filter(Boolean).forEach((value) => {
    const span = document.createElement('span');
    span.textContent = value;
    meta.appendChild(span);
  });

  body.append(title, meta);

  if (product.price !== null && product.price !== undefined) {
    const price = document.createElement('span');
    price.className = 'product-price';
    price.textContent = formatCurrency(product.price);
    body.appendChild(price);
  }

  card.append(art, body);
  return card;
}

function renderFilters(filters) {
  els.filters.innerHTML = '';
  const entries = Object.entries(filters);
  if (!entries.length) return;

  entries.forEach(([key, value]) => {
    const pill = document.createElement('span');
    pill.className = 'filter-pill';
    pill.textContent = `${humanize(key)}: ${formatFilterValue(value)}`;
    els.filters.appendChild(pill);
  });
}

function renderFollowups(questions) {
  els.followups.innerHTML = '';
  questions.filter(Boolean).slice(0, 4).forEach((question) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = question;
    button.addEventListener('click', () => submitMessage(question));
    els.followups.appendChild(button);
  });
}

function clearFollowups() {
  els.followups.innerHTML = '';
}

async function clearSession() {
  const sessionId = cleanSessionId();
  setBusy(true);
  try {
    await fetch(`/chat/v2/session/${encodeURIComponent(sessionId)}`, { method: 'DELETE' });
  } catch (error) {
    console.warn('Unable to clear session', error);
  } finally {
    setBusy(false);
    renderWelcome();
    renderProducts([]);
    renderFilters({});
    clearFollowups();
    els.input.focus();
  }
}

function startNewSession() {
  els.session.value = 'session-' + Date.now();
  window.localStorage.setItem('semantic_chat_session_id', els.session.value);
  renderWelcome();
  renderProducts([]);
  renderFilters({});
  clearFollowups();
  els.input.focus();
}

function setBusy(busy) {
  state.busy = busy;
  els.send.disabled = busy;
  els.input.disabled = busy;
  els.send.querySelector('span').textContent = busy ? 'Sending' : 'Send';
}

async function safeJson(response) {
  try {
    return await response.json();
  } catch (_) {
    return {};
  }
}

function formatCurrency(value) {
  const number = Number(value);
  if (!Number.isFinite(number)) return String(value);
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(number);
}

function formatFilterValue(value) {
  if (value && typeof value === 'object' && !Array.isArray(value)) {
    return Object.entries(value)
      .map(([op, amount]) => `${op} ${typeof amount === 'number' ? formatCurrency(amount) : amount}`)
      .join(', ');
  }
  if (Array.isArray(value)) return value.join(', ');
  return String(value);
}

function humanize(value) {
  return String(value).replace(/_/g, ' ');
}
