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
  link:     '<svg class="svg-icon" width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M7 9a3 3 0 004.24 0l2.12-2.12a3 3 0 10-4.24-4.24L8 3.76"/><path d="M9 7a3 3 0 00-4.24 0L2.64 9.12a3 3 0 104.24 4.24L8 12.24"/></svg>',
  pencil:   '<svg class="svg-icon" width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M11 2l3 3-8 8H3v-3l8-8z"/></svg>',
  folder:   '<svg class="svg-icon" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M2 4.5a1 1 0 011-1h3.5l1 1.5H13a1 1 0 011 1v6a1 1 0 01-1 1H3a1 1 0 01-1-1v-7.5z"/></svg>',
  pr:       '<svg class="svg-icon" width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="4" cy="4" r="1.5"/><circle cx="4" cy="12" r="1.5"/><circle cx="12" cy="12" r="1.5"/><path d="M4 5.5v5"/><path d="M5.5 4H10a2 2 0 012 2v5"/></svg>',
  trash:    '<svg class="svg-icon" width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M3 4h10M6.5 4V2.5h3V4M5 4l.5 9h5l.5-9M7 6.5v5M9 6.5v5"/></svg>',
  doc:      '<svg class="svg-icon" width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M4 2h6l3 3v9a1 1 0 01-1 1H4a1 1 0 01-1-1V3a1 1 0 011-1z"/><path d="M10 2v3h3"/></svg>',
};

const STATUSES = ['todo','progress','review','done','cancel'];
const STATUS_LABELS = { todo:'Todo', progress:'In Progress', review:'In Review', done:'Done', cancel:'Cancelled' };
const STATUS_DOT = { todo:'dot-todo', progress:'dot-progress', review:'dot-review', done:'dot-done', cancel:'dot-cancel' };
const STATUS_COLOR_CLASS = { todo:'status-color-todo', progress:'status-color-progress', review:'status-color-review', done:'status-color-done', cancel:'status-color-cancel' };

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
  // Docs state
  docsContext: { space: 'global', project_id: null },
  activeFolderId: null,
  activeDocId: null,
  folders: [],
  docs: [],
  currentDoc: null,
  // Track which folders are collapsed (set of ids collapsed)
  collapsedFolders: new Set(),
  // Editor state
  editorMode: false,
  editorDirty: false,
  editorTags: [],
  // Version history panel open/closed
  versionsOpen: false,
  // Docs search XHR state (hoisted to avoid race conditions on re-bind)
  _searchXhr: null,
  _searchDebounceTimer: null,
  // Sidebar project submenu state
  _openProjectMenu: null,

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
    // Ticket route
    const mTicket = hash.match(/^#\/ticket\/(\d+)$/);
    if (mTicket) {
      const tid = parseInt(mTicket[1]);
      if (tid && !$('.panel').length) this.openTicket(tid);
      return;
    }
    // Docs routes: #docs/global, #docs/global/<doc_id>,
    //              #docs/project/<pid>, #docs/project/<pid>/<doc_id>
    const mDocsGlobalDoc = hash.match(/^#docs\/global\/(\d+)$/);
    if (mDocsGlobalDoc) {
      const docId = parseInt(mDocsGlobalDoc[1]);
      this.docsContext = { space: 'global', project_id: null };
      this.view = 'docs-global';
      this.loadDocsTree().then(() => this.openDoc(docId));
      return;
    }
    const mDocsGlobal = hash.match(/^#docs\/global$/);
    if (mDocsGlobal) {
      this.docsContext = { space: 'global', project_id: null };
      this.view = 'docs-global';
      this.loadDocsTree();
      return;
    }
    const mDocsProjDoc = hash.match(/^#docs\/project\/(\d+)\/(\d+)$/);
    if (mDocsProjDoc) {
      const pid = parseInt(mDocsProjDoc[1]);
      const docId = parseInt(mDocsProjDoc[2]);
      this.docsContext = { space: 'project', project_id: pid };
      this.view = 'docs-project';
      this.loadDocsTree().then(() => this.openDoc(docId));
      return;
    }
    const mDocsProj = hash.match(/^#docs\/project\/(\d+)$/);
    if (mDocsProj) {
      const pid = parseInt(mDocsProj[1]);
      this.docsContext = { space: 'project', project_id: pid };
      this.view = 'docs-project';
      this.loadDocsTree();
      return;
    }
  },

  filtered() {
    let list = this.tickets;
    const cid = this.activeCycleId;
    if (this.view === 'backlog') list = list.filter(t => !t.cycle_id);
    else if (this.view === 'project' && this.activeProjectId) list = list.filter(t => t.project_id == this.activeProjectId);
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
    const isTicketView = ['cycle','project','backlog'].includes(this.view);
    const isDocsView = this.view === 'docs-global' || this.view === 'docs-project';
    $('#filterbar').toggle(isTicketView);
    // Hide the topbar action buttons (New ticket / view tabs) in docs views
    $('.topbar-actions').toggle(!isDocsView);
    if (this.view === 'projects') {
      this.renderProjectsPage();
    } else if (this.view === 'users') {
      if (AUTH.user()?.role !== 'admin') { this.view = 'cycle'; this.render(); return; }
      this.renderUsersPage();
    } else if (this.view === 'profile') {
      this.renderProfilePage();
    } else if (this.view === 'backlog') {
      this.renderCrumbs();
      $('#content-area').html(this.backlogHTML());
      this.bindBacklogEvents();
    } else if (this.view === 'project-cycles') {
      this.renderProjectCyclesPage();
    } else if (isDocsView) {
      this.renderDocsPage();
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
        <div class="sb-cycle-label"><span>Active cycle</span><button class="sb-cycle-card-edit" title="Edit cycle" onclick="event.stopPropagation();App.editCycle(${c.id})">${I.pencil}</button></div>
        <div class="sb-cycle-name">${this.esc(c.title)}${c.description ? ' · ' + this.esc(c.description) : ''}</div>
        <div class="sb-cycle-progress"><div class="sb-cycle-progress-fill" style="width:${pct}%"></div></div>
        <div class="sb-cycle-stats"><span>${c.done} of ${c.total} done</span><span>${pct}%</span></div>
      `);
    }

    // Counts
    const isAdmin = AUTH.user()?.role === 'admin';
    $('#sb-people-section').toggle(isAdmin);
    if (isAdmin) $('#cnt-users').text(this.users.length);
    $('#cnt-backlog').text(this.tickets.filter(t => !t.cycle_id).length);

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
    const projectViewActive = this.view === 'project' || this.view === 'project-cycles' || this.view === 'docs-project';
    if (projectViewActive) $(`.sb-item.project-item[data-id="${this.activeProjectId}"]`).addClass('active');

    // Project list
    $('#sb-project-list').html(this.projects.map(p => {
      const count = this.tickets.filter(t => t.project_id === p.id && t.status !== 'done' && t.status !== 'cancel').length;
      const isOpen = this._openProjectMenu === p.id;
      const act = (projectViewActive && this.activeProjectId === p.id) ? ' active' : '';
      const submenu = isOpen ? `<div class="sb-project-submenu">
        <button class="sb-project-submenu-item" onclick="event.stopPropagation();App.setView('docs-project',${p.id})">Docs</button>
        <button class="sb-project-submenu-item" onclick="event.stopPropagation();App.setView('project-cycles',${p.id})">Cycles</button>
      </div>` : '';
      return `<div class="sb-project-wrap${isOpen ? ' open' : ''}">
        <button class="sb-item project-item${act}" data-id="${p.id}" onclick="App.selectProject(${p.id})">
          <span class="sb-dot" style="background:${p.color}"></span><span class="sb-label">${p.name}</span><span class="sb-count">${count}</span>
        </button>${submenu}
      </div>`;
    }).join(''));

    // Cycle list
    $('#sb-cycle-list').html(this.cycles.filter(c => c.status === 'in_progress').map(c => {
      const act = (this.view === 'cycle' && this.activeCycleId === c.id) ? ' active' : '';
      const nowBadge = c.active ? '<span class="sb-cycle-row-now">now</span>' : '';
      return `<div class="sb-cycle-row${act}">
        <button class="sb-item${act}" onclick="App.setCycle(${c.id})" style="padding-right:28px">
          <span class="sb-icon">${I.sparkle}</span><span class="sb-label">${this.esc(c.title)}</span>${nowBadge}
        </button>
        <button class="sb-cycle-edit" title="Edit cycle" onclick="event.stopPropagation();App.editCycle(${c.id})">${I.pencil}</button>
      </div>`;
    }).join(''));
  },

  renderCrumbs() {
    if (this.view === 'projects' || this.view === 'users') return;
    let html = '';
    if (this.view === 'project' && this.activeProjectId) {
      const p = this.projects.find(p => p.id == this.activeProjectId);
      html = `<span class="crumb" onclick="App.showProjectsView()">Projects</span><span class="crumb-sep">${I.chevRight}</span><span class="crumb active"><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${p?.color};margin-right:6px"></span>${p?.name}</span>`;
    } else if (this.view === 'backlog') {
      html = `<span class="crumb active">Backlog</span><span style="color:var(--text-faint);font-size:12px;margin-left:4px">· tickets without a cycle · ${this.filtered().length} tickets</span>`;
    } else {
      const labels = { inbox:'Board', cycle: this.cycles.find(c => c.id === this.activeCycleId)?.title || '' };
      html = `<span class="crumb active">${labels[this.view] || 'Board'}</span>`;
      const c = this.cycles.find(c => c.id === this.activeCycleId);
      if (c) {
        html += `<span style="color:var(--text-faint);font-size:12px;margin-left:4px">· ${c.description || ''} · ${this.filtered().length} tickets</span>`;
      }
    }
    $('#crumbs').html(html);
  },

  // ── Board ──
  boardHTML() {
    const filtered = this.filtered();
    // Backlog is now the standalone Backlog page (cycle_id IS NULL); no column.
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

  // ── Backlog page ──
  backlogHTML() {
    const filtered = this.filtered();
    if (!filtered.length) {
      return `<div style="padding:60px 18px;text-align:center;color:var(--text-faint);font-size:13px">
        No tickets in the backlog. Tickets with no cycle land here.
      </div>`;
    }
    // Group by project, then within a project sort by priority then status.
    const PRIO_RANK = { urgent: 0, high: 1, medium: 2, low: 3, none: 4 };
    const STATUS_RANK = { progress: 0, review: 1, todo: 2, done: 3, cancel: 4 };
    const byProject = new Map();
    for (const t of filtered) {
      const k = t.project_id || 'none';
      if (!byProject.has(k)) byProject.set(k, []);
      byProject.get(k).push(t);
    }
    let html = `<div class="list-view backlog-view">`;
    for (const [pid, rows] of byProject) {
      rows.sort((a, b) =>
        (PRIO_RANK[a.priority] ?? 9) - (PRIO_RANK[b.priority] ?? 9)
        || (STATUS_RANK[a.status] ?? 9) - (STATUS_RANK[b.status] ?? 9));
      const proj = this.projects.find(p => p.id == pid);
      const projLabel = proj ? `<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${proj.color};margin-right:6px"></span>${this.esc(proj.name)}` : '<span style="color:var(--text-faint)">No project</span>';
      html += `<div class="list-group">
        <div class="list-group-head">${projLabel}<span class="count">${rows.length}</span></div>
        ${rows.map(t => this.backlogRowHTML(t)).join('')}
      </div>`;
    }
    html += `</div>`;
    return html;
  },

  backlogRowHTML(t) {
    const proj = this.projects.find(p => p.id == t.project_id);
    const prioCls = t.priority === 'urgent' || t.priority === 'high' ? 'high' : t.priority === 'medium' ? 'medium' : 'low';
    const prioHTML = t.priority === 'urgent'
      ? `<span class="card-prio urgent" title="Urgent"><svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="var(--p-high)" stroke-width="1.5"><rect x="3" y="3" width="10" height="10" rx="2"/><path d="M8 6v3M8 11h.01" stroke-width="1.6"/></svg></span>`
      : `<span class="card-prio ${prioCls}"><span class="prio-bars"><span class="b1"></span><span class="b2"></span><span class="b3"></span></span></span>`;
    const cycleOpts = ['<option value="">— assign cycle —</option>']
      .concat(this.cycles.map(c => `<option value="${c.id}">${this.esc(c.title)}</option>`))
      .join('');
    return `<div class="list-row" data-ticket-id="${t.id}">
      <span class="row-prio" onclick="App.openTicket(${t.id})">${prioHTML}</span>
      <span class="card-type ${TYPE_CLASS[t.type] || 'feature'}" onclick="App.openTicket(${t.id})">${TYPE_LETTER[t.type] || 'F'}</span>
      <span class="row-id" onclick="App.openTicket(${t.id})">${t.display_id}</span>
      <span class="row-title" onclick="App.openTicket(${t.id})">${this.esc(t.name)}</span>
      <span class="row-proj" onclick="App.openTicket(${t.id})"><span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:${proj?.color};margin-right:6px"></span>${proj?.name||''}</span>
      <span class="row-comments" onclick="App.openTicket(${t.id})">${t.comment_count > 0 ? `${I.comment} ${t.comment_count}` : ''}</span>
      <span class="row-cycle-assign">
        <select class="prop-pill backlog-cycle-select" data-ticket-id="${t.id}" onclick="event.stopPropagation()">${cycleOpts}</select>
      </span>
    </div>`;
  },

  bindBacklogEvents() {
    const self = this;
    $('.backlog-cycle-select').off('change').on('change', function() {
      const cid = parseInt($(this).val());
      const tid = parseInt($(this).data('ticket-id'));
      if (!cid || !tid) return;
      const patch = { cycle_id: cid };
      const ticket = self.tickets.find(t => t.id === tid);
      if (ticket && (!ticket.status || ticket.status === 'backlog')) patch.status = 'todo';
      $.ajax({ url: `/api/tickets/${tid}`, method: 'PATCH', contentType: 'application/json', data: JSON.stringify(patch) })
        .then(updated => { self.tickets = self.tickets.map(t => t.id === tid ? { ...t, ...updated } : t); self.render(); })
        .fail(e => { console.error(e); alert('Failed to assign cycle'); });
    });
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

  async renderProjectCyclesPage() {
    const p = this.projects.find(p => p.id === this.activeProjectId);
    $('#crumbs').html('');
    $('#content-area').html('<div class="projects-page"><div style="padding:40px;text-align:center;color:var(--text-muted)">Loading cycles…</div></div>');
    let cycles;
    try {
      cycles = await $.get(`/api/cycles?project_id=${this.activeProjectId}`);
    } catch (e) {
      $('#content-area').html(`<div class="projects-page"><div style="padding:40px;color:var(--p-high)">Failed to load cycles: ${this.esc(e?.responseJSON?.error || e?.statusText || String(e))}</div></div>`);
      return;
    }
    const CYCLE_STATUS_LABELS = { planning: 'Planning', in_progress: 'In Progress', completed: 'Completed', pending: 'Pending' };
    const STATUS_ORDER = ['in_progress', 'planning', 'pending', 'completed'];
    const grouped = {};
    cycles.forEach(c => {
      const s = c.status || 'planning';
      if (!grouped[s]) grouped[s] = [];
      grouped[s].push(c);
    });
    const groups = STATUS_ORDER.filter(s => grouped[s]);
    Object.keys(grouped).forEach(s => { if (!groups.includes(s)) groups.push(s); });
    let html = '';
    if (cycles.length === 0) {
      html = '<div style="color:var(--text-faint);font-size:13.5px;padding:24px 0">No cycles yet.</div>';
    } else {
      groups.forEach(status => {
        const label = CYCLE_STATUS_LABELS[status] || status;
        html += `<div class="cycles-group">
          <div class="cycles-group-header">${label}</div>
          <div class="cycles-group-cards">${grouped[status].map(c => {
            const pct = c.total ? Math.round((c.done / c.total) * 100) : 0;
            const dateRange = (c.start_date || c.end_date) ? `<div class="cycle-card-dates">${this.esc(c.start_date || '')}${c.start_date && c.end_date ? ' → ' : ''}${this.esc(c.end_date || '')}</div>` : '';
            return `<div class="cycle-card" onclick="App.selectCycle(${c.id})">
              <div class="cycle-card-title">${I.sparkle} ${this.esc(c.title)}</div>
              ${c.description ? `<div class="cycle-card-desc">${this.esc(c.description)}</div>` : ''}
              ${dateRange}
              <div class="cycle-card-progress"><div class="cycle-card-progress-fill" style="width:${pct}%"></div></div>
              <div class="cycle-card-stats"><span>${c.done} of ${c.total} done</span><span>${pct}%</span></div>
            </div>`;
          }).join('')}</div>
        </div>`;
      });
    }
    const pName = p ? this.esc(p.name) : 'Project';
    $('#content-area').html(`<div class="projects-page">
      <div class="page-header"><div><h1>${pName} — Cycles</h1><div class="sub">${cycles.length} cycle${cycles.length !== 1 ? 's' : ''}</div></div></div>
      ${html}
    </div>`);
  },

  selectCycle(id) {
    if (!this._guardDirtyEditor()) return;
    this.activeCycleId = id; this.view = 'cycle'; this.render();
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
    const cycleOpts = `<option value=""${!t.cycle_id?' selected':''}>— Backlog (no cycle) —</option>` +
      this.cycles.map(c => `<option value="${c.id}" ${t.cycle_id===c.id?'selected':''}>${c.title}</option>`).join('');
    const userOpts = this.users.map(u => `<option value="${u.id}" ${t.assignee_id===u.id?'selected':''}>${this.esc(u.name)}</option>`).join('');

    const activityFeed = this.activityFeedHTML(t);

    const attachments = t.attachments || [];
    const attachmentsHTML = attachments.map(a => `
      <div class="attachment-item">
        <span class="attachment-icon">${I.attach}</span>
        <a class="attachment-name" href="${a.download_url}" target="_blank" rel="noopener">${this.esc(a.filename)}</a>
        <span class="attachment-meta">${this.fmtBytes(a.size_bytes)} · ${this.esc(a.uploader_name||'Unknown')} · ${this.relDate(a.created_at)}</span>
        <button class="rel-remove" onclick="App.deleteAttachment(${t.id},${a.id})" title="Remove">${I.close}</button>
      </div>
    `).join('');

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

    const linkedDocs = t.linked_documents || [];
    const linkedDocsHTML = linkedDocs.map(d => {
      const spaceBadge = d.space_type === 'project'
        ? `<span class="docs-link-space" title="Project doc">${this.esc((this.projects.find(p => p.id === d.project_id) || {}).name || 'Project')}</span>`
        : `<span class="docs-link-space" title="Global doc">Global</span>`;
      return `<div class="docs-link-row" data-doc-id="${d.id}" data-doc-space="${d.space_type}" data-doc-project="${d.project_id || ''}">
        <span class="docs-link-icon">${I.doc}</span>
        <span class="docs-link-title">${this.esc(d.title)}</span>
        ${spaceBadge}
        <button class="docs-link-remove" data-unlink-doc-id="${d.id}" data-unlink-ticket-id="${t.id}" title="Unlink">${I.close}</button>
      </div>`;
    }).join('');

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
            <button class="btn-icon" title="Attach file" onclick="App.openAttachmentPicker(${t.id})">${I.attach}</button>
            <button class="btn-icon" title="Copy link" onclick="App.copyTicketLink(${t.id})">${I.link}</button>
            <button class="btn-icon" title="Delete ticket" onclick="App.deleteTicket(${t.id})" style="color:var(--p-high)">${I.trash}</button>
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
            <div class="panel-section-title rel-section-head">
              <span>Linked documents · ${linkedDocs.length}</span>
              <button class="btn btn-ghost" onclick="App.showLinkDocModal(${t.id})">+ Link doc</button>
            </div>
            <div id="panel-linked-docs">${linkedDocsHTML || '<div class="rel-empty">No linked documents yet.</div>'}</div>
          </div>
          <div class="panel-section">
            <div class="panel-section-title rel-section-head">
              <span>Attachments · ${attachments.length}</span>
              <button class="btn btn-ghost" onclick="App.openAttachmentPicker(${t.id})">+ Add</button>
            </div>
            <div id="panel-attachments-drop" class="attachment-drop" data-ticket-id="${t.id}">
              ${attachmentsHTML || '<div class="rel-empty">No attachments yet — drop files here or click + Add.</div>'}
            </div>
            <input type="file" id="panel-attachment-input" multiple style="display:none" onchange="App.uploadAttachments(${t.id}, this.files)"/>
          </div>
          <div class="panel-section">
            <div class="panel-section-title">Activity · ${(t.comments||[]).length + (t.history||[]).length}</div>
            <div class="comments">${activityFeed || '<div style="color:var(--text-faint);font-size:12.5px;padding:8px 0">No activity yet.</div>'}</div>
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
      // Allow clearing cycle_id (Backlog) by sending null on empty.
      if (field === 'cycle_id') App.patchTicket(t.id, field, val === '' ? null : val);
      else if (val !== '') App.patchTicket(t.id, field, val);
    });
    $('.panel-patch-input').on('blur', function() {
      const field = $(this).data('field');
      const val = $(this).val();
      App.patchTicket(t.id, field, val);
    });
    // Drag-drop attachments onto the panel section.
    const $drop = $('#panel-attachments-drop');
    $drop.on('dragover', function(e) { e.preventDefault(); e.stopPropagation(); $(this).addClass('drag-over'); });
    $drop.on('dragleave dragend drop', function(e) { $(this).removeClass('drag-over'); });
    $drop.on('drop', function(e) {
      e.preventDefault(); e.stopPropagation();
      const files = e.originalEvent.dataTransfer && e.originalEvent.dataTransfer.files;
      if (files && files.length) App.uploadAttachments(t.id, files);
    });
    // Linked-docs row navigation + unlink (delegated; data-attrs avoid XSS via title)
    $('#panel-linked-docs').on('click', '.docs-link-remove', function(e) {
      e.stopPropagation();
      const docId = parseInt($(this).data('unlink-doc-id'));
      const ticketId = parseInt($(this).data('unlink-ticket-id'));
      App.unlinkTicketDoc(ticketId, docId);
    });
    $('#panel-linked-docs').on('click', '.docs-link-row', function() {
      const docId = parseInt($(this).data('doc-id'));
      const space = $(this).data('doc-space');
      const projectId = $(this).data('doc-project');
      App.openDocFromTicket(docId, space, projectId);
    });
  },

  openAttachmentPicker(id) {
    $('#panel-attachment-input').trigger('click');
  },

  async uploadAttachments(ticketId, fileList) {
    const files = Array.from(fileList || []);
    if (!files.length) return;
    for (const f of files) {
      if (f.size > 25 * 1024 * 1024) {
        alert(`${f.name} is larger than 25MB and was skipped.`);
        continue;
      }
      const fd = new FormData();
      fd.append('file', f);
      try {
        await $.ajax({
          url: `/api/tickets/${ticketId}/attachments`,
          method: 'POST',
          data: fd,
          processData: false,
          contentType: false,
        });
      } catch (e) {
        alert(`Failed to upload ${f.name}: ${e.responseJSON?.error || e.statusText}`);
      }
    }
    await this.refreshTicketDetail(ticketId);
  },

  async deleteAttachment(ticketId, attachmentId) {
    if (!confirm('Remove this attachment? This cannot be undone.')) return;
    try {
      await $.ajax({ url: `/api/tickets/${ticketId}/attachments/${attachmentId}`, method: 'DELETE' });
      await this.refreshTicketDetail(ticketId);
    } catch (e) {
      alert('Failed to remove attachment: ' + (e.responseJSON?.error || e.statusText));
    }
  },

  async refreshTicketDetail(ticketId) {
    try {
      const t = await $.ajax({ url: `/api/tickets/${ticketId}`, method: 'GET' });
      this.ticketDetail = t;
      const idx = this.tickets.findIndex(x => x.id == ticketId);
      if (idx >= 0) this.tickets[idx] = t;
      $('.panel, .panel-overlay').remove();
      this.showPanel(t);
    } catch (e) { console.error(e); }
  },

  fmtBytes(n) {
    if (!n && n !== 0) return '';
    const units = ['B', 'KB', 'MB', 'GB'];
    let i = 0; let v = n;
    while (v >= 1024 && i < units.length - 1) { v /= 1024; i++; }
    return `${v.toFixed(v < 10 && i > 0 ? 1 : 0)} ${units[i]}`;
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
                 data-ticket-id="${t.id}"
                 data-display-id="${App.esc(t.display_id)}"
                 data-ticket-name="${App.esc(t.name)}">
              <span class="rel-ticket-link">${App.esc(t.display_id)}</span>
              <span class="rel-ticket-name">${App.esc(t.name)}</span>
              <span class="rel-status-dot ${STATUS_DOT[t.status]}"></span>
            </div>
          `).join(''));
          $('#rel-results').off('click').on('click', '.rel-search-item', function() {
            const $el = $(this);
            $('#rel-search').val($el.data('displayId') + ' — ' + $el.data('ticketName')).data('selected-id', $el.data('ticketId'));
            $('#rel-results').html('');
          });
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
    const onBacklog = this.view === 'backlog';
    const cycleOpts = `<option value=""${onBacklog?' selected':''}>— Backlog (no cycle) —</option>` +
      this.cycles.map(c => `<option value="${c.id}" ${!onBacklog && c.id===this.activeCycleId?'selected':''}>${c.title}</option>`).join('');
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
          cycle_id: $('#nt-cycle').val() ? parseInt($('#nt-cycle').val()) : null,
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

  editCycle(id) {
    const c = this.cycles.find(c => c.id == id);
    if (!c) return;
    const pids = new Set((c.project_ids || (c.projects || []).map(p => p.id) || []).map(Number));
    const projOpts = this.projects.map(p => `
      <label style="display:flex;align-items:center;gap:6px;padding:4px 8px;border-radius:4px;cursor:pointer;font-size:12.5px" onmouseover="this.style.background='var(--bg-hover)'" onmouseout="this.style.background=''">
        <input type="checkbox" class="ec-pid" value="${p.id}" ${pids.has(p.id) ? 'checked' : ''}>
        <span class="sb-dot" style="background:${p.color};display:inline-block;width:8px;height:8px;border-radius:50%"></span>
        <span>${this.esc(p.name)}</span>
      </label>`).join('');
    const modal = $(`
      <div class="cmd-overlay" style="z-index:1500" id="edit-cycle-overlay" onclick="if(event.target===this) $('#edit-cycle-overlay').remove()">
        <div class="cmd" style="padding:20px">
          <h3 style="font-weight:600;margin-bottom:16px">Edit Cycle — ${this.esc(c.title)}</h3>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Title</label><input class="form-control" id="ec-title" value="${this.esc(c.title)}" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></div>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Description</label><textarea class="form-control" id="ec-desc" rows="2" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px">${this.esc(c.description || '')}</textarea></div>
          <div style="display:flex;gap:10px;margin-bottom:14px">
            <div style="flex:1"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Status</label><select class="form-select" id="ec-status" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius)">
              <option value="pending"${c.status==='pending'?' selected':''}>Pending</option>
              <option value="in_progress"${c.status==='in_progress'?' selected':''}>In Progress</option>
              <option value="completed"${c.status==='completed'?' selected':''}>Completed</option>
              <option value="cancelled"${c.status==='cancelled'?' selected':''}>Cancelled</option>
            </select></div>
          </div>
          <div style="display:flex;gap:10px;margin-bottom:14px">
            <div style="flex:1"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Start date</label><input type="date" class="form-control" id="ec-start" value="${c.start_date || ''}" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></div>
            <div style="flex:1"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">End date</label><input type="date" class="form-control" id="ec-end" value="${c.end_date || ''}" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px"></div>
          </div>
          <div class="mb-3"><label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Projects</label>
            <div style="border:1px solid var(--border);border-radius:var(--radius);padding:4px;max-height:160px;overflow-y:auto">${projOpts || '<div style="padding:6px 8px;color:var(--text-muted);font-size:12px">No projects yet</div>'}</div>
          </div>
          <div style="display:flex;justify-content:space-between;gap:8px">
            <button class="btn btn-ghost" style="color:var(--p-high)" onclick="App.deleteCycle(${id})">Delete</button>
            <div style="display:flex;gap:8px">
              <button class="btn btn-secondary" onclick="$('#edit-cycle-overlay').remove()">Cancel</button>
              <button class="btn btn-primary" onclick="App.submitEditCycle(${id})">Save Changes</button>
            </div>
          </div>
        </div>
      </div>
    `);
    $('body').append(modal);
    $('#ec-title').focus();
  },

  async submitEditCycle(id) {
    const title = $('#ec-title').val().trim();
    if (!title) { alert('Title is required'); return; }
    const project_ids = $('#edit-cycle-overlay .ec-pid:checked').map(function(){ return parseInt(this.value); }).get();
    const data = {
      title,
      description: $('#ec-desc').val().trim(),
      status: $('#ec-status').val(),
      start_date: $('#ec-start').val() || null,
      end_date: $('#ec-end').val() || null,
      project_ids,
    };
    try {
      const updated = await $.ajax({ url: `/api/cycles/${id}`, method: 'PUT', contentType: 'application/json', data: JSON.stringify(data) });
      const idx = this.cycles.findIndex(c => c.id == id);
      if (idx >= 0) this.cycles[idx] = updated;
      $('#edit-cycle-overlay').remove();
      this.render();
    } catch (e) { console.error(e); alert('Error updating cycle: ' + (e.responseJSON?.error || e.statusText)); }
  },

  async deleteCycle(id) {
    const c = this.cycles.find(c => c.id == id);
    if (!c) return;
    if (!confirm(`Delete cycle "${c.title}"? Tickets in this cycle will not be deleted but will lose their cycle assignment.`)) return;
    try {
      await $.ajax({ url: `/api/cycles/${id}`, method: 'DELETE' });
      this.cycles = this.cycles.filter(c => c.id != id);
      if (this.activeCycleId == id) this.activeCycleId = this.cycles[0]?.id || null;
      $('#edit-cycle-overlay').remove();
      this.render();
    } catch (e) { console.error(e); alert('Error deleting cycle: ' + (e.responseJSON?.error || e.statusText)); }
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

  logout() {
    if (this.editorMode && this.editorDirty) {
      if (!confirm('You have unsaved changes. Discard them and sign out?')) return;
    }
    AUTH.clear(); location.reload();
  },

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
    const ticket = this.tickets.find(t => t.id == id) || this.ticketDetail;
    const label = display || (ticket ? ticket.display_id : `#${id}`);
    if (!confirm(`Delete ${label}?\n\nThis is permanent — the ticket and its comments, PR links, and history will be removed.`)) return;
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

    $('#cmd-list').on('click', '.cmd-row', function() { actOnRow(this); });

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
  _guardDirtyEditor() {
    if (this.editorMode && this.editorDirty) {
      if (!confirm('You have unsaved changes. Discard them?')) return false;
    }
    this.editorMode = false;
    this.editorDirty = false;
    this.editorTags = [];
    this.versionsOpen = false;
    return true;
  },

  setView(v, projectId) {
    if (!this._guardDirtyEditor()) return;
    if (v === 'docs-global') {
      this.view = 'docs-global';
      this.activeProjectId = null;
      this.docsContext = { space: 'global', project_id: null };
      this.activeFolderId = null;
      this.activeDocId = null;
      this.currentDoc = null;
      this.folders = [];
      this.docs = [];
      this.loadDocsTree();
      return;
    }
    if (v === 'docs-project' && projectId) {
      this.view = 'docs-project';
      this.activeProjectId = parseInt(projectId);
      this.docsContext = { space: 'project', project_id: parseInt(projectId) };
      this.activeFolderId = null;
      this.activeDocId = null;
      this.currentDoc = null;
      this.folders = [];
      this.docs = [];
      this.loadDocsTree();
      return;
    }
    if (v === 'project-cycles' && projectId) {
      this.view = 'project-cycles';
      this.activeProjectId = parseInt(projectId);
      this.render();
      return;
    }
    this.view = v;
    this.activeProjectId = null;
    this.render();
  },
  setCycle(id) {
    if (!this._guardDirtyEditor()) return;
    this.activeCycleId = id; this.view = 'cycle'; this.render();
  },
  selectProject(id) {
    if (!this._guardDirtyEditor()) return;
    this._openProjectMenu = (this._openProjectMenu === id) ? null : id;
    this.renderSidebar();
  },
  showProjectsView() {
    if (!this._guardDirtyEditor()) return;
    this.view = 'projects'; this.activeProjectId = null; this.render();
  },

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

  activityFeedHTML(t) {
    const comments = (t.comments || []).map(c => ({
      kind: 'comment',
      created_at: c.created_at,
      data: c,
    }));
    const history = (t.history || []).map(h => ({
      kind: 'history',
      created_at: h.created_at,
      data: h,
    }));
    const merged = comments.concat(history).sort((a, b) => {
      const ta = new Date(a.created_at).getTime() || 0;
      const tb = new Date(b.created_at).getTime() || 0;
      return ta - tb;
    });
    return merged.map(item => item.kind === 'comment'
      ? this.commentHTML(item.data)
      : this.historyHTML(item.data)
    ).join('');
  },

  commentHTML(c) {
    const isAgent = c.author_type === 'agent';
    const name = c.author_name || 'Unknown';
    const initials = name.split(' ').map(w => w[0]).join('').slice(0,2).toUpperCase();
    return `<div class="comment">
      <div class="comment-avatar ${isAgent?'agent':''}" style="${!isAgent?'background:var(--text-muted)':''}">${isAgent ? I.sparkle : initials}</div>
      <div class="comment-body">
        <div class="comment-head">
          <span class="comment-author">${this.esc(name)}${isAgent?'<span class="agent-tag">agent</span>':''}</span>
          <span class="comment-time">${this.relDateTime(c.created_at)}</span>
        </div>
        <div class="comment-text">${this.md(c.body || '')}</div>
        ${c.pr_link ? `<div class="comment-pr">${I.pr} <span>${this.esc(c.pr_link.title||c.pr_link.url||'')}</span><span class="pr-status ${c.pr_link.status}">${c.pr_link.status}</span></div>` : ''}
      </div>
    </div>`;
  },

  historyHTML(h) {
    const name = h.author_name || 'System';
    const initials = name.split(' ').map(w => w[0]).join('').slice(0,2).toUpperCase();
    const summary = this.historySummary(h);
    return `<div class="activity-event">
      <div class="activity-avatar">${initials}</div>
      <div class="activity-line">
        <span class="activity-author">${this.esc(name)}</span>
        <span class="activity-text">${summary}</span>
        <span class="activity-time">${this.relDateTime(h.created_at)}</span>
      </div>
    </div>`;
  },

  historySummary(h) {
    const f = h.field_name;
    const oldV = h.old_value;
    const newV = h.new_value;
    const fmt = v => v === null || v === undefined || v === '' ? '<em>nothing</em>' : `<code>${this.esc(String(v))}</code>`;
    const FIELD_LABELS = {
      name: 'name', description: 'description', type: 'type', priority: 'priority',
      status: 'status', project_id: 'project', cycle_id: 'cycle',
      assignee: 'assignee', assignee_id: 'assignee', due_date: 'due date',
    };
    if (f === 'ticket_created') return `created this ticket`;
    if (f === 'comment_added') return `commented`;
    if (f === 'pr_linked') return `linked a PR — ${this.esc(newV || '')}`;
    if (f === 'pr_removed') return `removed PR link — ${this.esc(oldV || '')}`;
    if (f === 'relationship_added') return `added relationship — ${this.esc(newV || '')}`;
    if (f === 'relationship_removed') return `removed relationship — ${this.esc(oldV || '')}`;
    if (f === 'attachment_added') return `attached <code>${this.esc(newV || '')}</code>`;
    if (f === 'attachment_removed') return `removed attachment <code>${this.esc(oldV || '')}</code>`;
    const label = FIELD_LABELS[f] || f;
    if (oldV && newV) return `changed ${label} from ${fmt(oldV)} to ${fmt(newV)}`;
    if (newV) return `set ${label} to ${fmt(newV)}`;
    if (oldV) return `cleared ${label} (was ${fmt(oldV)})`;
    return `updated ${label}`;
  },

  // ── Docs ──

  async loadDocsTree() {
    const ctx = this.docsContext;
    const params = { space: ctx.space };
    if (ctx.project_id) params.project_id = ctx.project_id;
    try {
      const [folders, docs] = await Promise.all([
        $.get('/api/folders', params),
        $.get('/api/documents', params),
      ]);
      this.folders = folders;
      this.docs = docs;
    } catch (e) {
      console.error('loadDocsTree error:', e);
      this.folders = [];
      this.docs = [];
    }
    this.render();
    return Promise.resolve();
  },

  renderDocsPage() {
    const ctx = this.docsContext;
    const isGlobal = ctx.space === 'global';
    const proj = isGlobal ? null : this.projects.find(p => p.id === ctx.project_id);
    const title = isGlobal ? 'Global docs' : (proj ? proj.name + ' docs' : 'Project docs');

    // Update hash
    let hashTarget;
    if (isGlobal) {
      hashTarget = this.activeDocId ? `#docs/global/${this.activeDocId}` : '#docs/global';
    } else {
      hashTarget = this.activeDocId
        ? `#docs/project/${ctx.project_id}/${this.activeDocId}`
        : `#docs/project/${ctx.project_id}`;
    }
    if (window.location.hash !== hashTarget) {
      history.replaceState(null, '', hashTarget);
    }

    // Update crumbs
    let crumbHtml = `<span class="crumb active">${this.esc(title)}</span>`;
    if (!isGlobal && proj) {
      crumbHtml = `<span class="crumb" onclick="App.showProjectsView()">Projects</span>
        <span class="crumb-sep">${I.chevRight}</span>
        <span class="crumb active">${this.esc(proj.name)} docs</span>`;
    }
    $('#crumbs').html(crumbHtml);

    const treeHtml = this.buildDocTreeHtml(null, 0);

    let contentHtml;
    if (this.editorMode && this.currentDoc) {
      contentHtml = this.buildDocEditorHtml(this.currentDoc);
    } else if (this.currentDoc) {
      contentHtml = this.buildDocViewerHtml(this.currentDoc);
    } else {
      contentHtml = `<div class="docs-empty">
           <svg width="40" height="40" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round"><path d="M4 2h6l3 3v9a1 1 0 01-1 1H4a1 1 0 01-1-1V3a1 1 0 011-1z"/><path d="M10 2v3h3"/><path d="M5 7h6M5 9.5h4"/></svg>
           <div>Select or create a document</div>
         </div>`;
    }

    // Search bar HTML
    const searchBarHtml = `
      <div class="docs-search-wrap">
        <span class="docs-search-icon">${I.search}</span>
        <input class="docs-search" id="docs-search-input" placeholder="Search docs…" autocomplete="off">
        <div class="docs-search-results" id="docs-search-results" style="display:none"></div>
      </div>`;

    $('#content-area').html(`
      <div class="docs-layout">
        <div class="docs-tree">
          ${searchBarHtml}
          <div class="docs-tree-actions">
            <button class="btn btn-secondary" style="font-size:11.5px;padding:4px 8px" onclick="App.createFolder(null)">
              ${I.plus} Folder
            </button>
            <button class="btn btn-secondary" style="font-size:11.5px;padding:4px 8px" onclick="App.createDoc(null)">
              ${I.plus} Doc
            </button>
          </div>
          ${treeHtml || '<div style="color:var(--text-faint);font-size:12px;padding:4px 6px">No folders or documents yet</div>'}
        </div>
        <div class="docs-content" id="docs-content-pane">${contentHtml}</div>
      </div>
    `);

    this.bindDocsEvents();

    // Async load attachments and versions after DOM is set
    if (this.currentDoc && !this.editorMode) {
      this.loadDocAttachmentsInline(this.currentDoc.id);
      if (this.versionsOpen) {
        this.loadVersionsInline(this.currentDoc.id);
      }
      // Lazy-fetch any linked tickets not in local cache
      const linkedIds = this.currentDoc.linked_ticket_ids || [];
      const unknownIds = linkedIds.filter(tid => !this.tickets.find(x => x.id === tid));
      unknownIds.forEach(tid => this._lazyFetchLinkedTicket(this.currentDoc.id, tid));
    }
  },

  buildDocTreeHtml(parentFolderId, depth) {
    let html = '';
    // Folders at this level
    const folders = this.folders.filter(f => {
      if (parentFolderId === null) return !f.parent_folder_id;
      return f.parent_folder_id === parentFolderId;
    });
    folders.forEach(f => {
      const isCollapsed = this.collapsedFolders.has(f.id);
      const isActive = this.activeFolderId === f.id;
      const chevron = isCollapsed ? I.chevRight : I.chevDown;
      const childHtml = this.buildDocTreeHtml(f.id, depth + 1);
      html += `
        <div class="docs-tree-folder${isCollapsed ? ' collapsed' : ''}" data-folder-id="${f.id}">
          <div class="docs-tree-folder-row${isActive ? ' active' : ''}"
               onclick="App.toggleFolder(${f.id})"
               data-folder-id="${f.id}">
            <span class="docs-folder-chevron">${chevron}</span>
            <span class="docs-folder-icon">${I.folder}</span>
            <span class="docs-folder-name" title="${this.esc(f.name)}">${this.esc(f.name)}</span>
            <button class="docs-item-more" onclick="event.stopPropagation();App.showFolderMenu(event,${f.id})" title="More">${I.more}</button>
          </div>
          <div class="docs-tree-children">${childHtml}</div>
        </div>`;
    });
    // Docs at this level (those with this folder_id)
    const docs = this.docs.filter(d => {
      if (parentFolderId === null) return !d.folder_id;
      return d.folder_id === parentFolderId;
    });
    docs.forEach(d => {
      const isActive = this.activeDocId === d.id;
      html += `
        <div class="docs-tree-doc${isActive ? ' active' : ''}"
             onclick="App.openDoc(${d.id})"
             data-doc-id="${d.id}">
          <span class="docs-doc-icon">${I.doc}</span>
          <span class="docs-doc-title" title="${this.esc(d.title)}">${this.esc(d.title)}</span>
          <button class="docs-item-more" onclick="event.stopPropagation();App.showDocMenu(event,${d.id})" title="More">${I.more}</button>
        </div>`;
    });
    return html;
  },

  buildDocViewerHtml(doc) {
    const version = doc.current_version;
    const bodyHtml = version && version.body_md ? this.md(version.body_md) : '<em style="color:var(--text-faint)">No content yet.</em>';
    // Build breadcrumb
    const breadcrumbs = this.buildFolderBreadcrumb(doc.folder_id);
    const breadcrumbHtml = breadcrumbs.length
      ? breadcrumbs.map(f => `<span class="crumb" style="cursor:pointer;color:var(--accent-text)" onclick="App.selectFolderInTree(${f.id})">${this.esc(f.name)}</span>`).join(`<span style="color:var(--text-faint)">${I.chevRight}</span>`)
        + `<span style="color:var(--text-faint)">${I.chevRight}</span><span>${this.esc(doc.title)}</span>`
      : `<span>${this.esc(doc.title)}</span>`;
    const tags = doc.tags || [];
    const tagsHtml = tags.length
      ? tags.map(t => `<span class="docs-tag-viewer-pill">${this.esc(t.name)}</span>`).join('')
      : '';

    // Linked tickets
    const linkedIds = doc.linked_ticket_ids || [];
    const linkedHtml = linkedIds.length
      ? linkedIds.map(tid => {
          const t = this.tickets.find(x => x.id === tid);
          if (t) {
            return `<div class="docs-link-row" onclick="App.openTicket(${t.id})">
              <span class="dot ${STATUS_DOT[t.status] || 'dot-todo'}" style="width:7px;height:7px;border-radius:50%;flex-shrink:0"></span>
              <span class="docs-link-id">${this.esc(t.display_id)}</span>
              <span class="docs-link-name">${this.esc(t.name)}</span>
              <button class="docs-link-remove" onclick="event.stopPropagation();App.unlinkDocTicket(${doc.id},${t.id})" title="Unlink">${I.close}</button>
            </div>`;
          }
          // Unknown ticket — render placeholder and lazy-fetch
          return `<div class="docs-link-row" id="docs-linked-ticket-${tid}">
            <span class="docs-link-id">Ticket #${tid}</span>
            <span class="docs-link-name" style="color:var(--text-faint)">Loading…</span>
            <button class="docs-link-remove" onclick="event.stopPropagation();App.unlinkDocTicket(${doc.id},${tid})" title="Unlink">${I.close}</button>
          </div>`;
        }).join('')
      : `<div class="docs-links-empty">No linked tickets yet.</div>`;

    // Attachments placeholder — will be loaded async
    const attachmentsHtml = `<div id="docs-attachments-list"><div style="color:var(--text-faint);font-size:12px"><span class="spinner" style="margin-right:6px"></span>Loading…</div></div>`;

    // Version history (toggle)
    const versionsSection = this.versionsOpen
      ? `<div id="docs-versions-panel"><div style="color:var(--text-faint);font-size:12px"><span class="spinner" style="margin-right:6px"></span>Loading…</div></div>`
      : '';

    return `
      <div class="docs-doc-header">
        <h1 class="docs-doc-title-h1">${this.esc(doc.title)}</h1>
        <div class="docs-doc-actions">
          <button class="btn btn-secondary" style="font-size:12px" onclick="App.editDoc(${doc.id})">${I.pencil} Edit</button>
          <button class="btn btn-secondary" style="font-size:12px" id="docs-versions-btn" onclick="App.toggleVersionPanel(${doc.id})" title="Version history">${I.list} History</button>
          <button class="btn-icon" onclick="App.deleteDoc(${doc.id})" title="Delete document" style="color:var(--p-high)">${I.trash}</button>
        </div>
      </div>
      <div class="docs-breadcrumb">${breadcrumbHtml}</div>
      ${tagsHtml ? `<div style="display:flex;gap:5px;flex-wrap:wrap;margin-bottom:14px">${tagsHtml}</div>` : ''}
      <div class="docs-doc-body">${bodyHtml}</div>

      ${this.versionsOpen ? `<div class="docs-versions">
        <div class="docs-versions-header">
          <span class="docs-versions-title">Version history</span>
          <button class="btn btn-ghost" style="font-size:11.5px;padding:2px 8px" onclick="App.toggleVersionPanel(${doc.id})">Close</button>
        </div>
        ${versionsSection}
      </div>` : ''}

      <div class="docs-links">
        <div class="docs-links-header">
          <span class="docs-links-title">Linked tickets · ${linkedIds.length}</span>
          <button class="btn btn-ghost" style="font-size:11.5px;padding:2px 8px" onclick="App.showLinkTicketModal(${doc.id})">+ Link ticket</button>
        </div>
        ${linkedHtml}
      </div>

      <div class="docs-attachments">
        <div class="docs-attachments-header">
          <span class="docs-attachments-title">Attachments</span>
          <button class="btn btn-ghost" style="font-size:11.5px;padding:2px 8px" onclick="App.openDocAttachmentPicker(${doc.id})">+ Upload</button>
        </div>
        ${attachmentsHtml}
        <input type="file" id="doc-attachment-input" multiple style="display:none" onchange="App.uploadDocAttachments(${doc.id},this.files)">
      </div>
    `;
  },

  buildFolderBreadcrumb(folderId) {
    if (!folderId) return [];
    const crumbs = [];
    let current = folderId;
    const seen = new Set();
    while (current) {
      if (seen.has(current)) break;
      seen.add(current);
      const folder = this.folders.find(f => f.id === current);
      if (!folder) break;
      crumbs.unshift(folder);
      current = folder.parent_folder_id;
    }
    return crumbs;
  },

  bindDocsEvents() {
    // Close any open context menus when clicking elsewhere
    $(document).off('click.docs-ctx').on('click.docs-ctx', function(e) {
      if (!$(e.target).closest('.docs-ctx-menu').length) {
        $('.docs-ctx-menu').remove();
      }
      // Close search results when clicking outside
      if (!$(e.target).closest('.docs-search-wrap').length) {
        $('#docs-search-results').hide();
      }
    });

    // Delegated download handler — avoids filename in onclick attr (XSS)
    $(document).off('click.docs-download').on('click.docs-download', '.docs-attachment-row .btn[data-attachment-id]', function() {
      const $btn = $(this);
      App.downloadDocAttachment(
        parseInt($btn.data('docId')),
        parseInt($btn.data('attachmentId')),
        $btn.data('filename')
      );
    });

    // Search bar — uses App._searchXhr and App._searchDebounceTimer (hoisted) to avoid race on re-bind
    $(document).off('input.docs-search').on('input.docs-search', '#docs-search-input', function() {
      const q = $(this).val().trim();
      if (App._searchDebounceTimer) clearTimeout(App._searchDebounceTimer);
      if (!q) { $('#docs-search-results').hide(); return; }
      App._searchDebounceTimer = setTimeout(() => App.doDocsSearch(q), 300);
    });

    $(document).off('keydown.docs-search').on('keydown.docs-search', '#docs-search-input', function(e) {
      if (e.key === 'Escape') { $(this).val(''); $('#docs-search-results').hide(); }
    });
  },

  toggleFolder(folderId) {
    if (this.collapsedFolders.has(folderId)) {
      this.collapsedFolders.delete(folderId);
    } else {
      this.collapsedFolders.add(folderId);
    }
    this.activeFolderId = folderId;
    this.renderDocsPage();
  },

  selectFolderInTree(folderId) {
    // Expand it if collapsed
    this.collapsedFolders.delete(folderId);
    this.activeFolderId = folderId;
    this.renderDocsPage();
  },

  showFolderMenu(event, folderId) {
    event.stopPropagation();
    $('.docs-ctx-menu').remove();
    const folder = this.folders.find(f => f.id === folderId);
    if (!folder) return;
    const menu = $(`
      <div class="docs-ctx-menu">
        <button class="docs-ctx-item" onclick="App.renameFolder(${folderId})">Rename</button>
        <button class="docs-ctx-item" onclick="App.createFolder(${folderId})">+ Subfolder</button>
        <button class="docs-ctx-item" onclick="App.createDoc(${folderId})">+ Doc here</button>
        <button class="docs-ctx-item danger" onclick="App.deleteFolder(${folderId})">Delete</button>
      </div>
    `);
    $('body').append(menu);
    const rect = event.target.getBoundingClientRect();
    const menuEl = menu[0];
    let top = rect.bottom + 2;
    let left = rect.left;
    if (left + 150 > window.innerWidth) left = window.innerWidth - 155;
    if (top + 160 > window.innerHeight) top = rect.top - menuEl.offsetHeight - 2;
    menu.css({ top: top + 'px', left: left + 'px' });
  },

  showDocMenu(event, docId) {
    event.stopPropagation();
    $('.docs-ctx-menu').remove();
    const menu = $(`
      <div class="docs-ctx-menu">
        <button class="docs-ctx-item" onclick="App.openDoc(${docId})">Open</button>
        <button class="docs-ctx-item danger" onclick="App.deleteDoc(${docId})">Delete</button>
      </div>
    `);
    $('body').append(menu);
    const rect = event.target.getBoundingClientRect();
    let top = rect.bottom + 2;
    let left = rect.left;
    if (left + 150 > window.innerWidth) left = window.innerWidth - 155;
    if (top + 100 > window.innerHeight) top = rect.top - menu[0].offsetHeight - 2;
    menu.css({ top: top + 'px', left: left + 'px' });
  },

  async createFolder(parentFolderId) {
    const name = prompt('Folder name:');
    if (!name || !name.trim()) return;
    const ctx = this.docsContext;
    const body = {
      name: name.trim(),
      space_type: ctx.space,
    };
    if (ctx.project_id) body.project_id = ctx.project_id;
    if (parentFolderId) body.parent_folder_id = parentFolderId;
    try {
      const folder = await $.ajax({
        url: '/api/folders', method: 'POST',
        contentType: 'application/json', data: JSON.stringify(body),
      });
      this.folders.push(folder);
      // Auto-expand the parent
      if (parentFolderId) this.collapsedFolders.delete(parentFolderId);
      this.renderDocsPage();
    } catch (e) {
      alert('Failed to create folder: ' + (e.responseJSON?.error || e.statusText));
    }
  },

  async renameFolder(folderId) {
    const folder = this.folders.find(f => f.id === folderId);
    if (!folder) return;
    const name = prompt('New name:', folder.name);
    if (!name || !name.trim() || name.trim() === folder.name) return;
    try {
      const updated = await $.ajax({
        url: `/api/folders/${folderId}`, method: 'PATCH',
        contentType: 'application/json', data: JSON.stringify({ name: name.trim() }),
      });
      const idx = this.folders.findIndex(f => f.id === folderId);
      if (idx >= 0) this.folders[idx] = updated;
      this.renderDocsPage();
    } catch (e) {
      alert('Failed to rename folder: ' + (e.responseJSON?.error || e.statusText));
    }
  },

  async deleteFolder(folderId) {
    const folder = this.folders.find(f => f.id === folderId);
    if (!folder) return;
    if (this.editorDirty && !confirm('You have unsaved edits in the open document. Continue with folder delete?')) return;
    if (!confirm(`Delete folder "${folder.name}"?\n\nAll documents and subfolders will be deleted. This cannot be undone.`)) return;
    try {
      await $.ajax({ url: `/api/folders/${folderId}`, method: 'DELETE' });
      // Remove folder and all descendants from local state
      const removedIds = this.collectFolderIds(folderId);
      this.folders = this.folders.filter(f => !removedIds.has(f.id));
      this.docs = this.docs.filter(d => !d.folder_id || !removedIds.has(d.folder_id));
      removedIds.forEach(id => this.collapsedFolders.delete(id));
      if (removedIds.has(this.activeFolderId)) this.activeFolderId = null;
      // If active doc was in one of those folders, clear it
      if (this.currentDoc && this.currentDoc.folder_id && removedIds.has(this.currentDoc.folder_id)) {
        this.currentDoc = null;
        this.activeDocId = null;
      }
      this.renderDocsPage();
    } catch (e) {
      alert('Failed to delete folder: ' + (e.responseJSON?.error || e.statusText));
    }
  },

  collectFolderIds(rootId) {
    const ids = new Set([rootId]);
    let changed = true;
    while (changed) {
      changed = false;
      this.folders.forEach(f => {
        if (f.parent_folder_id && ids.has(f.parent_folder_id) && !ids.has(f.id)) {
          ids.add(f.id);
          changed = true;
        }
      });
    }
    return ids;
  },

  showCreateDocModal(folderId) {
    const ctx = this.docsContext;
    const folderOpts = ['<option value="">— No folder (root) —</option>']
      .concat(this.folders.map(f => `<option value="${f.id}"${f.id === folderId ? ' selected' : ''}>${this.esc(f.name)}</option>`))
      .join('');
    const modal = $(`
      <div class="cmd-overlay" style="z-index:1500" id="new-doc-overlay" onclick="if(event.target===this) $('#new-doc-overlay').remove()">
        <div class="cmd" style="padding:20px;max-height:80vh;overflow-y:auto">
          <h3 style="font-weight:600;margin-bottom:16px">New Document</h3>
          <div class="mb-3">
            <label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Title</label>
            <input class="form-control" id="nd-title" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px">
          </div>
          <div class="mb-3">
            <label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Folder</label>
            <select class="form-select" id="nd-folder" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius)">${folderOpts}</select>
          </div>
          <div class="mb-3">
            <label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Body (Markdown)</label>
            <textarea class="form-control" id="nd-body" rows="8" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px;font-family:var(--font-mono)"></textarea>
          </div>
          <div class="mb-3">
            <label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Tags (comma-separated)</label>
            <input class="form-control" id="nd-tags" placeholder="e.g. api, backend, reference" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px">
          </div>
          <div class="mb-3">
            <label class="form-label" style="font-size:12px;font-weight:500;color:var(--text-muted)">Change note (optional)</label>
            <input class="form-control" id="nd-note" placeholder="Initial version" style="font-size:13px;border:1px solid var(--border);border-radius:var(--radius);padding:6px 10px">
          </div>
          <div style="display:flex;justify-content:flex-end;gap:8px">
            <button class="btn btn-secondary" onclick="$('#new-doc-overlay').remove()">Cancel</button>
            <button class="btn btn-primary" onclick="App.submitCreateDoc()">Create</button>
          </div>
        </div>
      </div>
    `);
    $('body').append(modal);
    $('#nd-title').focus();
  },

  createDoc(folderId) {
    this.showCreateDocModal(folderId);
  },

  async submitCreateDoc() {
    const title = $('#nd-title').val().trim();
    if (!title) { alert('Title is required'); return; }
    const ctx = this.docsContext;
    const rawTags = $('#nd-tags').val().trim();
    const tags = rawTags ? rawTags.split(',').map(t => t.trim()).filter(Boolean) : [];
    const folderVal = $('#nd-folder').val();
    const body = {
      title,
      space_type: ctx.space,
      body_md: $('#nd-body').val() || '',
      change_note: $('#nd-note').val().trim() || 'Initial version',
      tags,
    };
    if (ctx.project_id) body.project_id = ctx.project_id;
    if (folderVal) body.folder_id = parseInt(folderVal);
    try {
      const doc = await $.ajax({
        url: '/api/documents', method: 'POST',
        contentType: 'application/json', data: JSON.stringify(body),
      });
      this.docs.push(doc);
      $('#new-doc-overlay').remove();
      // Open the newly created doc
      await this.openDoc(doc.id);
    } catch (e) {
      alert('Failed to create document: ' + (e.responseJSON?.error || e.statusText));
    }
  },

  async openDoc(id) {
    // Guard dirty editor
    if (this.editorMode && this.editorDirty && this.activeDocId !== id) {
      if (!confirm('Discard unsaved changes?')) return;
    }
    this.editorMode = false;
    this.editorDirty = false;
    this.editorTags = [];
    this.versionsOpen = false;
    // Show loading state immediately so the pane isn't blank during fetch
    $('#docs-content-pane').html('<div class="docs-empty"><div class="spinner"></div><div style="margin-top:12px;color:var(--text-muted)">Loading document…</div></div>');
    try {
      const doc = await $.get(`/api/documents/${id}`);
      this.currentDoc = doc;
      this.activeDocId = doc.id;
      // Expand the folder chain so the doc is visible in the tree
      if (doc.folder_id) {
        this.buildFolderBreadcrumb(doc.folder_id).forEach(f => this.collapsedFolders.delete(f.id));
      }
      this.renderDocsPage();
    } catch (e) {
      if (e.status === 404) {
        alert('Document not found.');
        this.currentDoc = null;
        this.activeDocId = null;
        this.renderDocsPage();
      } else {
        console.error('openDoc error:', e);
      }
    }
  },

  async deleteDoc(id) {
    const doc = this.docs.find(d => d.id === id) || this.currentDoc;
    const name = doc ? doc.title : `document #${id}`;
    if (this.editorDirty && this.activeDocId === id && !confirm('You have unsaved edits. Continue with delete?')) return;
    if (!confirm(`Delete "${name}"?\n\nThis will permanently remove the document and all its versions. This cannot be undone.`)) return;
    try {
      await $.ajax({ url: `/api/documents/${id}`, method: 'DELETE' });
      this.docs = this.docs.filter(d => d.id !== id);
      if (this.activeDocId === id) {
        this.activeDocId = null;
        this.currentDoc = null;
        this.editorMode = false;
        this.editorDirty = false;
        this.editorTags = [];
        this.versionsOpen = false;
        $(document).off('click.editor-tags');
      }
      this.renderDocsPage();
    } catch (e) {
      alert('Failed to delete document: ' + (e.responseJSON?.error || e.statusText));
    }
  },

  // ── Docs search ──

  doDocsSearch(q) {
    // Abort any in-flight request to prevent stale results
    if (this._searchXhr) { this._searchXhr.abort(); this._searchXhr = null; }
    if (!q || !q.trim()) { $('#docs-search-results').hide(); return; }
    const ctx = this.docsContext;
    const params = { q, limit: 20 };
    if (ctx.space) params.space = ctx.space;
    if (ctx.project_id) params.project_id = ctx.project_id;
    this._searchXhr = $.get('/api/documents/search', params)
      .done(results => {
        this._searchXhr = null;
        const $res = $('#docs-search-results');
        if (!results.length) {
          $res.html('<div class="docs-search-empty">No matches</div>').show();
          return;
        }
        $res.html(results.map(r => {
          // Allow <mark> tags in snippet — sanitize with DOMPurify allowing mark
          const safeSnippet = typeof DOMPurify !== 'undefined'
            ? DOMPurify.sanitize(r.snippet || '', { ALLOWED_TAGS: ['mark'], ALLOWED_ATTR: [] })
            : this.esc(r.snippet || '');
          return `<div class="docs-search-result-row" onclick="App.selectSearchResult(${r.id})">
            <div class="docs-search-result-title">${this.esc(r.title)}</div>
            ${safeSnippet ? `<div class="docs-search-result-snippet">${safeSnippet}</div>` : ''}
          </div>`;
        }).join('')).show();
      })
      .fail(e => {
        if (e.statusText === 'abort') return; // expected when a newer request supersedes
        this._searchXhr = null;
        console.error('docs search error:', e);
        $('#docs-search-results').html('<div class="docs-search-empty">Search failed</div>').show();
      });
  },

  selectSearchResult(docId) {
    $('#docs-search-input').val('');
    $('#docs-search-results').hide();
    this.openDoc(docId);
  },

  // ── Doc editor ──

  buildDocEditorHtml(doc) {
    const version = doc.current_version;
    const currentBody = version ? (version.body_md || '') : '';
    const currentTitle = doc.title || '';
    const tagsHtml = this.editorTags.map((name, i) =>
      `<span class="docs-tag-pill">
        ${this.esc(name)}
        <button onclick="App.removeEditorTag(${i})" title="Remove tag">×</button>
      </span>`
    ).join('');
    return `
      <div class="docs-editor">
        <input class="docs-editor-title-input" id="editor-title" value="${this.esc(currentTitle)}" placeholder="Document title…">
        <div>
          <div style="font-size:11.5px;color:var(--text-faint);margin-bottom:4px;font-weight:500">Tags</div>
          <div class="docs-tag-input-wrap" id="editor-tag-wrap" onclick="document.getElementById('editor-tag-input').focus()">
            ${tagsHtml}
            <input class="docs-tag-type-input" id="editor-tag-input" placeholder="${this.editorTags.length ? '' : 'Add tag…'}" autocomplete="off">
            <div class="docs-tag-suggestions" id="editor-tag-suggestions" style="display:none"></div>
          </div>
        </div>
        <div>
          <div class="docs-editor-hint">Markdown supported — preview below</div>
          <textarea class="docs-editor-textarea" id="editor-body" placeholder="Start writing…">${this.esc(currentBody)}</textarea>
        </div>
        <div class="docs-editor-preview">
          <div class="docs-editor-preview-label">Preview</div>
          <div class="docs-doc-body" id="editor-preview">${this.md(currentBody)}</div>
        </div>
        <div>
          <input class="docs-editor-change-note" id="editor-change-note" placeholder="Optional change note">
        </div>
        <div class="docs-editor-actions">
          <button class="btn btn-primary" onclick="App.saveDocEdit(${doc.id})">Save</button>
          <button class="btn btn-secondary" onclick="App.cancelDocEdit(${doc.id})">Cancel</button>
          <span id="editor-save-error" style="color:var(--p-high);font-size:12px;margin-left:8px"></span>
        </div>
      </div>
    `;
  },

  editDoc(id) {
    if (this.editorMode && this.activeDocId === id) return;
    const doc = this.currentDoc;
    if (!doc || doc.id !== id) return;
    this.editorMode = true;
    this.editorDirty = false;
    // Copy current tags into working array
    this.editorTags = (doc.tags || []).map(t => t.name);
    this.renderDocsPage();
    // Bind editor events after DOM is ready
    this._bindEditorEvents(id, doc);
  },

  _bindEditorEvents(docId, doc) {
    // Mark dirty on any input change
    $('#editor-title, #editor-body, #editor-change-note').on('input', () => {
      this.editorDirty = true;
    });

    // Live preview with debounce
    let previewDebounce = null;
    $('#editor-body').on('input', () => {
      clearTimeout(previewDebounce);
      previewDebounce = setTimeout(() => {
        const val = $('#editor-body').val();
        $('#editor-preview').html(this.md(val));
      }, 250);
    });

    // Tag autocomplete
    let tagDebounce = null;
    $('#editor-tag-input').on('input', () => {
      this.editorDirty = true;
      const q = $('#editor-tag-input').val().trim().toLowerCase();
      clearTimeout(tagDebounce);
      if (!q) { $('#editor-tag-suggestions').hide(); return; }
      tagDebounce = setTimeout(() => App._fetchTagSuggestions(q), 200);
    });

    $('#editor-tag-input').on('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        const val = $('#editor-tag-input').val().trim().toLowerCase();
        if (val) this.addEditorTag(val);
      } else if (e.key === 'Escape') {
        $('#editor-tag-suggestions').hide();
      }
    });

    // Click outside tag suggestions to close
    $(document).off('click.editor-tags').on('click.editor-tags', (e) => {
      if (!$(e.target).closest('#editor-tag-wrap').length) {
        $('#editor-tag-suggestions').hide();
      }
    });

    // Delegated handler for tag suggestion items (avoids inline onclick + XSS)
    $(document).off('click.docs-tag-suggest').on('click.docs-tag-suggest', '.docs-tag-suggestion-item', function() {
      App.addEditorTag($(this).data('tag'));
    });
  },

  async _fetchTagSuggestions(prefix) {
    try {
      const tags = await $.get('/api/tags', { prefix });
      const existing = new Set(this.editorTags);
      const filtered = tags.filter(t => !existing.has(t.name)).slice(0, 8);
      if (!filtered.length) { $('#editor-tag-suggestions').hide(); return; }
      $('#editor-tag-suggestions').html(
        filtered.map(t =>
          `<div class="docs-tag-suggestion-item" data-tag="${this.esc(t.name)}">${this.esc(t.name)}</div>`
        ).join('')
      ).show();
    } catch (e) {
      console.error('tag fetch error:', e);
    }
  },

  addEditorTag(name) {
    const lower = name.toLowerCase().trim();
    if (!lower) return;
    if (this.editorTags.includes(lower)) return;
    this.editorTags.push(lower);
    this.editorDirty = true;
    $('#editor-tag-suggestions').hide();
    $('#editor-tag-input').val('').focus();
    // Re-render the tag pills area without full page render
    const tagsHtml = this.editorTags.map((n, i) =>
      `<span class="docs-tag-pill">
        ${this.esc(n)}
        <button onclick="App.removeEditorTag(${i})" title="Remove tag">×</button>
      </span>`
    ).join('');
    const $wrap = $('#editor-tag-wrap');
    // Remove existing pills, keep the input and suggestions
    $wrap.find('.docs-tag-pill').remove();
    $wrap.prepend(tagsHtml);
  },

  removeEditorTag(index) {
    this.editorTags.splice(index, 1);
    this.editorDirty = true;
    // Re-render pills
    const tagsHtml = this.editorTags.map((n, i) =>
      `<span class="docs-tag-pill">
        ${this.esc(n)}
        <button onclick="App.removeEditorTag(${i})" title="Remove tag">×</button>
      </span>`
    ).join('');
    const $wrap = $('#editor-tag-wrap');
    $wrap.find('.docs-tag-pill').remove();
    $wrap.prepend(tagsHtml);
  },

  async saveDocEdit(docId) {
    const doc = this.currentDoc;
    if (!doc || doc.id !== docId) return;
    const newTitle = $('#editor-title').val().trim();
    const newBody = $('#editor-body').val();
    const changeNote = $('#editor-change-note').val().trim();

    if (!newTitle) {
      $('#editor-save-error').text('Title is required');
      return;
    }

    const originalTagNames = (doc.tags || []).map(t => t.name).sort().join(',');
    const newTagNames = [...this.editorTags].sort().join(',');
    const tagsChanged = originalTagNames !== newTagNames;
    const oldTitle = doc.title;
    const oldBody = doc.current_version ? (doc.current_version.body_md || '') : '';
    const titleChanged = newTitle !== oldTitle;
    const bodyChanged = newBody !== oldBody;

    // Nothing changed — exit cleanly without any API calls
    if (!tagsChanged && !titleChanged && !bodyChanged) {
      this.cancelDocEdit(docId);
      return;
    }

    let stepReached = 'tags';
    try {
      // Step 1: If tags changed, PATCH document metadata
      if (tagsChanged) {
        await $.ajax({
          url: `/api/documents/${docId}`, method: 'PATCH',
          contentType: 'application/json',
          data: JSON.stringify({ tags: this.editorTags }),
        });
      }

      // Step 2: POST new version only if title or body changed
      stepReached = 'version';
      if (titleChanged || bodyChanged) {
        const versionBody = { body_md: newBody, title: newTitle };
        if (changeNote) versionBody.change_note = changeNote;
        await $.ajax({
          url: `/api/documents/${docId}/versions`, method: 'POST',
          contentType: 'application/json',
          data: JSON.stringify(versionBody),
        });
      }

      this.editorMode = false;
      this.editorDirty = false;
      this.editorTags = [];
      $(document).off('click.editor-tags');
      await this.openDoc(docId);
    } catch (e) {
      let msg;
      if (stepReached === 'version' && tagsChanged) {
        msg = 'Tags were saved, but the document body could not be saved. Please try again.';
      } else {
        msg = e.responseJSON?.error || e.statusText || 'Save failed';
      }
      $('#editor-save-error').text(msg);
    }
  },

  cancelDocEdit(docId) {
    if (this.editorDirty && !confirm('Discard unsaved changes?')) return;
    this.editorMode = false;
    this.editorDirty = false;
    this.editorTags = [];
    $(document).off('click.editor-tags');
    this.openDoc(docId);
  },

  // ── Version history ──

  toggleVersionPanel(docId) {
    this.versionsOpen = !this.versionsOpen;
    this.renderDocsPage();
    if (this.versionsOpen) {
      this.loadVersionsInline(docId);
    }
  },

  async loadVersionsInline(docId) {
    try {
      const versions = await $.get(`/api/documents/${docId}/versions`);
      const doc = this.currentDoc;
      const currentVersionId = doc && doc.current_version ? doc.current_version.id : null;
      const html = versions.length
        ? versions.map(v => {
            const isCurrent = v.id === currentVersionId;
            return `<div class="docs-version-row">
              <span class="docs-version-badge">v${v.version_number}</span>
              ${isCurrent ? '<span class="docs-version-current-badge">current</span>' : ''}
              ${v.title && v.title !== doc.title ? `<span style="font-weight:500;font-size:12px">${this.esc(v.title)}</span>` : ''}
              <span class="docs-version-note">${this.esc(v.change_note || '')}</span>
              <span class="docs-version-time">${this.relDateTime(v.created_at)}</span>
              <div class="docs-version-actions">
                <button class="btn btn-ghost" style="font-size:11px;padding:2px 6px" onclick="App.viewVersion(${docId},${v.id})">View</button>
                ${!isCurrent ? `<button class="btn btn-ghost" style="font-size:11px;padding:2px 6px" onclick="App.rollbackVersion(${docId},${v.id},${v.version_number})">Roll back</button>` : ''}
              </div>
            </div>`;
          }).join('')
        : '<div style="color:var(--text-faint);font-size:12.5px;padding:6px 0">No versions yet.</div>';
      $('#docs-versions-panel').html(html);
    } catch (e) {
      $('#docs-versions-panel').html('<div style="color:var(--p-high);font-size:12px">Failed to load versions.</div>');
    }
  },

  async viewVersion(docId, versionId) {
    try {
      const v = await $.get(`/api/documents/${docId}/versions/${versionId}`);
      const bodyHtml = v.body_md ? this.md(v.body_md) : '<em style="color:var(--text-faint)">Empty version.</em>';
      const modal = $(`
        <div class="cmd-overlay" style="z-index:1500" id="version-view-overlay" onclick="if(event.target===this)$('#version-view-overlay').remove()">
          <div class="cmd" style="padding:20px;max-height:80vh;overflow-y:auto;width:min(720px,92vw)">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
              <div>
                <span style="font-family:var(--font-mono);font-size:12px;color:var(--text-faint)">v${v.version_number}</span>
                <span style="font-weight:600;font-size:15px;margin-left:8px">${this.esc(v.title || '')}</span>
              </div>
              <button class="btn-icon" onclick="$('#version-view-overlay').remove()">${I.close}</button>
            </div>
            ${v.change_note ? `<div style="font-size:12px;color:var(--text-muted);margin-bottom:12px;font-style:italic">${this.esc(v.change_note)}</div>` : ''}
            <div style="font-size:12px;color:var(--text-faint);margin-bottom:16px">${this.relDateTime(v.created_at)} · ${this.esc(v.created_by || '')}</div>
            <div class="docs-doc-body">${bodyHtml}</div>
          </div>
        </div>
      `);
      $('body').append(modal);
    } catch (e) {
      alert('Failed to load version: ' + (e.responseJSON?.error || e.statusText));
    }
  },

  async rollbackVersion(docId, versionId, versionNumber) {
    if (!confirm(`Roll back to v${versionNumber}? This creates a new current version pointing to v${versionNumber}'s content.`)) return;
    try {
      await $.ajax({
        url: `/api/documents/${docId}/rollback`, method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ version_id: versionId }),
      });
      this.versionsOpen = false;
      await this.openDoc(docId);
    } catch (e) {
      alert('Rollback failed: ' + (e.responseJSON?.error || e.statusText));
    }
  },

  // ── Doc tag management (editor) ──

  // ── Doc-ticket links ──

  showLinkTicketModal(docId) {
    const modal = $(`
      <div class="cmd-overlay" style="z-index:1500" id="link-ticket-overlay" onclick="if(event.target===this)$('#link-ticket-overlay').remove()">
        <div class="cmd" style="padding:20px">
          <h3 style="font-weight:600;margin-bottom:12px">Link a ticket</h3>
          <input class="cmd-input" id="link-ticket-search" placeholder="Search by ID or name…" autofocus style="border:1px solid var(--border);border-radius:var(--radius);padding:7px 10px;width:100%;font-size:13px;font-family:inherit;outline:none;margin-bottom:8px">
          <div class="cmd-list" id="link-ticket-results" style="max-height:260px;overflow-y:auto"></div>
          <div style="display:flex;justify-content:flex-end;margin-top:10px">
            <button class="btn btn-secondary" onclick="$('#link-ticket-overlay').remove()">Cancel</button>
          </div>
        </div>
      </div>
    `);
    $('body').append(modal);

    const alreadyLinked = new Set(this.currentDoc ? (this.currentDoc.linked_ticket_ids || []) : []);

    const renderResults = (q) => {
      const lower = q.toLowerCase();
      const filtered = this.tickets.filter(t =>
        !alreadyLinked.has(t.id) &&
        (t.display_id.toLowerCase().includes(lower) || t.name.toLowerCase().includes(lower))
      ).slice(0, 10);
      if (!filtered.length) {
        $('#link-ticket-results').html('<div style="padding:10px;color:var(--text-faint);font-size:12.5px;text-align:center">No matching tickets</div>');
        return;
      }
      $('#link-ticket-results').html(filtered.map(t => `
        <div class="cmd-row" onclick="App._confirmLinkTicket(${docId},${t.id})">
          <span class="dot ${STATUS_DOT[t.status] || 'dot-todo'}" style="width:7px;height:7px;border-radius:50%;flex-shrink:0"></span>
          <span style="font-family:var(--font-mono);font-size:11px;color:var(--text-faint)">${this.esc(t.display_id)}</span>
          <span style="flex:1">${this.esc(t.name)}</span>
        </div>
      `).join(''));
    };

    renderResults('');

    $('#link-ticket-search').on('input', function() {
      renderResults($(this).val());
    });
    $('#link-ticket-search').on('keydown', function(e) {
      if (e.key === 'Escape') $('#link-ticket-overlay').remove();
    });
    setTimeout(() => $('#link-ticket-search').focus(), 0);
  },

  async _confirmLinkTicket(docId, ticketId) {
    try {
      await $.ajax({
        url: `/api/documents/${docId}/tickets`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ ticket_id: ticketId }),
      });
      $('#link-ticket-overlay').remove();
      // Update local currentDoc state
      if (this.currentDoc && this.currentDoc.id === docId) {
        const ids = this.currentDoc.linked_ticket_ids || [];
        if (!ids.includes(ticketId)) ids.push(ticketId);
        this.currentDoc.linked_ticket_ids = ids;
      }
      this.renderDocsPage();
    } catch (e) {
      alert('Failed to link ticket: ' + (e.responseJSON?.error || e.statusText));
    }
  },

  async unlinkDocTicket(docId, ticketId) {
    try {
      await $.ajax({ url: `/api/documents/${docId}/tickets/${ticketId}`, method: 'DELETE' });
      if (this.currentDoc && this.currentDoc.id === docId) {
        this.currentDoc.linked_ticket_ids = (this.currentDoc.linked_ticket_ids || []).filter(id => id !== ticketId);
      }
      this.renderDocsPage();
    } catch (e) {
      alert('Failed to unlink ticket: ' + (e.responseJSON?.error || e.statusText));
    }
  },

  // === Ticket-side linked-docs ===

  // Navigate from the ticket panel to a linked doc.
  openDocFromTicket(docId, spaceType, projectId) {
    this.closePanel();
    const target = spaceType === 'project' && projectId
      ? `#docs/project/${projectId}/${docId}`
      : `#docs/global/${docId}`;
    if (window.location.hash === target) {
      // Hash unchanged → router won't fire; navigate manually.
      this.checkHash();
    } else {
      window.location.hash = target;
    }
  },

  showLinkDocModal(ticketId) {
    const alreadyLinked = new Set(
      (this.ticketDetail && this.ticketDetail.id === ticketId
        ? (this.ticketDetail.linked_documents || []).map(d => d.id)
        : [])
    );

    const modal = $(`
      <div class="cmd-overlay" style="z-index:1500" id="link-doc-overlay" onclick="if(event.target===this)$('#link-doc-overlay').remove()">
        <div class="cmd" style="padding:20px">
          <h3 style="font-weight:600;margin-bottom:12px">Link a document</h3>
          <input class="cmd-input" id="link-doc-search" placeholder="Search documents…" autofocus
            style="border:1px solid var(--border);border-radius:var(--radius);padding:7px 10px;width:100%;font-size:13px;font-family:inherit;outline:none;margin-bottom:8px">
          <div class="cmd-list" id="link-doc-results" style="max-height:280px;overflow-y:auto">
            <div style="padding:14px;color:var(--text-faint);font-size:12.5px;text-align:center">Type to search…</div>
          </div>
          <div style="display:flex;justify-content:flex-end;margin-top:10px">
            <button class="btn btn-secondary" onclick="$('#link-doc-overlay').remove()">Cancel</button>
          </div>
        </div>
      </div>
    `);
    $('body').append(modal);

    let xhr = null;
    let debounceTimer = null;

    const renderResults = (q) => {
      if (xhr) { try { xhr.abort(); } catch (_) {} xhr = null; }
      if (!q || q.length < 2) {
        $('#link-doc-results').html('<div style="padding:14px;color:var(--text-faint);font-size:12.5px;text-align:center">Type at least 2 characters…</div>');
        return;
      }
      $('#link-doc-results').html('<div style="padding:14px;color:var(--text-faint);font-size:12.5px;text-align:center"><div class="spinner" style="margin:0 auto"></div></div>');
      xhr = $.ajax({
        url: '/api/documents/search',
        data: { q: q, limit: 20 },
        success: (results) => {
          const filtered = (results || []).filter(r => !alreadyLinked.has(r.id));
          if (!filtered.length) {
            $('#link-doc-results').html('<div style="padding:14px;color:var(--text-faint);font-size:12.5px;text-align:center">No matching documents</div>');
            return;
          }
          $('#link-doc-results').html(filtered.map(r => {
            const proj = r.space_type === 'project'
              ? (this.projects.find(p => p.id === r.project_id) || {}).name || 'Project'
              : 'Global';
            return `<div class="cmd-row" data-link-doc-id="${r.id}">
              <span style="flex-shrink:0">${I.doc}</span>
              <span style="flex:1">${this.esc(r.title)}</span>
              <span style="font-size:11px;color:var(--text-faint)">${this.esc(proj)}</span>
            </div>`;
          }).join(''));
          $('#link-doc-results').off('click.linkdoc').on('click.linkdoc', '[data-link-doc-id]', function() {
            const docId = parseInt($(this).data('link-doc-id'));
            App._confirmLinkDocToTicket(docId, ticketId);
          });
        },
        error: (e) => {
          if (e.statusText === 'abort') return;
          $('#link-doc-results').html('<div style="padding:14px;color:var(--p-high);font-size:12.5px;text-align:center">Search failed.</div>');
        },
      });
    };

    $('#link-doc-search').on('input', function() {
      const q = $(this).val();
      if (debounceTimer) clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => renderResults(q), 200);
    });
    $('#link-doc-search').on('keydown', function(e) {
      if (e.key === 'Escape') $('#link-doc-overlay').remove();
    });
    setTimeout(() => $('#link-doc-search').focus(), 0);
  },

  async _confirmLinkDocToTicket(docId, ticketId) {
    try {
      await $.ajax({
        url: `/api/documents/${docId}/tickets`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ ticket_id: ticketId }),
      });
      $('#link-doc-overlay').remove();
      await this._refreshTicketPanel(ticketId);
    } catch (e) {
      alert('Failed to link document: ' + (e.responseJSON?.error || e.statusText));
    }
  },

  async unlinkTicketDoc(ticketId, docId) {
    try {
      await $.ajax({ url: `/api/documents/${docId}/tickets/${ticketId}`, method: 'DELETE' });
      await this._refreshTicketPanel(ticketId);
    } catch (e) {
      alert('Failed to unlink document: ' + (e.responseJSON?.error || e.statusText));
    }
  },

  async _refreshTicketPanel(ticketId) {
    // Re-fetch with include_details so linked_documents is populated, then re-render.
    try {
      const fresh = await $.get(`/api/tickets/${ticketId}`);
      this.ticketDetail = fresh;
      // Replace existing panel without re-toggling overlay/scroll position.
      $('.panel, .panel-overlay').remove();
      this.showPanel(fresh);
    } catch (e) {
      console.error('Failed to refresh ticket panel:', e);
    }
  },

  _lazyFetchLinkedTicket(docId, ticketId) {
    $.get(`/api/tickets/${ticketId}`)
      .done(t => {
        // Add to local cache so future renders don't need to re-fetch
        if (!this.tickets.find(x => x.id === t.id)) this.tickets.push(t);
        const $row = $(`#docs-linked-ticket-${ticketId}`);
        if (!$row.length) return; // row may have been removed (unlinked)
        $row.html(`
          <span class="dot ${STATUS_DOT[t.status] || 'dot-todo'}" style="width:7px;height:7px;border-radius:50%;flex-shrink:0"></span>
          <span class="docs-link-id">${this.esc(t.display_id)}</span>
          <span class="docs-link-name">${this.esc(t.name)}</span>
          <button class="docs-link-remove" onclick="event.stopPropagation();App.unlinkDocTicket(${docId},${t.id})" title="Unlink">${I.close}</button>
        `);
        $row.attr('onclick', `App.openTicket(${t.id})`).css('cursor', 'pointer');
      })
      .fail(e => {
        if (e.status === 404) {
          const $row = $(`#docs-linked-ticket-${ticketId}`);
          if ($row.length) {
            $row.find('.docs-link-name').text(`Deleted ticket #${ticketId}`).css('color', 'var(--text-faint)');
            $row.find('.docs-link-id').text('');
            $row.attr('onclick', '').css('cursor', 'default');
          }
        }
      });
  },

  // ── Doc attachments ──

  openDocAttachmentPicker(docId) {
    $('#doc-attachment-input').trigger('click');
  },

  async loadDocAttachmentsInline(docId) {
    try {
      const attachments = await $.get(`/api/documents/${docId}/attachments`);
      const html = attachments.length
        ? attachments.map(a => `
          <div class="docs-attachment-row">
            <span style="color:var(--text-muted);flex-shrink:0">${I.attach}</span>
            <span class="docs-attachment-name">${this.esc(a.filename)}</span>
            <span class="docs-attachment-meta">${this.fmtBytes(a.size_bytes)} · ${this.esc(a.uploader_name || '')} · ${this.relDateTime(a.created_at)}</span>
            <button class="btn btn-ghost" style="font-size:11px;padding:2px 8px;flex-shrink:0" data-doc-id="${docId}" data-attachment-id="${a.id}" data-filename="${this.esc(a.filename)}">Download</button>
            <button class="btn-icon" onclick="App.deleteDocAttachment(${docId},${a.id})" title="Delete" style="color:var(--text-faint);flex-shrink:0">${I.trash}</button>
          </div>`).join('')
        : '<div class="docs-attachments-empty">No attachments yet.</div>';
      $('#docs-attachments-list').html(html);
    } catch (e) {
      $('#docs-attachments-list').html('<div style="color:var(--p-high);font-size:12px">Failed to load attachments.</div>');
    }
  },

  async uploadDocAttachments(docId, fileList) {
    const files = Array.from(fileList || []);
    if (!files.length) return;
    const $list = $('#docs-attachments-list');
    for (let i = 0; i < files.length; i++) {
      const f = files[i];
      if (f.size > 25 * 1024 * 1024) {
        alert(`${f.name} is larger than 25MB and was skipped.`);
        continue;
      }
      const fd = new FormData();
      fd.append('file', f);
      const upId = 'upload-prog-' + Date.now() + '-' + i;
      $list.prepend(`<div class="docs-attachment-row" id="${upId}"><span class="spinner"></span> Uploading ${this.esc(f.name)}…</div>`);
      try {
        await $.ajax({
          url: `/api/documents/${docId}/attachments`, method: 'POST',
          data: fd, processData: false, contentType: false,
        });
        $('#' + upId).remove();
      } catch (e) {
        $('#' + upId).remove();
        const msg = e.status === 413 ? 'File too large (max 25MB)' : (e.responseJSON?.error || e.statusText || 'Upload failed');
        alert(`Failed to upload ${f.name}: ${msg}`);
      }
    }
    // Reset the file input so the same file can be re-selected
    $('#doc-attachment-input').val('');
    await this.loadDocAttachmentsInline(docId);
  },

  downloadDocAttachment(docId, attachmentId, filename) {
    // Use XHR with blob so the auth header is sent
    $.ajax({
      url: `/api/documents/${docId}/attachments/${attachmentId}/download`,
      method: 'GET',
      xhrFields: { responseType: 'blob' },
    }).done(function(blob) {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(() => URL.revokeObjectURL(url), 5000);
    }).fail(function(e) {
      alert('Download failed: ' + (e.statusText || 'Unknown error'));
    });
  },

  async deleteDocAttachment(docId, attachmentId) {
    if (!confirm('Remove this attachment? This cannot be undone.')) return;
    try {
      await $.ajax({ url: `/api/documents/${docId}/attachments/${attachmentId}`, method: 'DELETE' });
      await this.loadDocAttachmentsInline(docId);
    } catch (e) {
      alert('Failed to remove attachment: ' + (e.responseJSON?.error || e.statusText));
    }
  },

  relDate(d) {
    if (!d) return '';
    try { return new Date(d).toLocaleDateString('en-US',{month:'short',day:'numeric'}); } catch(e) { return d; }
  },

  relDateTime(d) {
    if (!d) return '';
    try {
      const dt = new Date(d);
      const now = new Date();
      const diffMs = now - dt;
      const diffMin = Math.floor(diffMs / 60000);
      if (diffMin < 1) return 'just now';
      if (diffMin < 60) return `${diffMin}m ago`;
      const diffH = Math.floor(diffMin / 60);
      if (diffH < 24) return `${diffH}h ago`;
      const diffD = Math.floor(diffH / 24);
      if (diffD < 7) return `${diffD}d ago`;
      return dt.toLocaleDateString('en-US',{month:'short',day:'numeric'});
    } catch(e) { return d; }
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
