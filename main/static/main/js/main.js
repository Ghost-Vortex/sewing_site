// ===========================
//   DOM LOGIC (header, scroll, parallax, blur)
// ===========================
document.addEventListener('DOMContentLoaded', function () {
  const header = document.querySelector('.main-header');
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav-menu');

  // Липкий хедер с затемнением при скролле
  function onScroll() {
    if (!header) return;

    if (window.scrollY > 10) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }
  window.addEventListener('scroll', onScroll);
  onScroll();

  // Бургер-меню (фикс для мобилок)
  if (toggle && nav) {
    const closeMenu = () => {
      toggle.classList.remove('open');
      nav.classList.remove('open');
    };

    // открыть / закрыть по нажатию на кнопку
    toggle.addEventListener('click', (e) => {
      e.stopPropagation();               // чтобы клик не улетал дальше
      if (nav.classList.contains('open')) {
        closeMenu();
      } else {
        toggle.classList.add('open');
        nav.classList.add('open');
      }
    });

    // закрывать меню при клике по ссылке
    nav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', closeMenu);
    });

    // закрывать меню при клике вне его области
    document.addEventListener('click', (e) => {
      const insideNav = nav.contains(e.target);
      const onToggle = toggle.contains(e.target);
      if (!insideNav && !onToggle) {
        closeMenu();
      }
    });
  }

  // REVEAL-Анимация на скролле
  const revealElements = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.15
    });

    revealElements.forEach(el => observer.observe(el));
  } else {
    // запасной вариант: просто сразу показать
    revealElements.forEach(el => el.classList.add('visible'));
  }

  // ===========================
  //   PARALLAX HERO
  // ===========================
  const hero = document.querySelector('.hero');
  const heroContent = document.querySelector('.hero-content');

  if (hero && heroContent) {
    hero.addEventListener('mousemove', (e) => {
      const rect = hero.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5; // -0.5 .. 0.5
      const y = (e.clientY - rect.top) / rect.height - 0.5;

      const moveX = x * 16; // чем больше число, тем сильнее эффект
      const moveY = y * 10;

      heroContent.style.transform =
        `translate3d(${moveX}px, ${moveY}px, 0)`;
    });

    hero.addEventListener('mouseleave', () => {
      heroContent.style.transform = 'translate3d(0,0,0)';
    });
  }

  // ===========================
  //   PARALLAX НА ПРОИЗВОДСТВЕ
  // ===========================
  const productionScroll = document.querySelector('.horizontal-scroll');

  if (productionScroll) {
    productionScroll.addEventListener('mousemove', (e) => {
      const rect = productionScroll.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;

      // лёгкий parallax по X для всех карточек
      productionScroll.querySelectorAll('.horizontal-card').forEach((card, index) => {
        const depth = (index + 1) * 2; // разная глубина
        const offsetX = x * depth;
        card.style.transform = `translate3d(${offsetX}px, 0, 0) scale(1.02)`;
      });
    });

    productionScroll.addEventListener('mouseleave', () => {
      productionScroll.querySelectorAll('.horizontal-card').forEach((card) => {
        card.style.transform = 'translate3d(0,0,0)';
      });
    });
  }

  // ===========================
  //   MOTION BLUR НА СКРОЛЛЕ
  // ===========================
  document.querySelectorAll('.horizontal-scroll').forEach((scroller) => {
    let blurTimeout;

    scroller.addEventListener('scroll', () => {
      scroller.classList.add('is-scrolling');

      clearTimeout(blurTimeout);
      blurTimeout = setTimeout(() => {
        scroller.classList.remove('is-scrolling');
      }, 90); // чем меньше, тем быстрее blur пропадает
    });
  });
});


// ===========================
//   YANDEX MAP BLOCK
// ===========================
function initYandexMap() {
  // Координаты твоей точки (поставь свои из Яндекс Карт)
  const coords = [55.739823, 37.783141];

  const map = new ymaps.Map("yandex-map", {
    center: coords,
    zoom: 15,
    controls: ["zoomControl"]
  });

  const placemark = new ymaps.Placemark(coords, {
    hintContent: "Мы здесь",
    balloonContent: "Швейное производство Ulagasheff"
  }, {
    preset: "islands#whiteStretchyIcon"
  });

  map.geoObjects.add(placemark);
}

if (window.ymaps) {
  ymaps.ready(initYandexMap);
}