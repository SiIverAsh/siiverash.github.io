(() => {
    'use strict';

    const dataEl = document.getElementById('home-site-data');
    if (!dataEl) return;

    let SITE_DATA = {};
    try {
        SITE_DATA = JSON.parse(dataEl.textContent || '{}');
    } catch (err) {
        return;
    }

    const HOME_URL = SITE_DATA.homeUrl || '/';
    const SEARCH_URL = SITE_DATA.searchUrl || '/search.json';
    const SITE_TITLE = SITE_DATA.siteTitle || document.title || 'Home';
    const SITE_YEAR = SITE_DATA.siteYear || String(new Date().getFullYear());
    const CHANNELS = Array.isArray(SITE_DATA.channels) ? SITE_DATA.channels : [];
    const LEFT_FILMS = Array.isArray(SITE_DATA.leftFilms) ? SITE_DATA.leftFilms : [];
    const RIGHT_MODELS = Array.isArray(SITE_DATA.rightModels) ? SITE_DATA.rightModels : [];
    const ME_DATA = SITE_DATA.me || {};
    const SOCIAL_DATA = SITE_DATA.social || {};

    const POSTS = (Array.isArray(SITE_DATA.posts) ? SITE_DATA.posts : []).map((p) => {
        const plainExcerpt = String(p.excerpt || '').replace(/\s+/g, ' ').trim();
        return {
            date: p.date || '',
            dateTime: p.dateTime || p.date || '',
            updated: p.updated || '',
            title: p.title || '',
            cat: p.cat || 'emo',
            catName: p.catName || p.cat || '',
            hexNo: p.hexNo || '',
            url: p.url || '#',
            tags: Array.isArray(p.tags) ? p.tags : [],
            readTime: p.readTime || '1 min',
            excerpt: plainExcerpt,
            plainBody: plainExcerpt
        };
    });

    const TILTS = [-2.2, 1.6, -1.2, 2.0, -1.7, 1.4, -2.0, 1.5];
    const OFFSETS = [0, 12, 4, 16, 2, 14, 6, 10];
    const PAGE_SIZE = 8;
    const HOLD_DURATION = 1860;
    const FOCUS_LOCK_MS = 1320;
    const EXPOSURE_STEP_MS = 84;
    const EXPOSURE_FINAL = { shutter: '1/800', aperture: 'F4', iso: '64' };
    const EXPOSURE_TRIADS = [
        ['1/640', 'F2.8', '400'],
        ['1/320', 'F5.6', '200'],
        ['1/125', 'F2', '800'],
        ['1/250', 'F8', '160'],
        ['1/500', 'F3.5', '320'],
        ['1/80', 'F11', '100'],
        ['1/160', 'F1.8', '640'],
        ['1/400', 'F5.6', '250']
    ];
    const SKIP_INTRO_ON_REPEAT = true;
    const INTRO_SEEN_KEY = 'evf_intro_seen';

    const body = document.body;
    const root = document.documentElement;
    const reduceMotionQuery = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
    const darkSchemeQuery = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

    const shutterFill = document.getElementById('shutter-progress-fill');
    const shutterVal = document.getElementById('evf-shutter-val');
    const apertureVal = document.getElementById('evf-aperture-val');
    const isoVal = document.getElementById('evf-iso-val');
    const mainPanel = document.getElementById('main-panel');
    const focusFrame = document.getElementById('evf-focus-frame');

    const deckPrevBtn = document.getElementById('deck-prev-btn');
    const deckNextBtn = document.getElementById('deck-next-btn');

    const readerBackdrop = document.getElementById('post-reader-backdrop');
    const readerMeta = document.getElementById('reader-meta');
    const readerTitle = document.getElementById('reader-title');
    const readerTags = document.getElementById('reader-tags');
    const readerBody = document.getElementById('reader-body');
    const readerScroll = document.getElementById('reader-scroll');

    const reelBackdrop = document.getElementById('film-reel-backdrop');
    const reelTrack = document.getElementById('film-reel-track');
    const reelTabs = document.getElementById('film-reel-tabs');

    const sideReelBackdrop = document.getElementById('side-reel-backdrop');
    const sideReelViewport = document.getElementById('side-reel-viewport');
    const sideReelList = document.getElementById('side-reel-list');

    const searchBackdrop = document.getElementById('search-vf-backdrop');
    const searchVfInput = document.getElementById('search-vf-input');
    const searchVfCount = document.getElementById('search-vf-count');
    const searchVfResults = document.getElementById('search-vf-results');

    let activeCat = 'home';
    let currentPage = 1;
    let pendingDirection = 0;
    let skipNextFloatIn = false;
    let pageAdvanceTimer = null;
    let filmSettle = null;
    let reelTimer = null;
    let evfTimer = null;
    let focusTimer = null;
    let exposureTimer = null;
    let dofTimer = null;
    let seqTimers = [];
    let evfPaused = false;
    let elapsedMs = 0;
    let shutterBusy = false;

    let lastFilteredPosts = [];
    let activeReelKey = 'about';
    let sideDragRaf = null;
    let searchMatchedPosts = [];
    let searchSelectedIdx = 0;
    let readerHistoryClosing = false;
    let pendingReaderPost = null;
    let activePostRequestId = 0;
    const postHtmlCache = new Map();
    const postPromiseCache = new Map();
    let katexLoadPromise = null;

    let searchIndexLoaded = false;
    let searchIndexPromise = null;

    function prefersReducedMotion() {
        return !!(reduceMotionQuery && reduceMotionQuery.matches);
    }

    function escapeHtml(str) {
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    function clearSeqTimers() {
        seqTimers.forEach((id) => clearTimeout(id));
        seqTimers = [];
        if (dofTimer) { clearTimeout(dofTimer); dofTimer = null; }
        if (pageAdvanceTimer) { clearTimeout(pageAdvanceTimer); pageAdvanceTimer = null; }
        if (reelTimer) { clearTimeout(reelTimer); reelTimer = null; }
    }

    function stopExposureHunt() {
        if (exposureTimer) {
            clearInterval(exposureTimer);
            exposureTimer = null;
        }
    }

    function setExposureFinal() {
        stopExposureHunt();
        if (shutterVal) shutterVal.textContent = EXPOSURE_FINAL.shutter;
        if (apertureVal) apertureVal.textContent = EXPOSURE_FINAL.aperture;
        if (isoVal) isoVal.textContent = EXPOSURE_FINAL.iso;
    }

    function startExposureHunt() {
        stopExposureHunt();
        if (!shutterVal || !apertureVal || !isoVal) return;

        let index = 0;
        const triads = EXPOSURE_TRIADS.slice();
        for (let i = triads.length - 1; i > 0; i -= 1) {
            const j = Math.floor(Math.random() * (i + 1));
            [triads[i], triads[j]] = [triads[j], triads[i]];
        }
        const applyTriad = (triad) => {
            shutterVal.textContent = triad[0];
            apertureVal.textContent = triad[1];
            isoVal.textContent = triad[2];
        };

        applyTriad(triads[0]);
        exposureTimer = setInterval(() => {
            index = (index + 1) % triads.length;
            applyTriad(triads[index]);
        }, EXPOSURE_STEP_MS);
    }

    function buildReelFrames() {
        const specs = (ME_DATA.game && ME_DATA.game.specs) || {};
        const equip = (ME_DATA.snap && ME_DATA.snap.equipment) || {};

        const gearLines = [
            equip.camera ? `机身：<code>${escapeHtml(equip.camera)}</code>` : '',
            equip.lens ? `挂机镜头：<code>${escapeHtml(equip.lens)}</code>` : ''
        ].filter(Boolean).join('<br>');

        const pcLines = [
            specs.cpu ? `CPU：<code>${escapeHtml(specs.cpu)}</code>` : '',
            specs.gpu ? `GPU：<code>${escapeHtml(specs.gpu)}</code>` : '',
            specs.ram ? `内存：<code>${escapeHtml(specs.ram)}</code>` : '',
            specs.storage ? `存储：<code>${escapeHtml(specs.storage).trim()}</code>` : ''
        ].filter(Boolean).join('<br>');

        return [
            { key: 'lead', stub: true, label: 'SILVERASH · Z8' },
            {
                key: 'about',
                meta: 'USST · Soft Engineering',
                title: 'About Me',
                icon: 'fas fa-user-astronaut',
                tab: '关于我',
                body: `
                    <h2>🎓 教育背景</h2>
                    <ul>
                        <li><strong>学校专业</strong>: USST、Soft Engineering、Master's Degree</li>
                        <li><strong>研究方向</strong>: LLM 、ASR etc.</li>
                    </ul>
                    <h2>💻 技术栈</h2>
                    <ul>
                        <li><strong>语言</strong>：Py、Cpp(studing)、 JAVA、 TS(Studing)、JS</li>
                        <li><strong>核心领域</strong>：Fullstack、RealtimeASR、AI algorithms。(假如给我三天Vibe)</li>
                    </ul>
                    <h2>🎨 个人爱好</h2>
                    <ul>
                        <li><strong>二次元</strong>：看动漫（）。</li>
                        <li><strong>绘画</strong>：苦手。</li>
                        <li><strong>音乐</strong>：无忌口。（ASMR也算音乐么？！）</li>
                        <li><strong>游戏</strong>：FPS、Gal、二次元手游等，无忌口。</li>
                        <li><strong>摄影</strong>：I AM NIKON ！</li>
                    </ul>
                    <h2>📬 联系我</h2>
                    <p>如果想与我聊聊、交朋友，欢迎通过底部胶片的社交链接联系我！</p>
                `
            },
            {
                key: 'gear',
                meta: 'Camera & Workstation',
                title: '摄影器材与桌面主机配置',
                icon: 'fas fa-camera',
                tab: '装备清单',
                body: `
                    <blockquote>I AM NIKON！一套稳定顺手的机身与镜头，和一台能跑实验与游戏的桌面主力。</blockquote>
                    <h2>摄影器材</h2>
                    <p>${gearLines || 'Nikon Z8 / Z 24-120mm f/4 S'}</p>
                    <h2>桌面主机</h2>
                    <p>${pcLines || 'Desktop Workstation'}</p>
                `
            },
            { key: 'tail', stub: true, label: 'Z 24-120 F/4 S' }
        ];
    }

    const REEL_FRAMES = buildReelFrames();

    function buildBottomItems() {
        const items = [
            { type: 'search', label: '检索', icon: 'fas fa-crosshairs' },
            { type: 'sheet', key: 'about', label: '关于我', icon: 'fas fa-user-astronaut' },
            { type: 'sheet', key: 'gear', label: '装备清单', icon: 'fas fa-camera' },
            { type: 'side', side: 'left', label: '胶片片号', icon: 'fas fa-film', mobileOnly: true },
            { type: 'side', side: 'right', label: 'AI 模型', icon: 'fas fa-microchip', mobileOnly: true },
            { type: 'replay', label: '重拍开场', icon: 'fas fa-rotate-left' }
        ];
        if (SOCIAL_DATA.github) items.push({ type: 'link', label: 'GitHub', icon: 'fab fa-github', href: SOCIAL_DATA.github });
        if (SOCIAL_DATA.twitter) items.push({ type: 'link', label: 'X', icon: 'fab fa-twitter', href: SOCIAL_DATA.twitter });
        if (SOCIAL_DATA.pixiv) items.push({ type: 'link', label: 'Pixiv', icon: 'fas fa-image', href: SOCIAL_DATA.pixiv });
        if (SOCIAL_DATA.email) {
            const mailHref = SOCIAL_DATA.email.startsWith('mailto:') ? SOCIAL_DATA.email : `mailto:${SOCIAL_DATA.email}`;
            items.push({ type: 'link', label: 'Email', icon: 'fas fa-envelope', href: mailHref });
        }
        items.push({
            type: 'info',
            label: `© ${SITE_YEAR} SilverAsh · Built with Actions & Jekyll`,
            icon: 'fab fa-github'
        });
        items.push({ type: 'visitor', label: '总访问量', icon: 'fas fa-eye' });
        return items;
    }

    function renderPerimeterFilms() {
        const repeat2 = (arr) => [...arr, ...arr];
        const repeat4 = (arr) => [...arr, ...arr, ...arr, ...arr];

        const topHtml = repeat4(CHANNELS).map((c, i) => {
            const searchFrame = i % CHANNELS.length === 0
                ? '<button class="para-cell-x search-cell" type="button" data-action="search"><span><i class="fas fa-crosshairs"></i> 检索</span></button>'
                : '';
            return searchFrame + `
                <button class="para-cell-x ${c.key === activeCat ? 'active' : ''}" data-cat="${escapeHtml(c.key)}">
                    <span>
                        <i class="fas ${escapeHtml(c.icon)}"></i>
                        ${escapeHtml(c.name)}
                    </span>
                </button>`;
        }).join('');
        document.getElementById('film-top-track').innerHTML = topHtml;

        document.getElementById('film-left-track').innerHTML = repeat2(LEFT_FILMS).map((label, i) => `
            <div class="para-cell-y" data-side="left" data-side-idx="${i % LEFT_FILMS.length}"><span>${escapeHtml(label)}</span></div>
        `).join('');

        document.getElementById('film-right-track').innerHTML = repeat2(RIGHT_MODELS).map((label, i) => `
            <div class="para-cell-y" data-side="right" data-side-idx="${i % RIGHT_MODELS.length}"><span>${escapeHtml(label)}</span></div>
        `).join('');

        const renderBottomItem = (item) => {
            if (item.type === 'link') {
                const extra = item.href.startsWith('http') ? ' target="_blank" rel="noopener noreferrer"' : '';
                return `<a class="para-cell-x static-cell" href="${escapeHtml(item.href)}"${extra}><span><i class="${item.icon}"></i> ${escapeHtml(item.label)}</span></a>`;
            }
            if (item.type === 'search') {
                return `<button class="para-cell-x static-cell search-cell" type="button" data-action="search"><span><i class="${item.icon}"></i> ${item.label}</span></button>`;
            }
            if (item.type === 'side') {
                const cls = item.mobileOnly ? ' mobile-only-cell' : '';
                return `<button class="para-cell-x static-cell${cls}" type="button" data-open-side="${item.side}"><span><i class="${item.icon}"></i> ${item.label}</span></button>`;
            }
            if (item.type === 'replay') {
                return `<button class="para-cell-x static-cell" type="button" data-action="replay"><span><i class="${item.icon}"></i> ${item.label}</span></button>`;
            }
            if (item.type === 'sheet') {
                return `<button class="para-cell-x static-cell" type="button" data-sheet="${item.key}"><span><i class="${item.icon}"></i> ${item.label}</span></button>`;
            }
            if (item.type === 'info') {
                return `<span class="para-cell-x static-cell info-cell"><span><i class="${item.icon}"></i> ${escapeHtml(item.label)}</span></span>`;
            }
            if (item.type === 'visitor') {
                return `<span class="para-cell-x static-cell info-cell visitor-cell" hidden><span><i class="${item.icon}"></i> ${escapeHtml(item.label)} <strong data-visitor-count>--</strong></span></span>`;
            }
            return `<button class="para-cell-x static-cell" type="button" data-cat="${escapeHtml(item.key)}"><span><i class="${item.icon}"></i> ${escapeHtml(item.label)}</span></button>`;
        };

        document.getElementById('film-bottom-track').innerHTML = repeat4(buildBottomItems()).map(renderBottomItem).join('');

        document.querySelectorAll('.film-edge [data-cat]').forEach((el) => {
            el.addEventListener('click', () => selectCategory(el.dataset.cat));
        });
        document.querySelectorAll('.film-edge [data-action="replay"]').forEach((el) => {
            el.addEventListener('click', () => startViewfinderSequence({ forceReplay: true }));
        });
        document.querySelectorAll('.film-edge [data-action="search"]').forEach((el) => {
            el.addEventListener('click', openViewfinderSearch);
        });
        document.querySelectorAll('.film-edge [data-open-side]').forEach((el) => {
            el.addEventListener('click', () => openSideReel(el.dataset.openSide, 0));
        });
        document.querySelectorAll('.film-edge [data-sheet]').forEach((el) => {
            el.addEventListener('click', () => openFilmReel(el.dataset.sheet));
        });
    }

    function updateActiveChannelState() {
        document.querySelectorAll('.film-edge [data-cat]').forEach((el) => {
            el.classList.toggle('active', el.dataset.cat === activeCat);
        });
    }

    // ---------- 底部专题胶片 ----------
    function renderFilmReel() {
        const realFrames = REEL_FRAMES.filter((f) => !f.stub);
        reelTabs.innerHTML = realFrames.map((f) => `
            <button class="reel-tab-btn" type="button" data-reel-tab="${f.key}">
                <i class="${f.icon}"></i> ${f.tab}
            </button>
        `).join('');

        reelTrack.innerHTML = REEL_FRAMES.map((f) => {
            if (f.stub) {
                return `<div class="reel-frame is-stub" data-reel-key="${f.key}">${f.label}</div>`;
            }
            return `
                <article class="reel-frame" data-reel-key="${f.key}">
                    <header class="reel-frame-head">
                        <span>${f.meta}</span>
                    </header>
                    <div class="reel-frame-body">
                        <h2 class="reel-frame-title" style="border:none;padding:0;margin:0 0 12px;">${f.title}</h2>
                        ${f.body}
                    </div>
                </article>
            `;
        }).join('');

        reelTabs.querySelectorAll('[data-reel-tab]').forEach((btn) => {
            btn.addEventListener('click', () => rollToReelFrame(btn.dataset.reelTab));
        });

        reelTrack.querySelectorAll('.reel-frame[data-reel-key]:not(.is-stub)').forEach((frame) => {
            frame.addEventListener('click', () => {
                const key = frame.dataset.reelKey;
                if (key !== activeReelKey) rollToReelFrame(key);
            });
        });
    }

    function setActiveReelState(key) {
        activeReelKey = key;
        reelTabs.querySelectorAll('[data-reel-tab]').forEach((btn) => {
            btn.classList.toggle('active', btn.dataset.reelTab === key);
        });
        reelTrack.querySelectorAll('.reel-frame').forEach((frame) => {
            frame.classList.toggle('is-active', frame.dataset.reelKey === key);
        });
    }

    function positionReelTrack(key, { instant = false } = {}) {
        const frame = reelTrack.querySelector(`.reel-frame[data-reel-key="${key}"]`);
        if (!frame) return;
        const targetX = window.innerWidth / 2 - (frame.offsetLeft + frame.offsetWidth / 2);
        if (instant) {
            reelTrack.classList.add('instant');
            reelTrack.style.transform = `translateX(${targetX}px)`;
            void reelTrack.offsetWidth;
            reelTrack.classList.remove('instant');
            return;
        }
        reelTrack.style.transform = `translateX(${targetX}px)`;
    }

    function rollToReelFrame(key) {
        setActiveReelState(key);
        positionReelTrack(key, { instant: false });
    }

    function openFilmReel(targetKey) {
        if (!REEL_FRAMES.some((f) => !f.stub && f.key === targetKey)) return;
        closePostReader({ immediate: true });
        closeSideReel();
        if (reelTimer) { clearTimeout(reelTimer); reelTimer = null; }

        body.classList.add('intro-settled');

        if (body.classList.contains('reel-open')) {
            rollToReelFrame(targetKey);
            return;
        }

        setActiveReelState('lead');
        positionReelTrack('lead', { instant: true });

        body.classList.add('reel-open');
        reelBackdrop.setAttribute('aria-hidden', 'false');

        if (prefersReducedMotion()) {
            setActiveReelState(targetKey);
            positionReelTrack(targetKey, { instant: true });
            return;
        }

        reelTimer = setTimeout(() => {
            rollToReelFrame(targetKey);
        }, 220);
    }

    function closeFilmReel() {
        if (reelTimer) { clearTimeout(reelTimer); reelTimer = null; }
        body.classList.remove('reel-open');
        reelBackdrop.setAttribute('aria-hidden', 'true');
    }

    // ---------- 左右两侧胶片抽屉 ----------
    function stopSideDragMomentum() {
        if (sideDragRaf) {
            cancelAnimationFrame(sideDragRaf);
            sideDragRaf = null;
        }
    }

    function openSideReel(side, focusIdx = 0) {
        if (side !== 'left' && side !== 'right') return;
        closePostReader({ immediate: true });
        closeFilmReel();
        stopSideDragMomentum();

        const items = side === 'left' ? LEFT_FILMS : RIGHT_MODELS;

        sideReelList.innerHTML = items.map((name, i) => `
            <div class="side-reel-item ${i === focusIdx ? 'is-highlight' : ''}" data-item-idx="${i}">
                <span>${escapeHtml(name)}</span>
            </div>
        `).join('');

        body.classList.add('intro-settled');
        body.classList.remove('side-reel-open', 'side-reel-left', 'side-reel-right');
        body.classList.add(side === 'left' ? 'side-reel-left' : 'side-reel-right');
        void sideReelBackdrop.offsetWidth;

        requestAnimationFrame(() => {
            body.classList.add('side-reel-open');
            sideReelBackdrop.setAttribute('aria-hidden', 'false');
            const targetEl = sideReelList.querySelector(`[data-item-idx="${focusIdx}"]`);
            if (targetEl) {
                sideReelViewport.scrollTop = Math.max(0, targetEl.offsetTop - sideReelViewport.clientHeight * 0.32);
            } else {
                sideReelViewport.scrollTop = 0;
            }
        });
    }

    function closeSideReel() {
        stopSideDragMomentum();
        body.classList.remove('side-reel-open');
        sideReelBackdrop.setAttribute('aria-hidden', 'true');
    }

    function initSideReelDrag() {
        let dragging = false;
        let startY = 0;
        let startScroll = 0;
        let lastY = 0;
        let lastTime = 0;
        let velocity = 0;

        sideReelViewport.addEventListener('pointerdown', (e) => {
            if (e.button !== 0) return;
            stopSideDragMomentum();
            dragging = true;
            startY = e.clientY;
            startScroll = sideReelViewport.scrollTop;
            lastY = e.clientY;
            lastTime = performance.now();
            velocity = 0;
            sideReelViewport.classList.add('is-dragging');
            sideReelViewport.setPointerCapture(e.pointerId);
        });

        sideReelViewport.addEventListener('pointermove', (e) => {
            if (!dragging) return;
            const now = performance.now();
            const dt = Math.max(8, now - lastTime);
            const dy = e.clientY - startY;
            sideReelViewport.scrollTop = startScroll - dy;
            const instV = (lastY - e.clientY) / dt;
            velocity = velocity * 0.45 + instV * 0.55;
            lastY = e.clientY;
            lastTime = now;
        });

        const endDrag = (e) => {
            if (!dragging) return;
            dragging = false;
            sideReelViewport.classList.remove('is-dragging');
            if (e && e.pointerId !== undefined && sideReelViewport.hasPointerCapture(e.pointerId)) {
                sideReelViewport.releasePointerCapture(e.pointerId);
            }
            if (Math.abs(velocity) < 0.04) return;
            let prevTs = performance.now();
            const step = (ts) => {
                const dt = Math.min(32, ts - prevTs);
                prevTs = ts;
                sideReelViewport.scrollTop += velocity * dt;
                velocity *= Math.pow(0.92, dt / 16);
                if (Math.abs(velocity) > 0.025) {
                    sideDragRaf = requestAnimationFrame(step);
                } else {
                    sideDragRaf = null;
                }
            };
            sideDragRaf = requestAnimationFrame(step);
        };

        sideReelViewport.addEventListener('pointerup', endDrag);
        sideReelViewport.addEventListener('pointercancel', endDrag);
    }

    // ---------- 浅景深正文阅读层 + 真实文章抓取 ----------
    function hasMathMarkup(content) {
        const ignoredTags = new Set(['SCRIPT', 'NOSCRIPT', 'STYLE', 'TEXTAREA', 'PRE', 'CODE']);
        const mathDelimiters = /\$\$[\s\S]*?\$\$|\$[^$]*?\$|\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]/;
        const walker = document.createTreeWalker(content, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, {
            acceptNode(node) {
                return node.nodeType === Node.ELEMENT_NODE && ignoredTags.has(node.tagName)
                    ? NodeFilter.FILTER_REJECT
                    : NodeFilter.FILTER_ACCEPT;
            }
        });
        while (walker.nextNode()) {
            if (walker.currentNode.nodeType === Node.TEXT_NODE && mathDelimiters.test(walker.currentNode.textContent)) {
                return true;
            }
        }
        return false;
    }

    function ensureKatexLoaded() {
        if (typeof window.renderMathInElement === 'function') return Promise.resolve();
        if (katexLoadPromise) return katexLoadPromise;

        katexLoadPromise = new Promise((resolve) => {
            if (!document.querySelector('link[data-vf-katex]')) {
                const link = document.createElement('link');
                link.rel = 'stylesheet';
                link.href = HOME_URL + 'assets/vendor/katex/katex.min.css';
                link.setAttribute('data-vf-katex', '1');
                document.head.appendChild(link);
            }

            const loadScript = (src) => new Promise((res, rej) => {
                const s = document.createElement('script');
                s.src = src;
                s.async = true;
                s.onload = res;
                s.onerror = rej;
                document.head.appendChild(s);
            });

            loadScript(HOME_URL + 'assets/vendor/katex/katex.min.js')
                .then(() => loadScript(HOME_URL + 'assets/vendor/katex/auto-render.min.js'))
                .then(resolve)
                .catch(() => {
                    katexLoadPromise = null;
                    resolve();
                });
        });

        return katexLoadPromise;
    }

    readerBody.addEventListener('click', (e) => {
        const copyBtn = e.target.closest('.reader-code-copy');
        if (!copyBtn || !navigator.clipboard) return;
        const box = copyBtn.closest('.reader-code-box');
        const preEl = box && box.querySelector('pre');
        if (!preEl) return;
        const text = preEl.innerText || preEl.textContent || '';
        navigator.clipboard.writeText(text).then(() => {
            copyBtn.textContent = 'Copied';
            setTimeout(() => { copyBtn.textContent = 'Copy'; }, 1600);
        }).catch(() => {});
    });

    async function decorateReaderHtml(rawHtml) {
        const temp = document.createElement('div');
        temp.innerHTML = rawHtml;

        temp.querySelectorAll('div.highlighter-rouge, pre').forEach((node) => {
            if (node.closest('.reader-code-box')) return;
            let lang = 'CODE';
            const langMatch = node.className && node.className.match(/language-([^\s]+)/);
            if (langMatch) lang = langMatch[1].toUpperCase();

            const preEl = node.tagName === 'PRE' ? node : node.querySelector('pre');
            if (!preEl) return;
            if (!langMatch && preEl.className) {
                const innerMatch = preEl.className.match(/language-([^\s]+)/);
                if (innerMatch) lang = innerMatch[1].toUpperCase();
            }

            const box = document.createElement('div');
            box.className = 'reader-code-box';

            const head = document.createElement('div');
            head.className = 'reader-code-head';
            head.innerHTML = `
                <span class="reader-code-dots"><i></i><i></i><i></i></span>
                <span>${escapeHtml(lang)}</span>
                <button class="reader-code-copy" type="button">Copy</button>
            `;

            box.appendChild(head);
            node.replaceWith(box);
            box.appendChild(preEl);
        });

        temp.querySelectorAll('img').forEach((img) => {
            if (!img.hasAttribute('loading')) img.setAttribute('loading', 'lazy');
            if (!img.hasAttribute('decoding')) img.setAttribute('decoding', 'async');
        });

        if (hasMathMarkup(temp)) {
            await ensureKatexLoaded();
            if (typeof window.renderMathInElement === 'function') {
                try {
                    window.renderMathInElement(temp, {
                        delimiters: [
                            { left: '$$', right: '$$', display: true },
                            { left: '$', right: '$', display: false },
                            { left: '\\(', right: '\\)', display: false },
                            { left: '\\[', right: '\\]', display: true }
                        ],
                        throwOnError: false,
                        ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
                    });
                } catch (err) {}
            }
        }

        return temp.innerHTML;
    }

    function loadPostContent(post) {
        if (!post || !post.url || post.url === '#') {
            return Promise.resolve(`<p>${escapeHtml(post ? post.excerpt : '')}</p>`);
        }
        if (postHtmlCache.has(post.url)) {
            return Promise.resolve(postHtmlCache.get(post.url));
        }
        if (postPromiseCache.has(post.url)) {
            return postPromiseCache.get(post.url);
        }

        const promise = (async () => {
            const res = await fetch(post.url, { credentials: 'same-origin' });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const htmlText = await res.text();
            const doc = new DOMParser().parseFromString(htmlText, 'text/html');
            const contentEl = doc.querySelector('.post-content');
            const extracted = contentEl ? contentEl.innerHTML : `<p>${escapeHtml(post.excerpt || post.title)}</p>`;
            const decorated = await decorateReaderHtml(extracted);
            postHtmlCache.set(post.url, decorated);
            return decorated;
        })();

        postPromiseCache.set(post.url, promise);
        promise.catch(() => {
            postPromiseCache.delete(post.url);
        });
        return promise;
    }

    function applyReaderContent(html) {
        readerBody.innerHTML = html;
        readerScroll.scrollTop = 0;
    }

    function getDofTier(distancePx) {
        if (distancePx < 290) return { scale: '0.985', opacity: '0.86' };
        if (distancePx < 520) return { scale: '0.955', opacity: '0.68' };
        if (distancePx < 780) return { scale: '0.925', opacity: '0.50' };
        return { scale: '0.90', opacity: '0.36' };
    }

    function openPostWithDof(targetCard, post, clickEvent, { fromHistory = false } = {}) {
        if (!targetCard || !post) return;
        // history.back() completes asynchronously. Open the next article only after
        // that traversal has reached the home entry, so it cannot close a new reader.
        if (readerHistoryClosing && !fromHistory) {
            pendingReaderPost = { post, category: activeCat };
            return;
        }
        if (dofTimer) { clearTimeout(dofTimer); dofTimer = null; }
        closeFilmReel();
        closeSideReel();
        body.classList.add('intro-settled');

        const targetSlot = targetCard.closest('.photo-print-slot');
        const targetRect = targetCard.getBoundingClientRect();
        const focusX = clickEvent && typeof clickEvent.clientX === 'number'
            ? clickEvent.clientX
            : targetRect.left + targetRect.width / 2;
        const focusY = clickEvent && typeof clickEvent.clientY === 'number'
            ? clickEvent.clientY
            : targetRect.top + targetRect.height / 2;

        // 先批量读取布局几何，再统一写入 class/style，避免循环内强制同步重排
        const slotMeasurements = Array.from(document.querySelectorAll('.photo-print-slot')).map((slot) => {
            const card = slot.querySelector('.photo-print');
            if (slot === targetSlot) {
                return { slot, card, isTarget: true, tier: null };
            }
            const rect = slot.getBoundingClientRect();
            const dist = Math.hypot(rect.left + rect.width / 2 - focusX, rect.top + rect.height / 2 - focusY);
            return { slot, card, isTarget: false, tier: getDofTier(dist) };
        });

        slotMeasurements.forEach(({ slot, card, isTarget, tier }) => {
            slot.classList.remove('is-target', 'is-blurred');
            if (isTarget) {
                slot.classList.add('is-target');
                slot.style.removeProperty('--dof-scale');
                slot.style.removeProperty('--dof-opacity');
                if (card) card.classList.add('dof-target');
                return;
            }
            slot.classList.add('is-blurred');
            slot.style.setProperty('--dof-scale', tier.scale);
            slot.style.setProperty('--dof-opacity', tier.opacity);
            if (card) card.classList.remove('dof-target');
        });

        body.classList.add('dof-active');
        root.classList.add('reader-scroll-locked');

        const updatedMeta = post.updated
            ? `<span class="reader-updated" title="最后修改日期">更新 ${escapeHtml(post.updated)}</span>`
            : '';
        readerMeta.innerHTML = `
            <span class="reader-cat-badge">${escapeHtml(post.catName)}</span>
            <span title="发布日期">${escapeHtml(post.dateTime || post.date)}</span>
            ${updatedMeta}
            <span>${escapeHtml(post.readTime || '1 min')}</span>
        `;
        readerTitle.textContent = post.title;
        readerTags.innerHTML = (post.tags || []).map((t) => `<span class="post-reader-tag">#${escapeHtml(t)}</span>`).join('');
        readerScroll.scrollTop = 0;

        if (!fromHistory && post.url && post.url !== '#') {
            try {
                const state = { vfPostUrl: post.url, vfCategory: activeCat };
                const title = `${post.title} - ${SITE_TITLE}`;
                if (history.state?.vfPostUrl || window.location.pathname === new URL(post.url, window.location.href).pathname) {
                    history.replaceState(state, title, post.url);
                } else {
                    history.pushState(state, title, post.url);
                }
            } catch (err) {}
        }

        const reqId = ++activePostRequestId;
        if (postHtmlCache.has(post.url)) {
            applyReaderContent(postHtmlCache.get(post.url));
        } else {
            readerBody.innerHTML = `
                <div class="reader-loading">
                    <i class="fas fa-circle-notch fa-spin"></i>
                    <span>正在对焦读取正文…</span>
                </div>
            `;
            loadPostContent(post).then((html) => {
                if (reqId !== activePostRequestId || !body.classList.contains('dof-active')) return;
                applyReaderContent(html);
            }).catch(() => {
                if (reqId !== activePostRequestId || !body.classList.contains('dof-active')) return;
                readerBody.innerHTML = `
                    <blockquote>当前环境暂无法异步读取该页面正文，已展示文章摘要。</blockquote>
                    <p>${escapeHtml(post.excerpt || post.title)}</p>
                    <p><a href="${escapeHtml(post.url)}">前往独立文章页面阅读全文 →</a></p>
                `;
            });
        }

        dofTimer = setTimeout(() => {
            body.classList.add('reader-open');
            readerBackdrop.setAttribute('aria-hidden', 'false');
        }, prefersReducedMotion() ? 0 : 160);
    }

    function syncUrlBackToHome() {
        readerHistoryClosing = false;
        try {
            if (window.location.pathname !== new URL(HOME_URL, window.location.href).pathname) {
                history.replaceState(null, SITE_TITLE, HOME_URL);
            }
        } catch (err) {}
    }

    function closePostReader({ immediate = false, fromPopState = false } = {}) {
        if (!fromPopState) pendingReaderPost = null;
        if (dofTimer) { clearTimeout(dofTimer); dofTimer = null; }
        activePostRequestId++;
        body.classList.remove('reader-open');
        readerBackdrop.setAttribute('aria-hidden', 'true');

        if (!fromPopState && !readerHistoryClosing) {
            if (history.state?.vfPostUrl) {
                readerHistoryClosing = true;
                try {
                    history.back();
                } catch (err) {
                    syncUrlBackToHome();
                }
            } else {
                syncUrlBackToHome();
            }
        }

        const clearDofState = () => {
            body.classList.remove('dof-active');
            root.classList.remove('reader-scroll-locked');
            document.querySelectorAll('.photo-print-slot').forEach((slot) => {
                slot.classList.remove('is-target', 'is-blurred');
                slot.style.removeProperty('--dof-scale');
                slot.style.removeProperty('--dof-opacity');
                const card = slot.querySelector('.photo-print');
                if (card) card.classList.remove('dof-target');
            });
        };

        if (immediate) {
            clearDofState();
            return;
        }

        dofTimer = setTimeout(clearDofState, 180);
    }

    // ---------- 桌面卡片与整桌左右翻页 ----------
    function bindPhotoTilt() {
        const allowPrefetch = !(navigator.connection && navigator.connection.saveData);
        document.querySelectorAll('.photo-print').forEach((card) => {
            let tiltRaf = null;
            let lastPointerX = 0;
            let lastPointerY = 0;
            let prefetchTimer = null;

            card.addEventListener('mouseenter', () => {
                if (!allowPrefetch || body.classList.contains('dof-active')) return;
                const post = lastFilteredPosts[Number(card.dataset.postIdx)];
                if (!post || !post.url || post.url === '#' || postHtmlCache.has(post.url)) return;
                prefetchTimer = setTimeout(() => {
                    loadPostContent(post).catch(() => {});
                }, 140);
            });

            card.addEventListener('mousemove', (e) => {
                if (body.classList.contains('dof-active')) return;
                lastPointerX = e.clientX;
                lastPointerY = e.clientY;
                if (tiltRaf) return;
                tiltRaf = requestAnimationFrame(() => {
                    tiltRaf = null;
                    if (body.classList.contains('dof-active')) return;
                    card.classList.add('is-tilting');
                    const rect = card.getBoundingClientRect();
                    const x = (lastPointerX - rect.left) / rect.width - 0.5;
                    const y = (lastPointerY - rect.top) / rect.height - 0.5;
                    card.style.transform = `translateY(-10px) scale(1.04) rotateX(${(-y * 8).toFixed(2)}deg) rotateY(${(x * 8).toFixed(2)}deg)`;
                });
            });
            card.addEventListener('mouseleave', () => {
                if (prefetchTimer) { clearTimeout(prefetchTimer); prefetchTimer = null; }
                if (tiltRaf) { cancelAnimationFrame(tiltRaf); tiltRaf = null; }
                card.classList.remove('is-tilting');
                card.style.transform = '';
            });
            card.addEventListener('click', (e) => {
                if (body.classList.contains('dof-active')) return;
                if (prefetchTimer) { clearTimeout(prefetchTimer); prefetchTimer = null; }
                const idx = Number(card.dataset.postIdx);
                openPostWithDof(card, lastFilteredPosts[idx], e);
            });
        });
    }

    function getFilteredPosts() {
        return POSTS.filter((p) => activeCat === 'home' || p.cat === activeCat);
    }

    function updateDeckSideNav(totalPages) {
        const showPrev = totalPages > 1 && currentPage > 1;
        const showNext = totalPages > 1 && currentPage < totalPages;
        deckPrevBtn.classList.toggle('is-visible', showPrev);
        deckNextBtn.classList.toggle('is-visible', showNext);
    }

    function goToPage(targetPage, explicitDir) {
        if (body.classList.contains('dof-active')) return;
        const filtered = getFilteredPosts();
        const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
        const next = Math.min(totalPages, Math.max(1, targetPage));
        if (next === currentPage) return;

        const dir = explicitDir || (next > currentPage ? 1 : -1);
        if (pageAdvanceTimer) { clearTimeout(pageAdvanceTimer); pageAdvanceTimer = null; }
        // 上一趟还没收片（快速连点 next/prev）：先把片带收掉，
        // 否则下面查到 .panel-swap 会命中片带里的旧格，越套越深。
        if (filmSettle) filmSettle();

        const swapEl = mainPanel.querySelector('.panel-swap');
        if (swapEl && !prefersReducedMotion()) {
            // 走片：把旧的一格和新的一格并排塞进同一条片带（.film-rail），
            // 整条带子只跑一个 transform，横移一格。带子自己铺片基和片孔，
            // 两格各自缩到 74% 像压在底片上，落片后新格再拉近放大。
            const ghost = swapEl.cloneNode(true);
            ghost.classList.remove('advance-next', 'advance-prev', 'skip-float-in', 'film-frame-in');
            ghost.classList.add('film-frame-out');

            currentPage = next;
            pendingDirection = 0;
            renderMainPanel();

            const fresh = mainPanel.firstElementChild;
            if (fresh && fresh.classList.contains('panel-swap')) {
                fresh.classList.add('film-frame-in');
                const rail = document.createElement('div');
                rail.className = `film-rail ${dir > 0 ? 'advance-next' : 'advance-prev'}`;
                if (dir > 0) {
                    rail.appendChild(ghost);
                    rail.appendChild(fresh);
                } else {
                    rail.appendChild(fresh);
                    rail.appendChild(ghost);
                }
                mainPanel.insertBefore(rail, mainPanel.firstChild);
                body.classList.add('film-advancing');

                let settled = false;
                const settleFilm = () => {
                    if (settled) return;
                    settled = true;
                    filmSettle = null;
                    if (pageAdvanceTimer) { clearTimeout(pageAdvanceTimer); pageAdvanceTimer = null; }
                    // 收片：新格落回主画布。得先戴上 skip-float-in，
                    // 否则脱离 .film-rail 的一瞬间卡片会从 opacity:0 重播入场；
                    // no-reveal 压住整格的 panelReveal，否则刚放大完会再淡入一次。
                    fresh.classList.add('skip-float-in', 'no-reveal');
                    fresh.classList.remove('film-frame-in');
                    // 片带可能已经被 renderMainPanel 的 innerHTML 冲掉了，
                    // 那就没什么可收回来的。
                    if (rail.parentNode === mainPanel) {
                        mainPanel.insertBefore(fresh, rail);
                    }
                    rail.remove();
                    body.classList.remove('film-advancing');
                };
                filmSettle = settleFilm;
                // 只认带子自己的 animationend：两个格子的缩放动画也会冒泡上来
                const onRailEnd = (event) => {
                    if (event.target !== rail) return;
                    rail.removeEventListener('animationend', onRailEnd);
                    settleFilm();
                };
                rail.addEventListener('animationend', onRailEnd);
                pageAdvanceTimer = setTimeout(settleFilm, 900);
                if (window.scrollY > 40) window.scrollTo({ top: 0, behavior: 'smooth' });
                return;
            }
        }

        currentPage = next;
        pendingDirection = dir;
        renderMainPanel();
        if (window.scrollY > 40) window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function renderMainPanel() {
        const filtered = getFilteredPosts();
        const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
        currentPage = Math.min(totalPages, Math.max(1, currentPage));
        updateDeckSideNav(totalPages);

        const startIdx = (currentPage - 1) * PAGE_SIZE;
        const pageItems = filtered.slice(startIdx, startIdx + PAGE_SIZE);
        lastFilteredPosts = pageItems;

        const swapClass = skipNextFloatIn
            ? 'panel-swap skip-float-in'
            : pendingDirection > 0
                ? 'panel-swap advance-next'
                : pendingDirection < 0
                    ? 'panel-swap advance-prev'
                    : 'panel-swap';
        pendingDirection = 0;
        skipNextFloatIn = false;

        const MAX_VISIBLE_DOTS = 8;
        let pageStart = 1;
        let pageEnd = totalPages;
        if (totalPages > MAX_VISIBLE_DOTS) {
            pageStart = Math.max(1, currentPage - Math.floor(MAX_VISIBLE_DOTS / 2) + 1);
            pageEnd = pageStart + MAX_VISIBLE_DOTS - 1;
            if (pageEnd > totalPages) {
                pageEnd = totalPages;
                pageStart = Math.max(1, pageEnd - MAX_VISIBLE_DOTS + 1);
            }
        }
        const visiblePages = Array.from({ length: pageEnd - pageStart + 1 }, (_, i) => pageStart + i);
        const showJumpPrev = totalPages > MAX_VISIBLE_DOTS && pageStart > 1;
        const showJumpNext = totalPages > MAX_VISIBLE_DOTS && pageEnd < totalPages;
        const jumpPrevTarget = Math.max(1, currentPage - MAX_VISIBLE_DOTS);
        const jumpNextTarget = Math.min(totalPages, currentPage + MAX_VISIBLE_DOTS);

        mainPanel.innerHTML = `
            <div class="${swapClass}">
                ${pageItems.length ? `
                    <div class="photo-table">
                        ${pageItems.map((p, idx) => `
                            <div class="photo-print-slot" style="--idx:${idx}; --offset-y:${OFFSETS[idx % OFFSETS.length]}px;">
                                <article class="photo-print" data-post-idx="${idx}" style="--idx:${idx}; --tilt:${TILTS[idx % TILTS.length]}deg;">
                                    <div class="card-af-brackets" aria-hidden="true">
                                        <span class="caf tl"></span>
                                        <span class="caf tr"></span>
                                        <span class="caf bl"></span>
                                        <span class="caf br"></span>
                                    </div>
                                    <div class="photo-face">
                                        ${p.hexNo ? `<span class="photo-hex-mark" aria-hidden="true">${escapeHtml(p.hexNo)}</span>` : ''}
                                        <div class="photo-cover-title">${escapeHtml(p.title)}</div>
                                    </div>
                                    <div class="photo-meta">
                                        <span>${escapeHtml(p.date)}</span>
                                        <span class="photo-cat">${escapeHtml(p.catName)}</span>
                                    </div>
                                </article>
                            </div>
                        `).join('')}
                    </div>
                    ${totalPages > 1 ? `
                        <div class="deck-dots-wrap" aria-label="桌面页数指示">
                            ${showJumpPrev ? `
                                <button class="deck-dot deck-jump prev" type="button" data-page-num="${jumpPrevTarget}" aria-label="向前 8 页（第 ${jumpPrevTarget} 桌）" title="向前 8 页（第 ${jumpPrevTarget} 桌）"></button>
                            ` : ''}
                            ${visiblePages.map((n) => `
                                <button class="deck-dot ${n === currentPage ? 'active' : ''}" type="button" data-page-num="${n}" title="第 ${n} 桌"></button>
                            `).join('')}
                            ${showJumpNext ? `
                                <button class="deck-dot deck-jump next" type="button" data-page-num="${jumpNextTarget}" aria-label="向后 8 页（第 ${jumpNextTarget} 桌）" title="向后 8 页（第 ${jumpNextTarget} 桌）"></button>
                            ` : ''}
                        </div>
                    ` : ''}
                ` : '<p style="color: rgba(255,255,255,0.78); padding: 24px 0;">该频道暂未收录文章</p>'}
            </div>
        `;

        mainPanel.querySelectorAll('[data-page-num]').forEach((btn) => {
            btn.addEventListener('click', () => goToPage(Number(btn.dataset.pageNum)));
        });

        bindPhotoTilt();
    }

    function selectCategory(cat) {
        closePostReader({ immediate: true });
        closeFilmReel();
        closeSideReel();
        closeViewfinderSearch();
        if (pageAdvanceTimer) { clearTimeout(pageAdvanceTimer); pageAdvanceTimer = null; }
        if (filmSettle) filmSettle();
        activeCat = cat;
        currentPage = 1;
        pendingDirection = 0;
        updateActiveChannelState();
        renderMainPanel();
    }

    // ---------- EVF 开场与快门 ----------
    function snapShutter() {
        if (shutterBusy || body.classList.contains('stage-workspace')) return;
        shutterBusy = true;

        if (evfTimer) { clearInterval(evfTimer); evfTimer = null; }
        if (focusTimer) { clearTimeout(focusTimer); focusTimer = null; }
        clearSeqTimers();
        setExposureFinal();

        try { sessionStorage.setItem(INTRO_SEEN_KEY, '1'); } catch (e) {}
        shutterFill.style.transform = 'scaleX(1)';
        body.classList.remove('evf-hunting');
        body.classList.add('evf-focused', 'shutter-closed');

        seqTimers.push(setTimeout(() => {
            body.classList.remove('shutter-closed');
            body.classList.add('evf-captured', 'shutter-flashing');

            seqTimers.push(setTimeout(() => {
                body.classList.remove('shutter-flashing');
            }, 130));

            seqTimers.push(setTimeout(() => {
                body.classList.add('evf-wind-away');

                seqTimers.push(setTimeout(() => {
                    body.classList.add('stage-workspace');
                    seqTimers.push(setTimeout(() => {
                        body.classList.add('intro-settled');
                    }, 1250));
                }, 580));

                seqTimers.push(setTimeout(() => {
                    body.classList.remove('evf-ready', 'evf-focused', 'evf-captured', 'evf-wind-away');
                    body.classList.add('evf-done');
                    shutterBusy = false;
                }, 1760));
            }, 720));
        }, 110));
    }

    function shouldSkipIntro() {
        const navEntry = performance.getEntriesByType && performance.getEntriesByType('navigation')[0];
        if (navEntry && navEntry.type === 'back_forward') return true;
        if (!SKIP_INTRO_ON_REPEAT) return false;
        try { return sessionStorage.getItem(INTRO_SEEN_KEY) === '1'; } catch (e) { return false; }
    }

    function startViewfinderSequence({ forceReplay = false } = {}) {
        closePostReader({ immediate: true });
        closeFilmReel();
        closeSideReel();
        closeViewfinderSearch();
        if (forceReplay) {
            try { sessionStorage.removeItem(INTRO_SEEN_KEY); } catch (e) {}
        }
        if (evfTimer) clearInterval(evfTimer);
        if (focusTimer) clearTimeout(focusTimer);
        stopExposureHunt();
        clearSeqTimers();
        shutterBusy = false;
        evfPaused = false;
        elapsedMs = 0;
        shutterFill.style.transform = 'scaleX(0)';

        body.classList.remove(
            'stage-workspace', 'intro-settled', 'reel-open',
            'side-reel-open', 'side-reel-left', 'side-reel-right', 'search-open',
            'evf-ready', 'evf-focused', 'evf-hunting',
            'shutter-closed', 'shutter-flashing',
            'evf-captured', 'evf-wind-away', 'evf-done'
        );

        if (prefersReducedMotion() || (!forceReplay && shouldSkipIntro())) {
            setExposureFinal();
            body.classList.add('stage-workspace', 'intro-settled', 'evf-done');
            return;
        }

        body.classList.add('evf-hunting');
        startExposureHunt();

        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                body.classList.add('evf-ready');
            });
        });

        focusTimer = setTimeout(() => {
            setExposureFinal();
            body.classList.remove('evf-hunting');
            body.classList.add('evf-focused');
        }, FOCUS_LOCK_MS);

        const step = 30;
        evfTimer = setInterval(() => {
            if (evfPaused) return;
            elapsedMs += step;
            shutterFill.style.transform = `scaleX(${Math.min(1, elapsedMs / HOLD_DURATION).toFixed(3)})`;
            if (elapsedMs >= HOLD_DURATION) {
                snapShutter();
            }
        }, step);
    }

    // ---------- 取景器全局检索（仅匹配博客标题与正文） ----------
    function loadSearchIndex() {
        if (searchIndexLoaded) return Promise.resolve();
        if (searchIndexPromise) return searchIndexPromise;

        searchIndexPromise = Promise.resolve()
            .then(() => fetch(SEARCH_URL, { credentials: 'same-origin' }))
            .then((res) => {
                if (!res.ok) throw new Error(`Search index returned HTTP ${res.status}`);
                return res.json();
            })
            .then((entries) => {
                if (!Array.isArray(entries)) throw new Error('Invalid search index');
                const byUrl = new Map();
                const byTitle = new Map();
                entries.forEach((item) => {
                    if (!item) return;
                    const bodyText = String(item.content || '').replace(/\s+/g, ' ').trim();
                    if (item.url) byUrl.set(item.url, bodyText);
                    if (item.title) byTitle.set(item.title, bodyText);
                });
                POSTS.forEach((post) => {
                    const matchedBody = byUrl.get(post.url) || byTitle.get(post.title);
                    if (matchedBody) post.plainBody = matchedBody;
                });
                searchIndexLoaded = true;
            })
            .catch(() => {})
            .finally(() => {
                searchIndexPromise = null;
            });

        return searchIndexPromise;
    }

    function highlightTerms(rawText, terms) {
        const safe = escapeHtml(rawText);
        if (!terms.length) return safe;
        const escapedTerms = terms
            .slice()
            .sort((a, b) => b.length - a.length)
            .map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
        const regex = new RegExp(`(${escapedTerms.join('|')})`, 'gi');
        return safe.replace(regex, '<mark class="vf-hl">$1</mark>');
    }

    function buildBodySnippet(plainBody, terms) {
        if (!plainBody) return '';
        if (!terms.length) {
            return plainBody.length > 96 ? plainBody.slice(0, 96) + '…' : plainBody;
        }
        const lower = plainBody.toLowerCase();
        let firstHit = -1;
        for (const term of terms) {
            const pos = lower.indexOf(term);
            if (pos !== -1 && (firstHit === -1 || pos < firstHit)) firstHit = pos;
        }
        if (firstHit === -1) {
            return plainBody.length > 96 ? plainBody.slice(0, 96) + '…' : plainBody;
        }
        const start = Math.max(0, firstHit - 26);
        const end = Math.min(plainBody.length, start + 104);
        return (start > 0 ? '…' : '') + plainBody.slice(start, end) + (end < plainBody.length ? '…' : '');
    }

    function searchBlogTitleAndBody(rawQuery) {
        const terms = rawQuery.trim().toLowerCase().split(/\s+/).filter(Boolean);
        if (!terms.length) {
            return { terms: [], items: POSTS.slice(0, 8) };
        }

        const scored = [];
        for (const post of POSTS) {
            const titleLower = post.title.toLowerCase();
            const bodyLower = post.plainBody.toLowerCase();
            let allMatched = true;
            let score = 0;

            for (const term of terms) {
                const inTitle = titleLower.includes(term);
                const inBody = bodyLower.includes(term);
                if (!inTitle && !inBody) {
                    allMatched = false;
                    break;
                }
                if (inTitle) score += titleLower.startsWith(term) ? 140 : 100;
                if (inBody) score += 20;
            }

            if (allMatched) scored.push({ post, score });
        }

        scored.sort((a, b) => b.score - a.score);
        return { terms, items: scored.map((s) => s.post) };
    }

    function updateSearchSelection() {
        const rows = searchVfResults.querySelectorAll('.search-vf-item');
        rows.forEach((row, i) => {
            const active = i === searchSelectedIdx;
            row.classList.toggle('is-selected', active);
            if (active) row.scrollIntoView({ block: 'nearest' });
        });
    }

    function renderSearchResults() {
        const { terms, items } = searchBlogTitleAndBody(searchVfInput.value);
        searchMatchedPosts = items;
        searchSelectedIdx = 0;

        searchVfCount.textContent = terms.length
            ? `${items.length} 条命中`
            : `共 ${POSTS.length} 篇`;

        if (!items.length) {
            searchVfResults.innerHTML = '<div class="search-vf-empty">翻遍了所有胶卷，没这张底片。</div>';
            return;
        }

        searchVfResults.innerHTML = items.map((post, idx) => {
            const snippet = buildBodySnippet(post.plainBody, terms);
            return `
                <button class="search-vf-item ${idx === 0 ? 'is-selected' : ''}" type="button" data-search-idx="${idx}">
                    <div class="search-vf-item-top">
                        <span class="search-vf-title">${highlightTerms(post.title, terms)}</span>
                        <span class="search-vf-date">${escapeHtml(post.date)}</span>
                    </div>
                    <div class="search-vf-snippet">${highlightTerms(snippet, terms)}</div>
                </button>
            `;
        }).join('');

        searchVfResults.querySelectorAll('.search-vf-item').forEach((btn) => {
            btn.addEventListener('click', () => {
                const post = searchMatchedPosts[Number(btn.dataset.searchIdx)];
                selectSearchResult(post);
            });
        });
    }

    function openViewfinderSearch() {
        if (!body.classList.contains('stage-workspace')) return;
        closePostReader({ immediate: true });
        closeFilmReel();
        closeSideReel();
        body.classList.add('intro-settled', 'search-open');
        searchBackdrop.setAttribute('aria-hidden', 'false');
        renderSearchResults();
        loadSearchIndex().then(() => {
            if (body.classList.contains('search-open')) renderSearchResults();
        });
        requestAnimationFrame(() => {
            searchVfInput.focus();
            searchVfInput.select();
        });
    }

    function closeViewfinderSearch() {
        body.classList.remove('search-open');
        searchBackdrop.setAttribute('aria-hidden', 'true');
    }

    function selectSearchResult(post, { fromHistory = false, category = 'home' } = {}) {
        if (!post) return;
        closeViewfinderSearch();
        const postGlobalIdx = POSTS.indexOf(post);
        if (postGlobalIdx === -1) return;

        if (fromHistory) {
            closePostReader({ immediate: true, fromPopState: true });
            body.classList.add('stage-workspace', 'intro-settled', 'evf-done');
        }
        if (pageAdvanceTimer) { clearTimeout(pageAdvanceTimer); pageAdvanceTimer = null; }
        if (filmSettle) filmSettle();
        activeCat = category;
        let filteredIdx = getFilteredPosts().indexOf(post);
        if (filteredIdx === -1) {
            activeCat = 'home';
            filteredIdx = postGlobalIdx;
        }
        currentPage = Math.floor(filteredIdx / PAGE_SIZE) + 1;
        pendingDirection = 0;
        skipNextFloatIn = true;
        updateActiveChannelState();
        renderMainPanel();

        const localIdx = filteredIdx % PAGE_SIZE;
        const card = mainPanel.querySelector(`.photo-print[data-post-idx="${localIdx}"]`);
        if (card) openPostWithDof(card, post, null, { fromHistory });
    }

    // ---------- 主题跟随与全局事件 ----------
    function applyTheme(dark, persist = false) {
        root.classList.toggle('dark-mode', dark);
        body.classList.toggle('dark-mode', dark);
        if (persist) {
            try { localStorage.setItem('theme', dark ? 'dark' : 'light'); } catch (e) {}
        }
    }

    function getSavedThemeDark() {
        try {
            const saved = localStorage.getItem('theme');
            if (saved === 'dark') return true;
            if (saved === 'light') return false;
        } catch (e) {}
        return !!(darkSchemeQuery && darkSchemeQuery.matches);
    }

    function bindEvents() {
        let userMovedPointer = false;
        window.addEventListener('pointermove', () => { userMovedPointer = true; }, { once: true, passive: true });
        if (focusFrame) {
            focusFrame.addEventListener('mouseenter', () => { if (userMovedPointer) evfPaused = true; });
            focusFrame.addEventListener('mouseleave', () => { evfPaused = false; });
        }

        if (deckPrevBtn) deckPrevBtn.addEventListener('click', () => goToPage(currentPage - 1, -1));
        if (deckNextBtn) deckNextBtn.addEventListener('click', () => goToPage(currentPage + 1, 1));

        let swipeStartX = 0;
        let swipeStartY = 0;
        mainPanel.addEventListener('touchstart', (e) => {
            if (!e.touches || e.touches.length !== 1) return;
            swipeStartX = e.touches[0].clientX;
            swipeStartY = e.touches[0].clientY;
        }, { passive: true });
        mainPanel.addEventListener('touchend', (e) => {
            if (!e.changedTouches || e.changedTouches.length !== 1 || body.classList.contains('dof-active')) return;
            const dx = e.changedTouches[0].clientX - swipeStartX;
            const dy = e.changedTouches[0].clientY - swipeStartY;
            if (Math.abs(dx) > 54 && Math.abs(dx) > Math.abs(dy) * 1.4) {
                goToPage(dx < 0 ? currentPage + 1 : currentPage - 1, dx < 0 ? 1 : -1);
            }
        }, { passive: true });

        document.querySelector('.film-edge.left').addEventListener('click', (e) => {
            const cell = e.target.closest('.para-cell-y');
            openSideReel('left', cell ? Number(cell.dataset.sideIdx || 0) : 0);
        });
        document.querySelector('.film-edge.right').addEventListener('click', (e) => {
            const cell = e.target.closest('.para-cell-y');
            openSideReel('right', cell ? Number(cell.dataset.sideIdx || 0) : 0);
        });
        sideReelBackdrop.addEventListener('click', (e) => {
            if (e.target === sideReelBackdrop) closeSideReel();
        });

        document.querySelector('.stage-center').addEventListener('dblclick', (e) => {
            if (!e.target.closest('button, a, input, .photo-print')) {
                openViewfinderSearch();
            }
        });
        document.getElementById('search-vf-close').addEventListener('click', closeViewfinderSearch);
        searchBackdrop.addEventListener('click', (e) => {
            if (e.target === searchBackdrop) closeViewfinderSearch();
        });
        searchVfInput.addEventListener('input', renderSearchResults);

        document.getElementById('reader-close').addEventListener('click', () => closePostReader());
        readerBackdrop.addEventListener('click', (e) => {
            if (e.target === readerBackdrop) closePostReader();
        });

        document.getElementById('reel-close').addEventListener('click', closeFilmReel);
        reelBackdrop.addEventListener('click', (e) => {
            if (e.target === reelBackdrop) closeFilmReel();
        });

        window.addEventListener('popstate', (event) => {
            readerHistoryClosing = false;
            const pending = pendingReaderPost;
            pendingReaderPost = null;
            if (pending) {
                closePostReader({ immediate: true, fromPopState: true });
                selectSearchResult(pending.post, { category: pending.category });
                return;
            }

            const post = POSTS.find((item) => item.url && item.url !== '#' &&
                new URL(item.url, window.location.href).pathname === window.location.pathname);
            if (post) {
                selectSearchResult(post, { fromHistory: true, category: event.state?.vfCategory || 'home' });
            } else {
                closePostReader({ immediate: true, fromPopState: true });
            }
        });

        window.addEventListener('resize', () => {
            if (body.classList.contains('reel-open')) {
                positionReelTrack(activeReelKey, { instant: true });
            }
        });

        window.addEventListener('keydown', (e) => {
            const activeTag = document.activeElement ? document.activeElement.tagName : '';
            const isTyping = activeTag === 'INPUT' || activeTag === 'TEXTAREA';

            if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k' && body.classList.contains('stage-workspace')) {
                e.preventDefault();
                if (body.classList.contains('search-open')) {
                    closeViewfinderSearch();
                } else {
                    openViewfinderSearch();
                }
                return;
            }

            if (e.key === '/' && !isTyping && body.classList.contains('stage-workspace') && !body.classList.contains('search-open')) {
                e.preventDefault();
                openViewfinderSearch();
                return;
            }

            if (body.classList.contains('search-open')) {
                if (e.key === 'Escape') {
                    e.preventDefault();
                    closeViewfinderSearch();
                    return;
                }
                if (e.key === 'ArrowDown' && searchMatchedPosts.length) {
                    e.preventDefault();
                    searchSelectedIdx = (searchSelectedIdx + 1) % searchMatchedPosts.length;
                    updateSearchSelection();
                    return;
                }
                if (e.key === 'ArrowUp' && searchMatchedPosts.length) {
                    e.preventDefault();
                    searchSelectedIdx = (searchSelectedIdx - 1 + searchMatchedPosts.length) % searchMatchedPosts.length;
                    updateSearchSelection();
                    return;
                }
                if (e.key === 'Enter' && searchMatchedPosts[searchSelectedIdx]) {
                    e.preventDefault();
                    selectSearchResult(searchMatchedPosts[searchSelectedIdx]);
                    return;
                }
                return;
            }

            if (e.key === 'Escape' && body.classList.contains('side-reel-open')) {
                e.preventDefault();
                closeSideReel();
                return;
            }
            if (e.key === 'Escape' && body.classList.contains('reel-open')) {
                e.preventDefault();
                closeFilmReel();
                return;
            }
            if (e.key === 'Escape' && body.classList.contains('dof-active')) {
                e.preventDefault();
                closePostReader();
                return;
            }
            if (!body.classList.contains('stage-workspace') && (e.key === 'Enter' || e.key === ' ')) {
                e.preventDefault();
                snapShutter();
                return;
            }
            if (body.classList.contains('reel-open')) {
                const realKeys = REEL_FRAMES.filter((f) => !f.stub).map((f) => f.key);
                const currIdx = realKeys.indexOf(activeReelKey);
                if (e.key === 'ArrowLeft' && currIdx > 0) {
                    e.preventDefault();
                    rollToReelFrame(realKeys[currIdx - 1]);
                } else if (e.key === 'ArrowRight' && currIdx >= 0 && currIdx < realKeys.length - 1) {
                    e.preventDefault();
                    rollToReelFrame(realKeys[currIdx + 1]);
                }
                return;
            }
            if (
                body.classList.contains('stage-workspace') &&
                !body.classList.contains('dof-active') &&
                !body.classList.contains('side-reel-open') &&
                !isTyping
            ) {
                if (e.key === 'ArrowLeft') {
                    e.preventDefault();
                    goToPage(currentPage - 1, -1);
                } else if (e.key === 'ArrowRight') {
                    e.preventDefault();
                    goToPage(currentPage + 1, 1);
                }
            }
        });

        applyTheme(getSavedThemeDark());
        if (darkSchemeQuery) {
            darkSchemeQuery.addEventListener('change', (e) => {
                try {
                    const saved = localStorage.getItem('theme');
                    if (saved === 'dark' || saved === 'light') return;
                } catch (err) {}
                applyTheme(e.matches);
            });
        }
    }

    // ---------- 访问量统计（与全站共享 session 去重） ----------
    async function loadVisitorCount() {
        const visitorNodes = document.querySelectorAll('[data-visitor-count]');
        const visitorCells = document.querySelectorAll('.visitor-cell');
        if (!visitorNodes.length || !visitorCells.length) return;

        let hasVisited = false;
        try { hasVisited = !!sessionStorage.getItem('v_session_flag'); } catch (e) {}
        const workerUrl = hasVisited ? 'https://api.silverash.site?update=false' : 'https://api.silverash.site';

        try {
            const response = await fetch(workerUrl);
            if (!response.ok) return;
            const text = (await response.text()).trim();
            if (!text || isNaN(text)) return;

            const formatted = parseInt(text, 10).toLocaleString();
            visitorNodes.forEach((node) => { node.textContent = formatted; });
            visitorCells.forEach((cell) => { cell.hidden = false; });

            if (!hasVisited) {
                try { sessionStorage.setItem('v_session_flag', 'true'); } catch (e) {}
            }
        } catch (err) {}
    }

    try {
        initSideReelDrag();
        renderPerimeterFilms();
        renderFilmReel();
        renderMainPanel();
    } catch (err) {
        console.error('[home-viewfinder] init render error:', err);
    }
    bindEvents();
    loadVisitorCount();

    startViewfinderSequence();
})();
