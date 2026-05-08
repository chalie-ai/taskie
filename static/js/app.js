// ── SVG Icon helpers ──
const I = {
  search:   '<svg class="svg-icon" width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="7" cy="7" r="4.5"/><path d="M10.5 10.5l3 3"/></svg>',
  plus:     '<svg class="svg-icon" width="14" height="14" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M9 3v12M3 9h12"/></svg>',
  board:    '<svg class="svg-icon" width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><rect x="2" y="2.5" width="3.5" height="11" rx="1"/><rect x="6.5" y="2.5" width="3.5" height="7" rx="1"/><rect x="11" y="2.5" width="3" height="9" rx="1"/></svg>',
  list:     '<svg class="svg-icon" width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M3 4h10M3 8h10M3 12h10"/></svg>',
  filter:   '<svg class="svg-icon" width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M2.5 3.5h11l-4 5v4l-3-1.5V8.5l-4-5z"/></svg>',
  comment:  '<svg class="svg-icon" width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M3 4a1 1 0 011-1h8a1 1 0 011 1v6a1 1 0 01-1 1H7l-3 2.5V11H4a1 1 0 01-1-1V4z"/></svg>',
  sparkle:  '<svg class="svg-icon" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M8 2.5L9 6l3.5 1L9 8l-1 3.5L7 8 3.5 7 7 6 8 2.5z"/></svg>',
  more:     '<svg class="svg-icon" width="13" height="13" viewBox="0 0 16 16" fill="currentColor" stroke="none"><circle cx="3.5" cy="8" r=".75"/><circle cx="8" cy="8" r=".75"/><circle cx="12.5" cy="8" r=".75"/></svg>',
  close:    '<svg class="svg-icon" width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M4 4l8 8M12 4l-8 8"/></svg>',
  chevDown: '<svg class="svg-icon" width="11" height="11" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M4 6l4 4 4-4"/></svg>',
  chevRight:'<svg class="svg-icon" width="11" height="11" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M6 4l4 4-4 4"/></svg>',
  attach:   '<svg class="svg-icon" width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M11 5L6.5 9.5a2 2 0 102.8 2.8l5-5a3.5 3.5 0 10-5-5L4.5 7.5"/></svg>',
  pencil:   '<svg class="svg-icon" width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M11 2l3 3-8 8H3v-3l8-8z"/></svg>',
  folder:   '<svg class="svg-icon" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M2 4.5a1 1 0 011-1h3.5l1 1.5H13a1 1 0 011 1v6a1 1 0 01-1 1H3a1 1 0 01-1-1v-7.5z"/></svg>',
  pr:       '<svg class="svg-icon" width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="4" cy="4" r="1.5"/><circle cx="4" cy="12" r="1.5"/><circle cx="12" cy="12" r="1.5"/><path d="M4 5.5v5"/><path d="M5.5 4H10a2 2 0 012 2v5"/></svg>',
  trash:    '<svg class="svg-icon" width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M3 4h10M6.5 4V2.5h3V4M5 4l.5 9h5l.5-9M7 6.5v5M9 6.5v5"/></svg>',
};

const STATUSES = ['backlog','todo','progress','review','done','cancel'];
const STATUS_LABELS = { backlog:'Backlog', todo:'Todo', progress:'In Progress', review:'In Review', done:'Done', cancel:'Cancelled' };
const STATUS_DOT = { backlog:'dot-backlog', todo:'dot-todo', progress:'dot-progress', review:'dot-review', done:'dot-done', cancel:'dot-cancel' };
const STATUS_COLOR_CLASS = { backlog:'status-color-backlog', todo:'status-color-todo', progress:'status-color-progress', review:'status-color-review', done:'status-color-done', cancel:'status-color-cancel' };

const TYPE_LETTER = { bug:'B', feature:'F', chore:'C' };
const TYPE_CLASS = { bug:'bug', feature:'feature', chore:'chore' };

const PRIO_LEVELS = { urgent:3, high:3, medium:2, low:1, none:0 };

// ── State ──
const AUTH = {
  get() { try { return JSON.parse(localStorage.getItem('tt_auth')||'null'); } catch { return null; } },
  set(data) { localStorage.setItem('tt_auth', JSON.stringify(data)); },
  clear() { localStorage.removeItem('tt_auth'); },
  token() { const a = this.get(); return a?.access_token || null; },
  user() { const a = this.get(); return a?.user || null; },
};

// jQuery AJAX prefilter to auto-attach Bearer token
$.ajaxPrefilter(function(opts) {
  const t = AUTH.token();
  if (t) opts.headers = { ...(opts.headers||{}), 'Authorization': 'Bearer '+t };
});

const App = {
  view: 'cycle',
  mode: 'board',
  activeCycleId: null,
  activeProjectId: null,
  activeTicketId: null,
  tickets: [],
  projects: [],
  cycles: [],
  users: [],
  ticketDetail: null,
  filters: { status: null, priority: null, assignee_id: null, type: null },

  async init() {
    if (!AUTH.token()) { this.showLogin(); return; }
    try {
      if (localStorage.getItem('tt_sidebar_collapsed') === '1') {
        $('.sidebar').addClass('collapsed');
        $('#sb-collapse-btn').html('<svg class="svg-icon" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M6 4l4 4-4 4"/></svg>');
      }
      await this.loadAll();
      this.render();
      this.bindKeys();
      this.checkHash();
      $(window).on('hashchange', () => this.checkHash());
      this.updateSidebarUser();
    } catch (e) {
      console.error('App.init error:', e);
      if (e && e.status === 401) { AUTH.clear(); this.showLogin(); }
      else { $('#content-area').html(`<div style="padding:40px;text-align:center;color:var(--p-high)"><h3>Something went wrong</h3><pre style="font-size:11px;margin:12px 0;text-align:left">${this.esc(e?.responseJSON?.error || e?.statusText || e?.message || String(e))}</pre><button class="btn btn-primary" onclick="App.logout()">Sign out and try again</button></div>`); }
    }
  },

  async loadAll() {
    const [cycles, projects, tickets, users] = await Promise.all([
      $.get('/api/cycles'),
      $.get('/api/projects'),
      $.get('/api/tickets'),
      $.get('/api/users'),
    ]);
    this.cycles = cycles; this.projects = projects; this.tickets = tickets; this.users = users;
    if (cycles.length > 0) this.activeCycleId = cycles.find(c => c.active)?.id || cycles[0].id;
  },

  updateSidebarUser() {
    const u = AUTH.user();
    if (u) {
      const init = (u.name||'?')[0].toUpperCase();
      $('#sb-avatar').text(init);
      $('#sb-user-name').text(u.name);
    }
  },

  showLogin() {
    $('body').html(`<div class="login-overlay">
      <div class="login-card">
        <h2>Sign in</h2>
        <div class="sub">Enter your credentials to continue</div>
        <div class="login-error" id="login-error">Invalid email or password</div>
        <div class="field"><label>Email</label><input type="email" id="login-email" placeholder="admin@tasktracker.local" autofocus></div>
        <div class="field"><label>Password</label><input type="password" id="login-password" placeholder="Enter password"></div>
        <button class="btn btn-primary" style="width:100%;justify-content:center;padding:8px" onclick="App.doLogin()">Sign in</button>
      </div>
    </div>`);
    $('#login-password').on('keydown', function(e) { if (e.key==='Enter') App.doLogin(); });
  },

  async doLogin() {
    const email = $('#login-email').val().trim();
    const password = $('#login-password').val();
    if (!email || !password) return;
    try {
      const resp = await $.ajax({ url: '/api/auth/token', method: 'POST', contentType: 'application/json', data: JSON.stringify({ email, password }) });
      AUTH.set(resp);
      location.reload();
    } catch (e) {
      $('#login-error').show();
    }
  },

  checkHash() {
    const hash = window.location.hash;
    const m = hash.match(/^#\/ticket\/(\d+)$/);
    if (m) {
      const tid = parseInt(m[1]);
      if (tid && !$('.panel').length) this.openTicket(tid);
    }
  },

  filtered() {
    let list = this.tickets;
    const cid = this.activeCycleId;
    if (this.view === 'project' && this.activeProjectId) list = list.filter(t => t.project_id == this.activeProjectId);
    else if (cid) list = list.filter(t => t.cycle_id == cid);
    const f = this.filters;
    if (f.status) list = list.filter(t => t.status === f.status);
    if (f.priority) list = list.filter(t => t.priority === f.priority);
    if (f.type) list = list.filter(t => t.type === f.type);
    if (f.assignee_id) list = list.filter(t => t.assignee_id == f.assignee_id);
    return list;
  },

  // ── Render ──
  render() {
    this.renderSidebar();
    const isTicketView = ['cycle','project'].includes(this.view);
    $('#filterbar').toggle(isTicketView);
    if (this.view === 'projects') {
      this.renderProjectsPage();
    } else if (this.view === 'users') {
      if (AUTH.user()?.role !== 'admin') { this.view = 'cycle'; this.render(); return; }
      this.renderUsersPage();
    } else if (this.view === 'profile') {
      this.renderProfilePage();
    } else {
      this.renderCrumbs();
      $('#content-area').html(this.mode === 'board' ? this.boardHTML() : this.listHTML());
      this.bindBoardEvents();
    }
    $('#filter-summary').text(this.filtered().length + ' tickets');
  },

  renderSidebar() {
    // Cycle card
    const c = this.cycles.find(c => c.id === this.activeCycleId);
    if (c) {
      const pct = c.total ? Math.round((c.done / c.total) * 100) : 0;
      $('#sb-cycle-card').html(`
        <div class="sb-cycle-label"><span>Active cycle</span></div>
        <div class="sb-cycle-name">${c.title} · ${c.description}</div>
        <div class="sb-cycle-progress"><div class="sb-cycle-progress-fill" style="width:${pct}%"></div></div>
        <div class="sb-cycle-stats"><span>${c.done} of ${c.total} done</span><span>${pct}%</span></div>
      `);
    }

    // Counts
    const isAdmin = AUTH.user()?.role === 'admin';
    $('#sb-people-section').toggle(isAdmin);
    if (isAdmin) $('#cnt-users').text(this.users.length);

    // Filter chip styling
    const f = this.filters;
    const labels = { status:'Status', priority:'Priority', assignee:'Assignee', type:'Type' };
    const setChip = (name, val, displayVal) => {
      const $b = $(`#fc-${name}`);
      $b.toggleClass('applied', !!val);
      let chevHTML = '<svg class="svg-icon" width="11" height="11" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M4 6l4 4 4-4"/></svg>';
      $b.html(val ? `${displayVal} ${chevHTML}` : `${labels[name]} ${chevHTML}`);
    };
    const statusLabel = f.status ? STATUS_LABELS[f.status] : '';
    const prioLabel = f.priority ? f.priority.charAt(0).toUpperCase()+f.priority.slice(1) : '';
    const assigneeLabel = f.assignee_id ? (this.users.find(u => u.id == f.assignee_id)?.name || '') : '';
    const typeLabel = f.type ? f.type.charAt(0).toUpperCase()+f.type.slice(1) : '';
    setChip('status', f.status, statusLabel);
    setChip('priority', f.priority, prioLabel);
    setChip('assignee', f.assignee_id, assigneeLabel);
    setChip('type', f.type, typeLabel);

    // Active state on nav items
    $('.sb-item.view-trigger').removeClass('active');
    $(`.sb-item.view-trigger[data-view="${this.view}"]`).addClass('active');
    if (this.view === 'project') $(`.sb-item.project-item[data-id="${this.activeProjectId}"]`).addClass('active');

    // Project list
    $('#sb-project-list').html(this.projects.map(p => {
      const count = this.tickets.filter(t => t.project_id === p.id && t.status !== 'done' && t.status !== 'cancel').length;
      const act = (this.view === 'project' && this.activeProjectId === p.id) ? ' active' : '';
      return `<button class="sb-item project-item${act}" data-id="${p.id}" onclick="App.selectProject(${p.id})">
        <span class="sb-dot" style="background:${p.color}"></span><span class="sb-label">${p.name}</span><span class="sb-count">${count}</span>
      </button>`;
    }));

    // Cycle list
    $('#sb-cycle-list').html(this.cycles.map(c => {
      const act = (this.view === 'cycle' && this.activeCycleId === c.id) ? ' active' : '';
      const nowBadge = c.active ? '<span style="margin-left:auto;font-size:10px;color:var(--accent-text);background:var(--accent-soft);padding:1px 5px;border-radius:3px;font-weight:600;letter-spacing:0.04em;text-transform:uppercase">now</span>' : '';
      return `<button class="sb-item${act}" onclick="App.setCycle(${c.id})">
        <span class="sb-icon">${I.sparkle}</span><span class="sb-label">${c.title}</span>${nowBadge}
      </button>`;
    }));
  },

  renderCrumbs() {
    if (this.view === 'projects' || this.view === 'users') return;
    let html = '';
    if (this.view === 'project' && this.activeProjectId) {
      const p = this.projects.find(p => p.id == this.activeProjectId);
      html = `<span class="crumb" onclick="App.showProjectsView()">Projects</span><span class="crumb-sep">${I.chevRight}</span><span class="crumb active"><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${p?.color};margin-right:6px"></span>${p?.name}</span>`;
    } else {
      const labels = { inbox:'Board', cycle: this.cycles.find(c => c.id === this.activeCycleId)?.title || '' };
      html = `<span class="crumb active">${labels[this.view] || 'Board'}</span>`;
    }
    const c = this.cycles.find(c => c.id === this.activeCycleId);
    if (c && this.view !== 'projects') {
      html += `<span style="color:var(--text-faint);font-size:12px;margin-left:4px">· ${c.description} · ${this.filtered().length} tickets</span>`;
    }
    $('#crumbs').html(html);
  },

  // ── Board ──
  boardHTML() {
    const filtered = this.filtered();
    const boardStatuses = STATUSES.filter(s => s !== 'cancel');
    let cols = '';
    boardStatuses.forEach(s => {
      const items = s === 'done'
        ? filtered.filter(t => t.status === 'done' || t.status === 'cancel')
                  .sort((a, b) => (a.status === 'cancel') - (b.status === 'cancel'))
        : filtered.filter(t => t.status === s);
      cols += `<div class="col">
        <div class="col-head">
          <span class="dot ${STATUS_DOT[s]}"></span><span>${STATUS_LABELS[s]}</span><span class="count">${items.length}</span>
          <span class="col-actions">
            <button class="col-add" data-status="${s}" title="Add">+</button>
            <button class="col-add">…</button>
          </span>
        </div>
        <div class="col-body" data-status="${s}">
          ${items.length === 0 ? '<div class="card-empty">No tickets</div>' : ''}
          ${items.map(t => this.cardHTML(t)).join('')}
        </div>
      </div>`;
    });
    return `<div class="board"><div class="board-cols">${cols}</div></div>`;
  },

  cardHTML(t) {
    const isCancel = t.status === 'cancel';
    const isDone = t.status === 'done' || isCancel;
    const cardCls = isCancel ? 'cancel' : (isDone ? 'done' : '');
    const proj = this.projects.find(p => p.id == t.project_id);
    const prioCls = t.priority === 'urgent' || t.priority === 'high' ? 'high' : t.priority === 'medium' ? 'medium' : t.priority === 'low' ? 'low' : 'none';
    const lvls = PRIO_LEVELS[t.priority] || 0;
    let prioHTML;
    if (t.priority === 'urgent') {
      prioHTML = `<span class="card-prio urgent" title="Urgent"><svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="10" height="10" rx="2"/><path d="M8 6v3M8 11h.01" stroke-width="1.6"/></svg></span>`;
    } else {
      prioHTML = `<span class="card-prio ${prioCls}" title="${t.priority}">
        <span class="prio-bars"><span class="b1"></span><span class="b2"></span><span class="b3"></span></span>
      </span>`;
    }
    return `<div class="card ${cardCls}" data-ticket-id="${t.id}" onclick="App.openTicket(${t.id})">
      <div class="card-top">
        <span class="card-id">${t.display_id}</span>
        <span class="card-type ${TYPE_CLASS[t.type] || 'feature'}">${TYPE_LETTER[t.type] || 'F'}</span>
        ${isCancel ? '<span class="card-cancel-tag">Cancelled</span>' : ''}
        ${prioHTML}
      </div>
      <div class="card-title">${this.esc(t.name)}</div>
      <div class="card-meta">
        <span class="meta-tag"><span class="tag-dot" style="background:${proj?.color}"></span>${proj?.name || ''}</span>
        ${t.comment_count > 0 ? `<span>${I.comment} ${t.comment_count}</span>` : ''}
        <span class="meta-spacer"></span>
        ${t.assignee_name ? `<span class="sb-avatar" style="width:18px;height:18px;font-size:8px;background:${t.assignee_avatar||'var(--text-muted)'}">${t.assignee_name.slice(0,2).toUpperCase()}</span>` : (t.assignee ? `<span class="sb-avatar" style="width:18px;height:18px;font-size:8px;background:var(--text-muted)">${t.assignee.toUpperCase().slice(0,2)}</span>` : '')}
      </div>
    </div>`;
  },

  // ── List ──
  listHTML() {
    const filtered = this.filtered();
    let groups = '';
    STATUSES.forEach(s => {
      const rows = filtered.filter(t => t.status === s);
      if (!rows.length) return;
      groups += `<div class="list-group">
        <div class="list-group-head"><span class="dot ${STATUS_DOT[s]}"></span><span>${STATUS_LABELS[s]}</span><span class="count">${rows.length}</span></div>
        ${rows.map(t => this.listRowHTML(t)).join('')}
      </div>`;
    });
    return `<div class="list-view">${groups}</div>`;
  },

  listRowHTML(t) {
    const isDone = t.status === 'done' || t.status === 'cancel';
    const proj = this.projects.find(p => p.id == t.project_id);
    const prioCls = t.priority === 'urgent' || t.priority === 'high' ? 'high' : t.priority === 'medium' ? 'medium' : 'low';
    let prioHTML;
    if (t.priority === 'urgent') {
      prioHTML = `<span class="card-prio urgent" title="Urgent"><svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="var(--p-high)" stroke-width="1.5"><rect x="3" y="3" width="10" height="10" rx="2"/><path d="M8 6v3M8 11h.01" stroke-width="1.6"/></svg></span>`;
    } else {
      prioHTML = `<span class="card-prio ${prioCls}"><span class="prio-bars"><span class="b1"></span><span class="b2"></span><span class="b3"></span></span></span>`;
    }
    return `<div class="list-row ${isDone ? 'done' : ''}" onclick="App.openTicket(${t.id})">
      <span class="row-prio">${prioHTML}</span>
      <span class="card-type ${TYPE_CLASS[t.type] || 'feature'}">${TYPE_LETTER[t.type] || 'F'}</span>
      <span class="row-id">${t.display_id}</span>
      <span class="row-title">${this.esc(t.name)}</span>
      <span class="row-proj"><span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:${proj?.color};margin-right:6px"></span>${proj?.name||''}</span>
      <span class="row-comments">${t.comment_count > 0 ? `${I.comment} ${t.comment_count}` : ''}</span>
      <span class="row-date">${this.relDate(t.updated_at)}</span>
      <span>${t.assignee_name ? `<span class="sb-avatar" style="width:20px;height:20px;font-size:9px;background:${t.assignee_avatar||'var(--text-muted)'}">${t.assignee_name.slice(0,2).toUpperCase()}</span>` : (t.assignee ? `<span class="sb-avatar" style="width:20px;height:20px;font-size:9px;background:var(--text-muted)">${t.assignee.toUpperCase().slice(0,2)}</span>` : '')}</span>
    </div>`;
  },

  // ── Projects page ──
  renderProjectsPage() {
    const all = this.tickets;
    $('#crumbs').html('');
    let cards = this.projects.map(p => {
      const items = all.filter(t => t.project_id === p.id);
      const open = items.filter(t => t.status !== 'done' && t.status !== 'cancel').length;
      const progress = items.filter(t => t.status === 'progress').length;
      const init = p.name.slice(0,2);
      return `<div class="project-card">
        <div class="project-card-head">
          <div class="project-mark" style="background:${p.color}">${init}</div>
          <div style="flex:1;min-width:0">
            <div class="project-name">${this.esc(p.name)}</div>
            <div class="project-path">${this.esc(p.location||'')}</div>
          </div>
          <button class="btn-icon" onclick="event.stopPropagation();App.editProject(${p.id})">${I.pencil}</button>
        </div>
        <div class="project-desc">${this.esc(p.description||'')}</div>
        <div>
          <div class="project-instructions-label">${I.sparkle} Agent instructions</div>
          <div class="project-instructions">${p.agent_instructions||'No instructions yet'}</div>
        </div>
        <div class="project-stats">
          <span><strong>${items.length}</strong> tickets</span>
          <span><strong>${open}</strong> open</span>
          <span><strong>${progress}</strong> in progress</span>
        </div>
      </div>`;
    });
    cards.push(`<div class="project-card" style="display:grid;place-items:center;min-height:200px;border-style:dashed;cursor:pointer;color:var(--text-muted)" onclick="App.showNewProjectModal()">
      <div style="text-align:center">${I.plus}<div style="margin-top:6px;font-weight:500">New project</div><div style="font-size:11.5px;color:var(--text-faint);margin-top:2px">Connect a repo or create blank</div></div>
    </div>`);
    $('#content-area').html(`<div class="projects-page">
      <div class="page-header"><div><h1>Projects</h1><div class="sub">${this.projects.length} projects · ${this.tickets.length} tickets total</div></div><div style="display:flex;gap:6px"><button class="btn btn-secondary">${I.filter} Filter</button><button class="btn btn-primary" onclick="App.showNewProjectModal()">+ New project</button></div></div>
      <div class="projects-grid">${cards.join('')}</div>
    </div>`);
  },

  // ── Ticket panel ──
  openTicket(id) {
    if (this._opening) return;
    this._opening = true;
    const target = `/ticket/${id}`;
    if (window.location.hash !== '#' + target) window.location.hash = target;
    $.get(`/api/tickets/${id}`, t => {
      this.ticketDetail = t;
      this.showPanel(t);
      this._opening = false;
    }).fail(() => { this._opening = false; });
  },

  copyTicketLink(id) {
    const url = window.location.origin + window.location.pathname + '#/ticket/' + id;
    navigator.clipboard.writeText(url).then(() => {
      // brief visual feedback could go here
    }).catch(() => {
      prompt('Copy this link:', url);
    });
  },

  showPanel(t) {
    const proj = this.projects.find(p => p.id == t.project_id);
    const statusOpts = STATUSES.map(s => `<option value="${s}" ${t.status===s?'selected':''}>${STATUS_LABELS[s]}</option>`).join('');
    const prioOpts = ['urgent','high','medium','low','none'].map(p => `<option value="${p}" ${t.priority===p?'selected':''}>${p.charAt(0).toUpperCase()+p.slice(1)}</option>`).join('');
    const projOpts = this.projects.map(p => `<option value="${p.id}" ${t.project_id===p.id?'selected':''}>${p.name}</option>`).join('');
    const cycleOpts = this.cycles.map(c => `<option value="${c.id}" ${t.cycle_id===c.id?'selected':''}>${c.title}</option>`).join('');
    const userOpts = this.users.map(u => `<option value="${u.id}" ${t.assignee_id===u.id?'selected':''}>${this.esc(u.name)}</option>`).join('');

    const commentsHTML = (t.comments||[]).map(c => {
      const isAgent = c.author_type === 'agent';
      const initials = c.author_name.split(' ').map(w=>w[0]).join('').slice(0,2).toUpperCase();
      return `<div class="comment">
        <div class="comment-avatar ${isAgent?'agent':''}" style="${!isAgent?'background:var(--text-muted)':''}">${isAgent ? I.sparkle : initials}</div>
        <div class="comment-body">
          <div class="comment-head">
            <span class="comment-author">${this.esc(c.author_name)}${isAgent?'<span class="agent-tag">agent</span>':''}</span>
            <span class="comment-time">${this.relDate(c.created_at)}</span>
          </div>
          <div class="comment-text">${this.md(c.body)}</div>
          ${c.pr_link ? `<div class="comment-pr">${I.pr} <span>${this.esc(c.pr_link.title||'')}</span><span class="pr-status ${c.pr_link.status}">${c.pr_link.status}</span></div>` : ''}
        </div>
      </div>`;
    }).join('');

    const rels = t.relationships || [];
    const REL_TYPE_LABELS = { related:'Related to', blocks:'Blocks', blocked_by:'Blocked by' };
    const relsHTML = rels.map(r => `
      <div class="rel-item">
        <span class="rel-type-badge rel-type-${r.relationship_type}">${REL_TYPE_LABELS[r.relationship_type]||r.relationship_type}</span>
        <span class="rel-ticket-link">${this.esc(r.related_ticket_display_id)}</span>
        <span class="rel-ticket-name" onclick="App.closePanel();App.openTicket(${r.related_ticket_id})">${this.esc(r.related_ticket_name)}</span>
        <span class="rel-status-dot ${STATUS_DOT[r.related_ticket_status]}"></span>
        <button class="rel-remove" onclick="App.removeRelationship(${t.id},${r.id})" title="Remove">${I.close}</button>
      </div>
    `).join('');

    const panel = $(`
      <div class="panel-overlay" onclick="App.closePanel()"></div>
      <div class="panel">
        <div class="panel-head">
          <span class="pid">${t.display_id}</span>
          <span style="color:var(--text-faint)">·</span>
          <span style="display:inline-flex;align-items:center;gap:6px;font-size:12px;color:var(--text-muted)">
            <span class="sb-dot" style="background:${proj?.color};width:7px;height:7px;border-radius:50%"></span>${proj?.name}
          </span>
          <div class="panel-head-actions">
            <button class="btn-icon" title="Copy link" onclick="App.copyTicketLink(${t.id})">${I.attach}</button>
            <button class="btn-icon" title="Delete ticket" onclick="App.deleteTicket(${t.id}, '${this.esc(t.display_id)}')" style="color:var(--p-high)">${I.trash}</button>
            <button class="btn-icon" onclick="App.closePanel()" title="Close (Esc)">${I.close}</button>
          </div>
        </div>
        <div class="panel-body">
          <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:var(--text-muted)">
            <span class="card-type ${TYPE_CLASS[t.type]||'feature'}">${TYPE_LETTER[t.type]||'F'}</span>
            <span style="text-transform:capitalize">${t.type}</span>
            <span style="color:var(--text-faint)">·</span>
            <span>opened ${this.relDate(t.created_at)}</span>
            <span style="color:var(--text-faint)">·</span>
            <span>updated ${this.relDate(t.updated_at)}</span>
          </div>
          <h2 class="panel-title" contenteditable="true" id="panel-title-edit" onblur="App.saveTitle(${t.id}, this.innerText)">${this.esc(t.name)}</h2>
          <div class="panel-props">
            <div class="panel-prop-label">Status</div>
            <div class="panel-prop-value"><select class="prop-pill panel-patch" data-field="status">${statusOpts}</select></div>
            <div class="panel-prop-label">Priority</div>
            <div class="panel-prop-value"><select class="prop-pill panel-patch" data-field="priority"><option value="">—</option>${prioOpts}</select></div>
            <div class="panel-prop-label">Assignee</div>
            <div class="panel-prop-value"><select class="prop-pill panel-patch" data-field="assignee_id"><option value="">Unassigned</option>${userOpts}</select></div>
            <div class="panel-prop-label">Due date</div>
            <div class="panel-prop-value"><input type="date" class="prop-pill panel-patch-input" data-field="due_date" value="${t.due_date||''}" style="border:none;outline:none;background:transparent;font-size:12px;font-family:inherit"/></div>
            <div class="panel-prop-label">Project</div>
            <div class="panel-prop-value"><select class="prop-pill panel-patch" data-field="project_id"><option value="">—</option>${projOpts}</select></div>
            <div class="panel-prop-label">Cycle</div>
            <div class="panel-prop-value"><select class="prop-pill panel-patch" data-field="cycle_id">${cycleOpts}</select></div>
          </div>
          <div class="panel-section">
            <div class="panel-section-title">Description</div>
            <div id="panel-desc-wrap" style="position:relative">
              ${t.description
                ? `<div id="panel-desc" class="panel-desc" ondblclick="App.editDescription(${t.id})">${this.md(t.description)}</div>
                   <button class="btn-icon panel-desc-edit" title="Edit description" onclick="App.editDescription(${t.id})">${I.pencil}</button>`
                : `<div id="panel-desc" class="panel-desc empty" onclick="App.editDescription(${t.id})">No description yet — click to edit.</div>`
              }
            </div>
          </div>
          <div class="panel-section">
            <div class="panel-section-title rel-section-head">
              <span>Relationships · ${rels.length}</span>
              <button class="btn btn-ghost" onclick="App.showAddRelationship(${t.id})">+ Add</button>
            </div>
            <div id="panel-rels">${relsHTML || '<div class="rel-empty">No linked tickets yet.</div>'}</div>
            <div id="panel-add-rel" style="display:none"></div>
          </div>
          <div class="panel-section">
            <div class="panel-section-title">Activity · ${(t.comments||[]).length}</div>
            <div class="comments">${commentsHTML || '<div style="color:var(--text-faint);font-size:12.5px;padding:8px 0">No activity yet.</div>'}</div>
            <div class="composer">
              <textarea id="comment-input" placeholder="Leave a comment…  ⌘↵ to send" onkeydown="if(event.key==='Enter'&&(event.metaKey||event.ctrlKey)){event.preventDefault();App.submitComment(${t.id})}"></textarea>
              <div class="composer-actions">
                <span class="hint">Markdown supported · <span class="kbd">⌘</span><span class="kbd">↵</span> to send</span>
                <button class="btn btn-primary" onclick="App.submitComment(${t.id})">Comment</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    `);
    $('body').append(panel);
    $('.panel-patch').on('change', function() {
      const field = $(this).data('field');
      const val = $(this).val();
      if (val !== '') App.patchTicket(t.id, field, val);
    });
    $('.panel-patch-input').on('blur', function() {
      const field = $(this).data('field');
      const val = $(this).val();
      App.patchTicket(t.id, field, val);
    });
  },

  closePanel() {
    $('.panel, .panel-overlay').remove();
    window.location.hash = '';
  },

  async patchTicket(id, field, val) {
    const data = {};
    data[field] = val;
    try {
      const updated = await $.ajax({ url: `/api/tickets/${id}`, method: 'PATCH', contentType: 'application/json', data: JSON.stringify(data) });
      // Update local state
      const idx = this.tickets.findIndex(t => t.id == id);
      if (idx >= 0) this.tickets[idx] = updated;
      this.ticketDetail = updated;
      this.render();
    } catch (e) { console.error(e); }
  },

  saveTitle(id, title) {
    if (title.trim()) this.patchTicket(id, 'name', title.trim());
  },

  async submitComment(ticketId) {
    const body = $('#comment-input').val().trim();
    if (!body) return;
    try {
      await $.ajax({ url: `/api/tickets/${ticketId}/comments`, method: 'POST', contentType: 'application/json', data: JSON.stringify({ body, author_type: 'human', author_name: 'Dylan' }) });
      const t = await $.get(`/api/tickets/${ticketId}`);
      // Update local
      const idx = this.tickets.findIndex(t => t.id == ticketId);
      if (idx >= 0) this.tickets[idx] = t;
      this.closePanel();
      this.showPanel(t);
      this.render();
    } catch (e) { console.error(e); }
  },

  // ── Relationships ──

  showAddRelationship(ticketId) {
    const types = [
      { val: 'related', label: 'Related to' },
      { val: 'blocks', label: 'Blocks' },
      { val: 'blocked_by', label: 'Blocked by' },
    ];
    const typeOpts = types.map(t => `<option value="${t.val}">${t.label}</option>`).join('');
    $('#panel-add-rel').html(`
      <div class="add-rel-form">
        <input id="rel-search" placeholder="Search tickets…" autofocus>
        <select id="rel-type">${typeOpts}</select>
        <button class="btn btn-primary btn-sm" onclick="App.addRelationship(${ticketId})">Link</button>
        <button class="btn btn-ghost btn-sm" onclick="$('#panel-add-rel').hide()">Cancel</button>
      </div>
      <div class="rel-search-results" id="rel-results"></div>
    `).show();
    const searchInput = $('#rel-search');
    let debounce = null;
    searchInput.on('input', function() {
      const q = $(this).val();
      clearTimeout(debounce);
      if (!q.trim()) { $('#rel-results').html(''); return; }
      debounce = setTimeout(() => {
        $.get('/api/tickets', { search: q }, function(tickets) {
          const filtered = tickets.filter(t => t.id != ticketId).slice(0, 8);
          $('#rel-results').html(filtered.map(t => `
            <div class="rel-search-item"
                 onclick="$('#rel-search').val('${App.esc(t.display_id)} — ${App.esc(t.name)}').data('selected-id',${t.id});$('#rel-results').html('')">
              <span class="rel-ticket-link">${App.esc(t.display_id)}</span>
              <span class="rel-ticket-name">${App.esc(t.name)}</span>
              <span class="rel-status-dot ${STATUS_DOT[t.status]}"></span>
            </div>
          `).join(''));
        });
      }, 200);
    });
    searchInput.focus();
  },

  async addRelationship(ticketId) {
    const searchInput = $('#rel-search');
    const selectedId = searchInput.data('selected-id');
    if (!selectedId) return;
    const type = $('#rel-type').val();
    try {
      await $.ajax({
        url: `/api/tickets/${ticketId}/relationships`, method: 'POST', contentType: 'application/json',
        data: JSON.stringify({ related_ticket_id: selectedId, relationship_type: type }),
      });
      const t = await $.get(`/api/tickets/${ticketId}`);
      const idx = this.tickets.findIndex(t => t.id == ticketId);
      if (idx >= 0) this.tickets[idx] = t;
      this.closePanel();
      this.showPanel(t);
      this.render();
    } catch (e) { console.error(e); alert('Error: ' + (e.responseJSON?.error || e.statusText)); }
  },

  async removeRelationship(ticketId, relId) {
    if (!confirm('Remove this relationship?')) return;
    try {
      await $.ajax({ url: `/api/tickets/${ticketId}/relationships/${relId}`, method: 'DELETE' });
      const t = await $.get(`/api/tickets/${ticketId}`);
      const idx = this.tickets.findIndex(t => t.id == ticketId);
      if (idx >= 0) this.tickets[idx] = t;
      this.closePanel();
      this.showPanel(t);
      this.render();
    } catch (e) { console.error(e); }
  },

  // ── New ticket ──
  showNewTicketModal() {
    const projOpts = this.projects.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
    const cycleOpts = this.cycles.map(c => `<option value="${c.id}" ${c.id===this.activeCycleId?'selected':''}>${c.title}</option>`).join('');
    const userOpts = this.users.map(u => `<option value="${u.id}">${this.esc(u.name)}</option>`).join('');
    const modal = $(`
      <div class="cmd-overlay" style="z-index:1500" id="new-ticket-overlay" onclick="if(event.target===this) $('#new-ticket-overlay').remove()">
        <div class="cmd" style="padding:20px">
          <h3 style="font-weight:600;margin-bottom:16px">New Ticket</h3>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Name</label><input class="form-control" id="nt-name" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></div>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Description</label><textarea class="form-control" id="nt-desc" rows="3" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></textarea></div>
          <div style="display:flex;gap:10px;margin-bottom:14px">
            <div style="flex:1"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Type</label><select class="form-select" id="nt-type" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius)"><option value="bug">Bug</option><option value="feature" selected>Feature</option><option value="chore">Chore</option></select></div>
            <div style="flex:1"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Priority</label><select class="form-select" id="nt-priority" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius)"><option value="urgent">Urgent</option><option value="high">High</option><option value="medium" selected>Medium</option><option value="low">Low</option><option value="none">None</option></select></div>
          </div>
          <div style="display:flex;gap:10px;margin-bottom:14px">
            <div style="flex:1"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Status</label><select class="form-select" id="nt-status" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius)">${STATUSES.map(s => `<option value="${s}" ${s==='todo'?'selected':''}>${STATUS_LABELS[s]}</option>`).join('')}</select></div>
            <div style="flex:1"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Project</label><select class="form-select" id="nt-project" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius)">${projOpts}</select></div>
          </div>
          <div style="display:flex;gap:10px;margin-bottom:14px">
            <div style="flex:1"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Cycle</label><select class="form-select" id="nt-cycle" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius)">${cycleOpts}</select></div>
            <div style="flex:1"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Due date</label><input type="date" class="form-control" id="nt-due" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></div>
          </div>
          <div style="display:flex;gap:10px;margin-bottom:14px">
            <div style="flex:1"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Assignee</label><select class="form-select" id="nt-assignee" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius)"><option value="">Unassigned</option>${userOpts}</select></div>
          </div>
          <div style="display:flex;justify-content:flex-end;gap:8px">
            <button class="btn btn-secondary" onclick="$('#new-ticket-overlay').remove()">Cancel</button>
            <button class="btn btn-primary" onclick="App.createTicket()">Create Ticket</button>
          </div>
        </div>
      </div>
    `);
    $('body').append(modal);
    $('#nt-name').focus();
  },

  async createTicket() {
    const name = $('#nt-name').val().trim();
    if (!name) return;
    const assigneeId = $('#nt-assignee').val();
    try {
      const t = await $.ajax({
        url: '/api/tickets', method: 'POST', contentType: 'application/json',
        data: JSON.stringify({
          name, description: $('#nt-desc').val(),
          type: $('#nt-type').val(), priority: $('#nt-priority').val(),
          status: $('#nt-status').val(), project_id: parseInt($('#nt-project').val()),
          cycle_id: parseInt($('#nt-cycle').val()),
          assignee_id: assigneeId ? parseInt(assigneeId) : null,
          due_date: $('#nt-due').val() || null,
        }),
      });
      this.tickets.unshift(t);
      $('#new-ticket-overlay').remove();
      this.render();
    } catch (e) { console.error(e); alert('Error creating ticket: ' + (e.responseJSON?.error || e.statusText)); }
  },

  showNewProjectModal() {
    const modal = $(`
      <div class="cmd-overlay" style="z-index:1500" id="new-project-overlay" onclick="if(event.target===this) $('#new-project-overlay').remove()">
        <div class="cmd" style="padding:20px">
          <h3 style="font-weight:600;margin-bottom:16px">New Project</h3>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Name</label><input class="form-control" id="np-name" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></div>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Location</label><input class="form-control" id="np-location" placeholder="Path on machine" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></div>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Description</label><textarea class="form-control" id="np-desc" rows="2" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></textarea></div>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Agent Instructions</label><textarea class="form-control" id="np-instructions" rows="3" placeholder="Instructions for AI agents working on this project" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px;font-family:var(--font-mono)"></textarea></div>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Color</label><input type="color" class="form-control" id="np-color" value="#6B6B6B" style="width:60px;height:32px;padding:2px;border:1px solid var(--border);border-radius:var(--radius);cursor:pointer"></div>
          <div style="display:flex;justify-content:flex-end;gap:8px">
            <button class="btn btn-secondary" onclick="$('#new-project-overlay').remove()">Cancel</button>
            <button class="btn btn-primary" onclick="App.createProject()">Create Project</button>
          </div>
        </div>
      </div>
    `);
    $('body').append(modal);
    $('#np-name').focus();
  },

  async createProject() {
    const name = $('#np-name').val().trim();
    if (!name) return;
    try {
      const p = await $.ajax({
        url: '/api/projects', method: 'POST', contentType: 'application/json',
        data: JSON.stringify({
          name,
          location: $('#np-location').val().trim(),
          description: $('#np-desc').val().trim(),
          agent_instructions: $('#np-instructions').val().trim(),
          color: $('#np-color').val(),
        }),
      });
      this.projects.push(p);
      $('#new-project-overlay').remove();
      this.render();
    } catch (e) { console.error(e); alert('Error creating project: ' + (e.responseJSON?.error || e.statusText)); }
  },

  showNewCycleModal() {
    const modal = $(`
      <div class="cmd-overlay" style="z-index:1500" id="new-cycle-overlay" onclick="if(event.target===this) $('#new-cycle-overlay').remove()">
        <div class="cmd" style="padding:20px">
          <h3 style="font-weight:600;margin-bottom:16px">New Cycle</h3>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Title</label><input class="form-control" id="nc-title" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></div>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Description</label><textarea class="form-control" id="nc-desc" rows="2" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></textarea></div>
          <div style="display:flex;gap:10px;margin-bottom:14px">
            <div style="flex:1"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Status</label><select class="form-select" id="nc-status" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius)"><option value="pending">Pending</option><option value="in_progress">In Progress</option><option value="completed">Completed</option></select></div>
          </div>
          <div style="display:flex;gap:10px;margin-bottom:14px">
            <div style="flex:1"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Start date</label><input type="date" class="form-control" id="nc-start" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></div>
            <div style="flex:1"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">End date</label><input type="date" class="form-control" id="nc-end" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></div>
          </div>
          <div style="display:flex;justify-content:flex-end;gap:8px">
            <button class="btn btn-secondary" onclick="$('#new-cycle-overlay').remove()">Cancel</button>
            <button class="btn btn-primary" onclick="App.createCycle()">Create Cycle</button>
          </div>
        </div>
      </div>
    `);
    $('body').append(modal);
    $('#nc-title').focus();
  },

  async createCycle() {
    const title = $('#nc-title').val().trim();
    if (!title) return;
    try {
      const data = {
        title,
        description: $('#nc-desc').val().trim(),
        status: $('#nc-status').val(),
        start_date: $('#nc-start').val() || null,
        end_date: $('#nc-end').val() || null,
      };
      const c = await $.ajax({ url: '/api/cycles', method: 'POST', contentType: 'application/json', data: JSON.stringify(data) });
      this.cycles.push(c);
      $('#new-cycle-overlay').remove();
      this.render();
    } catch (e) { console.error(e); alert('Error creating cycle: ' + (e.responseJSON?.error || e.statusText)); }
  },

  editProject(id) {
    const p = this.projects.find(p => p.id == id);
    if (!p) return;
    const modal = $(`
      <div class="cmd-overlay" style="z-index:1500" id="edit-project-overlay" onclick="if(event.target===this) $('#edit-project-overlay').remove()">
        <div class="cmd" style="padding:20px">
          <h3 style="font-weight:600;margin-bottom:16px">Edit Project — ${this.esc(p.name)}</h3>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Name</label><input class="form-control" id="ep-name" value="${this.esc(p.name)}" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></div>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Location</label><input class="form-control" id="ep-location" value="${this.esc(p.location||'')}" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></div>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Description</label><textarea class="form-control" id="ep-desc" rows="3" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px">${this.esc(p.description||'')}</textarea></div>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Agent Instructions</label><textarea class="form-control" id="ep-instructions" rows="4" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px;font-family:var(--font-mono)">${this.esc(p.agent_instructions||'')}</textarea></div>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Git Repo URL</label><input class="form-control" id="ep-git" value="${this.esc(p.git_repo_url||'')}" placeholder="https://github.com/org/repo" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></div>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Color</label><input type="color" class="form-control" id="ep-color" value="${this.esc(p.color||'')}" style="width:60px;height:32px;padding:2px;border:1px solid var(--border);border-radius:var(--radius);cursor:pointer"></div>
          <div style="display:flex;justify-content:flex-end;gap:8px">
            <button class="btn btn-secondary" onclick="$('#edit-project-overlay').remove()">Cancel</button>
            <button class="btn btn-primary" onclick="App.submitEditProject(${id})">Save Changes</button>
          </div>
        </div>
      </div>
    `);
    $('body').append(modal);
    $('#ep-name').focus();
  },

  async submitEditProject(id) {
    try {
      const data = {
        name: $('#ep-name').val().trim(),
        location: $('#ep-location').val().trim(),
        description: $('#ep-desc').val().trim(),
        agent_instructions: $('#ep-instructions').val().trim(),
        git_repo_url: $('#ep-git').val().trim(),
        color: $('#ep-color').val(),
      };
      if (!data.name) { alert('Name is required'); return; }
      const updated = await $.ajax({ url: `/api/projects/${id}`, method: 'PUT', contentType: 'application/json', data: JSON.stringify(data) });
      const idx = this.projects.findIndex(p => p.id == id);
      if (idx >= 0) this.projects[idx] = updated;
      $('#edit-project-overlay').remove();
      this.render();
    } catch (e) { console.error(e); alert('Error updating project'); }
  },

  // ── Users page ──
  renderUsersPage() {
    const rows = this.users.map(u => {
      const initials = u.name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
      const roleBadge = u.role === 'admin' ? '<span style="background:oklch(0.94 0.06 295);color:oklch(0.45 0.16 295);padding:1px 6px;border-radius:3px;font-size:10.5px;font-weight:600;text-transform:uppercase;letter-spacing:0.04em">admin</span>' :
                        u.role === 'member' ? '<span style="background:oklch(0.95 0.06 150);color:oklch(0.4 0.14 150);padding:1px 6px;border-radius:3px;font-size:10.5px;font-weight:600;text-transform:uppercase;letter-spacing:0.04em">member</span>' :
                        '<span style="background:var(--bg-sunken);color:var(--text-muted);padding:1px 6px;border-radius:3px;font-size:10.5px;font-weight:600;text-transform:uppercase;letter-spacing:0.04em">viewer</span>';
      return `<tr>
        <td style="width:36px"><div class="sb-avatar" style="background:${u.avatar_color};width:28px;height:28px;font-size:10px">${initials}</div></td>
        <td><div style="font-weight:600;font-size:13px">${this.esc(u.name)}</div><div style="font-size:11.5px;color:var(--text-muted)">${this.esc(u.email)}</div></td>
        <td>${roleBadge}</td>
        <td style="color:var(--text-faint);font-size:11.5px">joined ${this.relDate(u.created_at)}</td>
        <td style="text-align:right">
          <button class="btn-icon" onclick="App.editUser(${u.id})" title="Edit">${I.pencil}</button>
          ${u.role !== 'admin' ? `<button class="btn-icon" onclick="App.deleteUser(${u.id})" title="Remove" style="color:var(--p-high)">${I.close}</button>` : ''}
        </td>
      </tr>`;
    }).join('');

    $('#content-area').html(`<div class="projects-page">
      <div class="page-header"><div><h1>Users</h1><div class="sub">${this.users.length} users · admins, members, and viewers</div></div><button class="btn btn-primary" onclick="App.showNewUserModal()">+ New user</button></div>
      <div style="margin-top:18px;background:var(--bg-elev);border:1px solid var(--border);border-radius:var(--radius-lg);overflow:hidden">
        <table style="width:100%;border-collapse:collapse">
          <tbody>${rows || '<tr><td colspan="5" style="padding:40px;text-align:center;color:var(--text-faint)">No users yet</td></tr>'}</tbody>
        </table>
      </div>
      <div style="margin-top:18px;padding:14px 16px;background:var(--bg-sunken);border:1px solid var(--border);border-radius:var(--radius-lg)">
        <div style="font-weight:600;font-size:13px;margin-bottom:6px">Permissions</div>
        <div style="display:flex;gap:24px;font-size:12.5px">
          <div><span style="color:var(--text-muted)">Admin —</span> full access, manage users, projects, cycles</div>
          <div><span style="color:var(--text-muted)">Member —</span> create and edit tickets, comment, link PRs</div>
          <div><span style="color:var(--text-muted)">Viewer —</span> read-only access to tickets and projects</div>
        </div>
      </div>
    </div>`);
  },

  async renderProfilePage() {
    const u = AUTH.user();
    let fullUser = {};
    try { fullUser = await $.get(`/api/users/${u.id}`); } catch(e) {}
    const token = fullUser.agent_token || '';
    $('#crumbs').html('');
    $('#content-area').html(`<div class="profile-page">
      <div class="page-header"><div><h1>Profile</h1><div class="sub">Your account details</div></div></div>
      <div class="profile-section">
        <h3>Account</h3>
        <table style="width:100%">
          <tr><td style="padding:6px 12px 6px 0;color:var(--text-muted);font-size:12px;width:80px">Name</td><td style="font-weight:500">${this.esc(fullUser.name||'')}</td></tr>
          <tr><td style="padding:6px 12px 6px 0;color:var(--text-muted);font-size:12px">Surname</td><td style="font-weight:500">${this.esc(fullUser.surname||'')}</td></tr>
          <tr><td style="padding:6px 12px 6px 0;color:var(--text-muted);font-size:12px">Email</td><td style="font-weight:500">${this.esc(fullUser.email||'')}</td></tr>
          <tr><td style="padding:6px 12px 6px 0;color:var(--text-muted);font-size:12px">Role</td><td><span style="display:inline-block;padding:1px 6px;border-radius:3px;font-size:10.5px;font-weight:600;text-transform:uppercase;letter-spacing:0.04em;background:${fullUser.role==='admin'?'oklch(0.94 0.06 295)':'oklch(0.95 0.06 150)'};color:${fullUser.role==='admin'?'oklch(0.45 0.16 295)':'oklch(0.4 0.14 150)'}">${fullUser.role||'member'}</span></td></tr>
        </table>
      </div>
      <div class="profile-section">
        <h3>Agent Token</h3>
        <p style="font-size:12.5px;color:var(--text-muted);margin-bottom:8px">Use this token to authenticate MCP tools. Treat it like a password — never commit it.</p>
        <div class="token-box"><span id="agent-token-display">${token}</span><button class="btn btn-secondary btn-sm" onclick="App.copyToken()">Copy</button></div>
      </div>
      <div class="profile-section">
        <h3>Change Password</h3>
        <div class="field"><label>Current password</label><input type="password" id="cp-old" style="width:100%;padding:7px 10px;border:1px solid var(--border);border-radius:var(--radius);font-size:13px;font-family:inherit;outline:none"></div>
        <div class="field"><label>New password</label><input type="password" id="cp-new" style="width:100%;padding:7px 10px;border:1px solid var(--border);border-radius:var(--radius);font-size:13px;font-family:inherit;outline:none"></div>
        <button class="btn btn-primary" onclick="App.changePassword()">Change Password</button>
        <span id="cp-msg" style="margin-left:10px;font-size:12px"></span>
      </div>
      <button class="btn btn-secondary" style="margin-top:12px" onclick="App.logout()">Sign out</button>
    </div>`);
  },

  copyToken() {
    const t = $('#agent-token-display').text();
    navigator.clipboard.writeText(t).then(() => {
      const btn = $('.token-box button');
      btn.text('Copied!');
      setTimeout(() => btn.text('Copy'), 1500);
    });
  },

  async changePassword() {
    const oldPw = $('#cp-old').val();
    const newPw = $('#cp-new').val();
    if (!oldPw || !newPw) return;
    try {
      await $.ajax({ url: '/api/auth/change-password', method: 'POST', contentType: 'application/json', data: JSON.stringify({ old_password: oldPw, new_password: newPw }) });
      $('#cp-msg').css('color','oklch(0.4 0.14 150)').text('Password changed.');
    } catch (e) {
      $('#cp-msg').css('color','var(--p-high)').text(e.responseJSON?.error||'Error');
    }
  },

  logout() { AUTH.clear(); location.reload(); },

  showNewUserModal() {
    const modal = $(`
      <div class="cmd-overlay" style="z-index:1500" id="new-user-overlay" onclick="if(event.target===this) $('#new-user-overlay').remove()">
        <div class="cmd" style="padding:20px">
          <h3 style="font-weight:600;margin-bottom:16px">New User</h3>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Name</label><input class="form-control" id="nu-name" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></div>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Email</label><input class="form-control" id="nu-email" type="email" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></div>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Password</label><input class="form-control" id="nu-password" type="password" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></div>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Role</label><select class="form-select" id="nu-role" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius)"><option value="admin">Admin</option><option value="member" selected>Member</option><option value="viewer">Viewer</option></select></div>
          <div style="display:flex;justify-content:flex-end;gap:8px">
            <button class="btn btn-secondary" onclick="$('#new-user-overlay').remove()">Cancel</button>
            <button class="btn btn-primary" onclick="App.createUser()">Create User</button>
          </div>
        </div>
      </div>
    `);
    $('body').append(modal);
    $('#nu-name').focus();
  },

  async createUser() {
    const name = $('#nu-name').val().trim();
    const email = $('#nu-email').val().trim();
    const password = $('#nu-password').val();
    if (!name || !email || !password) return;
    try {
      const u = await $.ajax({
        url: '/api/users', method: 'POST', contentType: 'application/json',
        data: JSON.stringify({ name, email, password, role: $('#nu-role').val() }),
      });
      this.users.push(u);
      $('#new-user-overlay').remove();
      this.render();
    } catch (e) { console.error(e); alert('Error creating user: ' + (e.responseJSON?.error || e.statusText)); }
  },

  editUser(id) {
    const u = this.users.find(u => u.id == id);
    if (!u) return;
    const modal = $(`
      <div class="cmd-overlay" style="z-index:1500" id="edit-user-overlay" onclick="if(event.target===this) $('#edit-user-overlay').remove()">
        <div class="cmd" style="padding:20px">
          <h3 style="font-weight:600;margin-bottom:16px">Edit User — ${this.esc(u.name)}</h3>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Name</label><input class="form-control" id="eu-name" value="${this.esc(u.name)}" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></div>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Email</label><input class="form-control" id="eu-email" type="email" value="${this.esc(u.email)}" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></div>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Role</label><select class="form-select" id="eu-role" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius)"><option value="admin" ${u.role==='admin'?'selected':''}>Admin</option><option value="member" ${u.role==='member'?'selected':''}>Member</option><option value="viewer" ${u.role==='viewer'?'selected':''}>Viewer</option></select></div>
          <div class="mb-3" style="padding:12px;background:var(--bg-sunken);border:1px solid var(--border);border-radius:var(--radius)">
            <label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">New Password</label>
            <div style="display:flex;gap:8px">
              <input class="form-control" id="eu-password" type="password" placeholder="Leave blank to keep current" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px;flex:1">
              <button class="btn btn-secondary" onclick="App.adminChangePassword(${id})">Set</button>
            </div>
            <span id="eu-pw-msg" style="font-size:11px"></span>
          </div>
          <div style="display:flex;justify-content:flex-end;gap:8px">
            <button class="btn btn-secondary" onclick="$('#edit-user-overlay').remove()">Cancel</button>
            <button class="btn btn-primary" onclick="App.submitEditUser(${id})">Save Changes</button>
          </div>
        </div>
      </div>
    `);
    $('body').append(modal);
    $('#eu-name').focus();
  },

  async adminChangePassword(id) {
    const pw = $('#eu-password').val();
    if (!pw) return;
    try {
      await $.ajax({ url: `/api/users/${id}/password`, method: 'PUT', contentType: 'application/json', data: JSON.stringify({ new_password: pw }) });
      $('#eu-pw-msg').css('color','oklch(0.4 0.14 150)').text('Password updated.');
      $('#eu-password').val('');
    } catch (e) {
      $('#eu-pw-msg').css('color','var(--p-high)').text(e.responseJSON?.error||'Error');
    }
  },

  async submitEditUser(id) {
    try {
      const data = {
        name: $('#eu-name').val().trim(),
        email: $('#eu-email').val().trim(),
        role: $('#eu-role').val(),
      };
      if (!data.name || !data.email) return;
      const updated = await $.ajax({ url: `/api/users/${id}`, method: 'PUT', contentType: 'application/json', data: JSON.stringify(data) });
      const idx = this.users.findIndex(u => u.id == id);
      if (idx >= 0) this.users[idx] = updated;
      $('#edit-user-overlay').remove();
      this.render();
    } catch (e) { console.error(e); alert('Error updating user'); }
  },

  async deleteTicket(id, display) {
    if (!confirm(`Delete ${display}?\n\nThis is permanent — the ticket and its comments, PR links, and history will be removed.`)) return;
    try {
      await $.ajax({ url: `/api/tickets/${id}`, method: 'DELETE' });
      this.closePanel();
      await this.reloadTickets();
    } catch (e) { console.error(e); alert('Error deleting ticket: ' + (e.responseJSON?.error || e.statusText)); }
  },

  async deleteUser(id) {
    const u = this.users.find(u => u.id == id);
    if (!u || !confirm(`Remove ${u.name}?`)) return;
    try {
      await $.ajax({ url: `/api/users/${id}`, method: 'DELETE' });
      this.users = this.users.filter(u => u.id != id);
      this.render();
    } catch (e) { console.error(e); alert('Error deleting user'); }
  },

  // ── Command palette ──
  openCmd() { this.renderCmd(); },
  closeCmd() { $('.cmd-overlay').remove(); },

  renderCmd() {
    const projects = this.projects;
    const actions = [
      { html: `${I.plus}<span>Create new ticket…</span><span class="cmd-meta">action</span>`, action: 'new-ticket' },
      { html: `${I.folder}<span>Go to projects</span><span class="cmd-meta">action</span>`, action: 'projects' },
    ];

    function ticketRowHTML(t) {
      const proj = projects.find(p => p.id == t.project_id);
      return `<span class="dot ${STATUS_DOT[t.status]}"></span><span class="cmd-id">${t.display_id}</span><span>${App.esc(t.name)}</span><span class="cmd-meta">${proj?.name||''}</span>`;
    }
    function projectRowHTML(p) {
      return `<span class="dot" style="background:${p.color}"></span><span>${p.name}</span><span class="cmd-meta">project</span>`;
    }

    function renderList(tickets, filter) {
      const q = (filter||'').toLowerCase();
      const projFiltered = q ? projects.filter(p => p.name.toLowerCase().includes(q) || (p.description||'').toLowerCase().includes(q)) : projects;
      const actFiltered = q ? actions.filter(a => {
        const el = $('<div>').html(a.html);
        return el.text().toLowerCase().includes(q);
      }) : actions;

      let html = tickets.slice(0, 8).map(t => `<div class="cmd-row" data-action="ticket" data-id="${t.id}">${ticketRowHTML(t)}</div>`).join('');
      if (projFiltered.length) html += '<div style="padding:6px 10px;font-size:10.5px;color:var(--text-faint);text-transform:uppercase;letter-spacing:0.04em;font-weight:600">Projects</div>';
      html += projFiltered.slice(0, 4).map(p => `<div class="cmd-row" data-action="project" data-id="${p.id}">${projectRowHTML(p)}</div>`).join('');
      html += actFiltered.map(a => `<div class="cmd-row" data-action="${a.action}">${a.html}</div>`).join('');
      if (!tickets.length && !projFiltered.length && !actFiltered.length) {
        html = '<div style="padding:12px;text-align:center;color:var(--text-faint);font-size:12.5px">No results</div>';
      }
      return html;
    }

    const overlay = $(`<div class="cmd-overlay" onclick="App.closeCmd()" id="cmd-overlay">
      <div class="cmd" onclick="event.stopPropagation()">
        <input class="cmd-input" id="cmd-search-input" placeholder="Search tickets, projects, actions…" autofocus>
        <div class="cmd-list" id="cmd-list"></div>
      </div>
    </div>`);

    $('body').append(overlay);

    let selIdx = -1;
    let searchDebounce = null;
    const visibleRows = () => $('#cmd-overlay .cmd-row');

    function updateSel(i) {
      const vr = visibleRows();
      vr.removeClass('sel');
      if (i >= 0 && i < vr.length) vr.eq(i).addClass('sel');
    }

    function actOnRow(row) {
      const action = $(row).data('action');
      const id = $(row).data('id');
      if (action === 'ticket') App.openTicket(id);
      else if (action === 'project') { App.selectProject(id); }
      else if (action === 'new-ticket') { App.closeCmd(); App.showNewTicketModal(); }
      else if (action === 'projects') { App.closeCmd(); App.showProjectsView(); }
      App.closeCmd();
    }

    function doSearch(query) {
      $.get('/api/tickets', { search: query || undefined }, tickets => {
        $('#cmd-list').html(renderList(tickets, query));
        selIdx = -1;
      });
    }

    doSearch('');

    $('#cmd-search-input').on('input', function() {
      const val = $(this).val();
      clearTimeout(searchDebounce);
      searchDebounce = setTimeout(() => doSearch(val), 150);
    });

    $('#cmd-search-input').on('keydown', function(e) {
      const vr = visibleRows();
      if (e.key === 'ArrowDown') { e.preventDefault(); selIdx = Math.min(selIdx + 1, vr.length - 1); updateSel(selIdx); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); selIdx = Math.max(selIdx - 1, 0); updateSel(selIdx); }
      else if (e.key === 'Enter') { e.preventDefault();
        if (selIdx >= 0) actOnRow(vr.eq(selIdx));
      }
      else if (e.key === 'Escape') { App.closeCmd(); }
    });

    $('#cmd-overlay').on('click', '.cmd-row', function() { actOnRow(this); });

    $('#cmd-search-input').focus();
  },

  // ── Sidebar collapse ──
  toggleSidebar() {
    const sb = $('.sidebar');
    const collapsed = !sb.hasClass('collapsed');
    sb.toggleClass('collapsed', collapsed);
    localStorage.setItem('tt_sidebar_collapsed', collapsed ? '1' : '0');
    const icon = collapsed
      ? '<svg class="svg-icon" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M6 4l4 4-4 4"/></svg>'
      : '<svg class="svg-icon" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M10 4l-4 4 4 4"/></svg>';
    $('#sb-collapse-btn').html(icon);
  },

  // ── Navigation ──
  setView(v) { this.view = v; this.activeProjectId = null; this.render(); },
  setCycle(id) { this.activeCycleId = id; this.view = 'cycle'; this.render(); },
  selectProject(id) { this.activeProjectId = id; this.view = 'project'; this.render(); },
  showProjectsView() { this.view = 'projects'; this.activeProjectId = null; this.render(); },

  bindBoardEvents() {
    $('.col-add[data-status]').off('click').on('click', function() {
      const status = $(this).data('status');
      App.showQuickAdd(status);
    });

    // jQuery UI Sortable — drag between columns + vertical reorder
    let reorderPending = false;
    $('.col-body').sortable({
      connectWith: '.col-body',
      items: '.card',
      placeholder: 'card-placeholder',
      forcePlaceholderSize: true,
      tolerance: 'pointer',
      stop: function() {
        if (reorderPending) return;
        reorderPending = true;
        const items = [];
        $('.col-body').each(function() {
          const status = $(this).data('status');
          $(this).find('.card').each(function(i) {
            items.push({ id: parseInt($(this).data('ticket-id')), status: status, sort_order: i });
          });
        });
        $.ajax({ url: '/api/tickets/reorder', method: 'PUT', contentType: 'application/json', data: JSON.stringify({ items }) })
          .then(() => App.reloadTickets())
          .always(() => { reorderPending = false; });
      },
    });
  },

  reloadTickets() {
    return $.get('/api/tickets', tickets => {
      this.tickets = tickets;
      this.render();
    });
  },

  showQuickAdd(status) {
    const colBody = $(`.col-body[data-status="${status}"]`);
    colBody.find('.card-quickadd').remove();
    const quickAdd = $(`<div class="card-quickadd">
      <input placeholder="Ticket title…" id="qa-input" onkeydown="if(event.key==='Enter')App.submitQuickAdd('${status}');if(event.key==='Escape')$(this).closest('.card-quickadd').remove()">
      <div class="card-quickadd-row">
        <span><span class="dot ${STATUS_DOT[status]}"></span> ${STATUS_LABELS[status]}</span>
        <span style="margin-left:auto"><span class="kbd">↵</span> add · <span class="kbd">esc</span> cancel</span>
      </div>
    </div>`);
    colBody.prepend(quickAdd);
    $('#qa-input').focus();
  },

  async submitQuickAdd(status) {
    const title = $('#qa-input').val().trim();
    if (!title) return;
    try {
      const t = await $.ajax({
        url: '/api/tickets', method: 'POST', contentType: 'application/json',
        data: JSON.stringify({ name: title, status, project_id: this.activeProjectId || this.projects[0]?.id, cycle_id: this.activeCycleId }),
      });
      this.tickets.unshift(t);
      this.render();
    } catch (e) { console.error(e); }
  },

  bindKeys() {
    $(document).on('keydown', function(e) {
      const tag = (e.target.tagName||'').toLowerCase();
      const editing = tag === 'input' || tag === 'textarea' || $(e.target).is('[contenteditable]');
      if (!editing && (e.key === '/' || ((e.metaKey||e.ctrlKey) && e.key.toLowerCase() === 'k'))) {
        e.preventDefault(); App.openCmd();
      }
      if (!editing && e.key.toLowerCase() === 'c' && !$('.cmd-overlay').length) {
        App.showNewTicketModal();
      }
      if (!editing && e.key.toLowerCase() === 'b' && !$('.cmd-overlay').length) {
        App.mode = 'board'; App.render();
      }
      if (!editing && e.key.toLowerCase() === 'l' && !$('.cmd-overlay').length) {
        App.mode = 'list'; App.render();
      }
    });
  },

  // ── Helpers ──
  toggleFilterDropdown(name) {
    const $dd = $(`#fd-${name}`);
    const wasOpen = $dd.is(':visible');
    $('.filter-drop').hide();
    if (!wasOpen) {
      this.buildFilterDropdown(name);
      $dd.show();
    }
  },

  buildFilterDropdown(name) {
    const $dd = $(`#fd-${name}`);
    let items = [];
    const labels = { status: 'Status', priority: 'Priority', assignee: 'Assignee', type: 'Type' };
    if (name === 'status') {
      items = STATUSES.map(s => ({ val: s, label: STATUS_LABELS[s] }));
    } else if (name === 'priority') {
      items = ['urgent','high','medium','low','none'].map(p => ({ val: p, label: p.charAt(0).toUpperCase()+p.slice(1) }));
    } else if (name === 'type') {
      items = [{val:'bug',label:'Bug'},{val:'feature',label:'Feature'},{val:'chore',label:'Chore'}];
    } else if (name === 'assignee') {
      items = this.users.map(u => ({ val: u.id, label: u.name }));
    }
    const cur = this.filters[name] || (name === 'assignee' ? this.filters['assignee_id'] : null);
    const selKey = name === 'assignee' ? 'assignee_id' : name;
    let html = `<button class="filter-drop-item${!cur?' sel':''}" onclick="App.setFilter('${selKey}','')">All</button>`;
    html += items.map(it => {
      const cls = (String(cur) === String(it.val)) ? ' sel' : '';
      return `<button class="filter-drop-item${cls}" onclick="App.setFilter('${selKey}','${it.val}')">${this.esc(it.label)}</button>`;
    }).join('');
    $dd.html(html);
  },

  setFilter(key, val) {
    if (!val || String(this.filters[key]) === String(val)) {
      this.filters[key] = null;
    } else {
      this.filters[key] = val;
    }
    $('.filter-drop').hide();
    this.render();
  },

  esc(s) { return $('<span>').text(s||'').html(); },

  // Render markdown to sanitised HTML. marked + DOMPurify are loaded from CDN
  // in index.html. If either fails to load, fall back to plain escaped text so
  // we never inject raw markdown source into the DOM as HTML.
  md(s) {
    if (!s) return '';
    if (typeof marked === 'undefined' || typeof DOMPurify === 'undefined') {
      return this.esc(s);
    }
    const raw = marked.parse(String(s), { breaks: true, gfm: true });
    return DOMPurify.sanitize(raw, {
      ALLOWED_ATTR: ['href', 'title', 'target', 'rel', 'class', 'src', 'alt'],
    });
  },

  editDescription(id) {
    const t = this.tickets.find(x => x.id == id);
    if (!t) return;
    const $wrap = $('#panel-desc-wrap');
    if ($wrap.find('textarea').length) return;
    const current = t.description || '';
    $wrap.html(`
      <textarea id="desc-edit" class="form-control" rows="6" style="font-family:inherit;font-size:13px;width:100%;resize:vertical">${this.esc(current)}</textarea>
      <div style="display:flex;gap:8px;justify-content:flex-end;margin-top:6px">
        <button class="btn btn-ghost" onclick="App.renderDescription(${id})">Cancel</button>
        <button class="btn btn-primary" onclick="App.saveDescription(${id})">Save</button>
      </div>
    `);
    setTimeout(() => $('#desc-edit').focus(), 0);
  },

  renderDescription(id) {
    const t = this.tickets.find(x => x.id == id);
    if (!t) return;
    const $wrap = $('#panel-desc-wrap');
    if (t.description) {
      $wrap.html(
        `<div id="panel-desc" class="panel-desc" ondblclick="App.editDescription(${id})">${this.md(t.description)}</div>` +
        `<button class="btn-icon panel-desc-edit" title="Edit description" onclick="App.editDescription(${id})">${I.pencil}</button>`
      );
    } else {
      $wrap.html(`<div id="panel-desc" class="panel-desc empty" onclick="App.editDescription(${id})">No description yet — click to edit.</div>`);
    }
  },

  async saveDescription(id) {
    const val = $('#desc-edit').val();
    try {
      const updated = await $.ajax({ url: `/api/tickets/${id}`, method: 'PATCH', contentType: 'application/json', data: JSON.stringify({ description: val }) });
      const idx = this.tickets.findIndex(t => t.id == id);
      if (idx >= 0) this.tickets[idx] = updated;
      this.ticketDetail = updated;
      this.renderDescription(id);
    } catch (e) { console.error(e); alert('Error saving description: ' + (e.responseJSON?.error || e.statusText)); }
  },

  relDate(d) {
    if (!d) return '';
    try { return new Date(d).toLocaleDateString('en-US',{month:'short',day:'numeric'}); } catch(e) { return d; }
  },
};

// ── Init ──
$(function() {
  App.init();

  // Close filter dropdowns on outside click
  $(document).on('click', function(e) {
    if (!$(e.target).closest('.filterchip-wrap').length) {
      $('.filter-drop').hide();
    }
  });

  // Board/List toggle
  $('.view-tabs').on('click', 'button', function() {
    App.mode = $(this).data('mode');
    App.render();
    $('.view-tabs button').removeClass('active');
    $(this).addClass('active');
  });
  $('.view-tabs button[data-mode="board"]').addClass('active');

  // Sidebar navigation
  $(document).on('click', '.view-trigger', function() {
    App.view = $(this).data('view');
    App.activeProjectId = null;
    App.render();
  });
});
