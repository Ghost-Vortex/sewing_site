// ===========================
//   КАСТОМНЫЙ КУРСОР
// ===========================
(function () {
  // Только на десктопе (pointer: fine = мышь/трекпад)
  if (!window.matchMedia('(pointer: fine)').matches) return;

  const dot  = document.getElementById('cursorDot');
  const ring = document.getElementById('cursorRing');
  if (!dot || !ring) return;

  let mouseX = 0, mouseY = 0;
  let ringX  = 0, ringY  = 0;

  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    dot.style.left = mouseX + 'px';
    dot.style.top  = mouseY + 'px';
  }, { passive: true });

  // Кольцо следует с плавным лагом
  (function animateRing() {
    ringX += (mouseX - ringX) * 0.12;
    ringY += (mouseY - ringY) * 0.12;
    ring.style.left = ringX + 'px';
    ring.style.top  = ringY + 'px';
    requestAnimationFrame(animateRing);
  })();

  // Расширяем кольцо на кликабельных элементах
  const hoverTargets = 'a, button, [role="button"], .work-card, .service-card, .step-card, .client-logo, .horizontal-card, .production-photo-card';
  document.addEventListener('mouseover', (e) => {
    if (e.target.closest(hoverTargets)) document.body.classList.add('cursor-hover');
  });
  document.addEventListener('mouseout', (e) => {
    if (e.target.closest(hoverTargets)) document.body.classList.remove('cursor-hover');
  });

  // Анимация клика
  document.addEventListener('mousedown', () => document.body.classList.add('cursor-click'));
  document.addEventListener('mouseup',   () => document.body.classList.remove('cursor-click'));
})();

// ===========================
//   DOM LOGIC
// ===========================
document.addEventListener('DOMContentLoaded', function () {
  const header  = document.querySelector('.main-header');
  const toggle  = document.querySelector('.menu-toggle');
  const nav     = document.querySelector('.nav-menu');

  // ===========================
  //   ХЕДЕР — затемнение при скролле
  //   passive: true = браузер не ждёт, можно не блокировать рендер
  // ===========================
  let ticking = false;

  function updateHeader() {
    if (!header) return;
    header.classList.toggle('scrolled', window.scrollY > 10);
    ticking = false;
  }

  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(updateHeader); // throttle через rAF
      ticking = true;
    }
  }, { passive: true });

  updateHeader();

  // ===========================
  //   БУРГЕР-МЕНЮ
  // ===========================
  if (toggle && nav) {
    const closeMenu = () => {
      toggle.classList.remove('open');
      nav.classList.remove('open');
    };

    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      nav.classList.contains('open') ? closeMenu() : (toggle.classList.add('open'), nav.classList.add('open'));
    });

    nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));

    document.addEventListener('click', (e) => {
      if (!nav.contains(e.target) && !toggle.contains(e.target)) closeMenu();
    });
  }

  // ===========================
  //   REVEAL-АНИМАЦИЯ (IntersectionObserver)
  // ===========================
  const revealEls = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window && revealEls.length) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    revealEls.forEach(el => revealObserver.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('visible'));
  }

  // ===========================
  //   PARALLAX HERO (mouse move)
  //   Делаем плавным через requestAnimationFrame
  // ===========================
  const hero        = document.querySelector('.hero');
  const heroContent = document.querySelector('.hero-content');

  if (hero && heroContent) {
    let heroRaf = null;
    let targetX = 0, targetY = 0;
    let currentX = 0, currentY = 0;

    // Плавная интерполяция — контент «плывёт» за курсором
    function animateHero() {
      currentX += (targetX - currentX) * 0.08;
      currentY += (targetY - currentY) * 0.08;
      heroContent.style.transform = `translate3d(${currentX}px, ${currentY}px, 0)`;
      heroRaf = requestAnimationFrame(animateHero);
    }

    hero.addEventListener('mousemove', (e) => {
      const rect = hero.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width  - 0.5;
      const y = (e.clientY - rect.top)  / rect.height - 0.5;
      targetX = x * 14;
      targetY = y * 8;
      if (!heroRaf) heroRaf = requestAnimationFrame(animateHero);
    }, { passive: true });

    hero.addEventListener('mouseleave', () => {
      targetX = 0;
      targetY = 0;
      // Дожидаемся возврата в 0 и останавливаем анимацию
      const stopWhenDone = () => {
        currentX += (0 - currentX) * 0.1;
        currentY += (0 - currentY) * 0.1;
        heroContent.style.transform = `translate3d(${currentX}px, ${currentY}px, 0)`;
        if (Math.abs(currentX) > 0.05 || Math.abs(currentY) > 0.05) {
          heroRaf = requestAnimationFrame(stopWhenDone);
        } else {
          heroContent.style.transform = 'translate3d(0,0,0)';
          cancelAnimationFrame(heroRaf);
          heroRaf = null;
        }
      };
      cancelAnimationFrame(heroRaf);
      heroRaf = requestAnimationFrame(stopWhenDone);
    });
  }

  // ===========================
  //   MOTION BLUR ПРИ СКРОЛЛЕ горизонтального контейнера
  // ===========================
  document.querySelectorAll('.horizontal-scroll').forEach((scroller) => {
    let blurTimer;

    scroller.addEventListener('scroll', () => {
      scroller.classList.add('is-scrolling');
      clearTimeout(blurTimer);
      blurTimer = setTimeout(() => scroller.classList.remove('is-scrolling'), 100);
    }, { passive: true });
  });

  // ===========================
  //   SUCCESS-СТЕЙТ ФОРМЫ
  //   Если на странице есть success message — прячем форму, показываем success
  // ===========================
  const successMsg = document.querySelector('.django-message.success');
  const heroForm   = document.querySelector('.hero-form-card, .contact-form-wrapper');

  if (successMsg && heroForm) {
    const formEl = heroForm.querySelector('form');
    const formTitle = heroForm.querySelector('h2, h3');

    if (formEl) {
      formEl.style.display = 'none';
      if (formTitle) formTitle.style.display = 'none';

      const successBlock = document.createElement('div');
      successBlock.className = 'form-success active';
      successBlock.innerHTML = `
        <div class="form-success-icon">✓</div>
        <h3 class="h5 fw-semibold mb-1">Заявка отправлена</h3>
        <p class="text-white-50 mb-0" style="font-size:0.9rem">Мы свяжемся с вами в ближайшее время</p>
      `;
      heroForm.appendChild(successBlock);
    }
  }

  // Автоскрытие уведомлений через 4 секунды
  document.querySelectorAll('.django-message').forEach(msg => {
    setTimeout(() => msg.remove(), 4200);
  });

  // ===========================
  //   STAGGER-АНИМАЦИЯ для карточек внутри .reveal
  //   Карточки появляются с задержкой друг за другом
  // ===========================
  document.querySelectorAll('.row.g-4').forEach(row => {
    const cards = row.querySelectorAll('.reveal');
    cards.forEach((card, i) => {
      card.style.transitionDelay = `${i * 0.07}s`;
    });
  });

  // ===========================
  //   КАСТОМНЫЙ FAQ АККОРДЕОН
  // ===========================
  document.querySelectorAll('.faq-trigger').forEach(trigger => {
    trigger.addEventListener('click', () => {
      const item = trigger.closest('.faq-item');
      const body = item.querySelector('.faq-body');
      const isOpen = item.classList.contains('open');

      // Закрываем все открытые
      document.querySelectorAll('.faq-item.open').forEach(openItem => {
        openItem.classList.remove('open');
        openItem.querySelector('.faq-trigger').setAttribute('aria-expanded', 'false');
        openItem.querySelector('.faq-body').style.maxHeight = '0';
      });

      // Открываем текущий (если был закрыт)
      if (!isOpen) {
        item.classList.add('open');
        trigger.setAttribute('aria-expanded', 'true');
        body.style.maxHeight = body.scrollHeight + 'px';
      }
    });
  });
});

// ===========================
//   ПЛАВНЫЕ ПЕРЕХОДЫ МЕЖДУ СТРАНИЦАМИ
// ===========================
(function () {
  document.addEventListener('click', (e) => {
    const link = e.target.closest('a[href]');
    if (!link) return;

    const href = link.getAttribute('href');
    if (
      !href ||
      href.startsWith('#') ||
      href.startsWith('http') ||
      href.startsWith('mailto:') ||
      href.startsWith('tel:') ||
      link.target === '_blank' ||
      e.ctrlKey || e.metaKey || e.shiftKey
    ) return;

    e.preventDefault();

    if (document.startViewTransition) {
      document.startViewTransition(() => { window.location.href = href; });
    } else {
      document.body.classList.add('page-leaving');
      setTimeout(() => { window.location.href = href; }, 260);
    }
  });
})();

// ===========================
//   BACK TO TOP
// ===========================
(function () {
  const btn = document.getElementById('backToTop');
  if (!btn) return;

  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        btn.classList.toggle('visible', window.scrollY > 400);
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });

  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
})();

// ===========================
//   YANDEX MAP
// ===========================
function initYandexMap() {
  const mapEl = document.getElementById('yandex-map');
  if (!mapEl) return;

  const coords = [55.739823, 37.783141];

  const map = new ymaps.Map('yandex-map', {
    center: coords,
    zoom: 16,
    controls: ['zoomControl'],
    behaviors: ['drag', 'scrollZoom', 'multiTouch']
  });

  // Тёмная тема через CSS filter на тайлах
  map.panes.get('ground').getElement().style.filter =
    'invert(92%) hue-rotate(180deg) saturate(0.6) brightness(0.85)';

  const placemark = new ymaps.Placemark(coords, {
    hintContent: 'Ulagasheff — швейное производство',
    balloonContent:
      '<strong>Ulagasheff</strong><br>Швейное производство<br>Москва, район Перово'
  }, {
    preset: 'islands#darkCircleDotIcon',
    iconColor: '#ffffff'
  });

  map.geoObjects.add(placemark);
  map.behaviors.disable('scrollZoom'); // не зумить колёсиком при скролле страницы
}

// Инициализируем карту после загрузки API
if (window.ymaps) {
  ymaps.ready(initYandexMap);
}

// ===========================
//   AJAX ФОРМЫ
// ===========================
(function () {
  // Читаем CSRF из cookie — всегда свежий, даже если страница закэширована
  function getCsrf() {
    var match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : '';
  }

  document.querySelectorAll('form[data-ajax-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      // Браузерная валидация required-полей
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      var btn = form.querySelector('[type="submit"]');
      var originalText = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Отправляем…'; }

      var data = new FormData(form);

      fetch(form.action, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCsrf()
        },
        body: data
      })
        .then(function (r) { return r.json(); })
        .then(function (json) {
          if (json.ok) {
            showFormSuccess(form, json.message);
          } else {
            if (btn) { btn.disabled = false; btn.textContent = originalText; }
          }
        })
        .catch(function () {
          if (btn) { btn.disabled = false; btn.textContent = originalText; }
        });
    });
  });

  function showFormSuccess(form, msg) {
    var wrap = form.closest('.home-hero-form-wrap') || form.parentElement;
    var success = document.createElement('div');
    success.className = 'form-success-state';
    success.innerHTML =
      '<div class="form-success-icon">✓</div>' +
      '<h3 class="form-success-title">Заявка отправлена</h3>' +
      '<p class="form-success-msg">' + (msg || 'Мы свяжемся с вами в течение рабочего дня.') + '</p>';
    wrap.style.position = 'relative';
    wrap.appendChild(success);
    // trigger animation
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        success.classList.add('visible');
      });
    });
  }
})();

// ===========================
//   COOKIE BANNER
// ===========================
(function () {
  var banner = document.getElementById('cookieBanner');
  var btn = document.getElementById('cookieAccept');
  if (!banner || !btn) return;

  // Если уже принял — не показываем
  if (localStorage.getItem('cookieAccepted')) return;

  // Показываем с небольшой задержкой
  banner.removeAttribute('hidden');
  setTimeout(function () {
    banner.classList.add('visible');
  }, 1200);

  btn.addEventListener('click', function () {
    localStorage.setItem('cookieAccepted', '1');
    banner.classList.remove('visible');
    setTimeout(function () { banner.setAttribute('hidden', ''); }, 500);
  });
})();
