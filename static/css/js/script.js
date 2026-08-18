/* =========================================================
   QUADNEX — SCRIPT.JS (JavaScript Vanilla)
   ========================================================= */

document.addEventListener('DOMContentLoaded', () => {

    /* ---------- MENÚ MÓVIL ---------- */
    const hamburgerBtn = document.getElementById('hamburger-btn');
    const mainNav = document.getElementById('main-nav');

    if (hamburgerBtn && mainNav) {
        hamburgerBtn.addEventListener('click', () => {
            const isOpen = mainNav.classList.toggle('open');
            hamburgerBtn.classList.toggle('open', isOpen);
            hamburgerBtn.setAttribute('aria-expanded', String(isOpen));
        });

        // Cerrar el menú al elegir una opción (en móvil)
        mainNav.querySelectorAll('a').forEach((link) => {
            link.addEventListener('click', () => {
                if (mainNav.classList.contains('open')) {
                    mainNav.classList.remove('open');
                    hamburgerBtn.classList.remove('open');
                    hamburgerBtn.setAttribute('aria-expanded', 'false');
                }
            });
        });
    }

    /* ---------- ANIMACIÓN DE ENTRADA DEL HERO ---------- */
    const heroAnimEls = document.querySelectorAll('.hero-anim');
    heroAnimEls.forEach((el, index) => {
        // Escalonar la aparición: título, subtítulo, botones
        setTimeout(() => {
            el.classList.add('in-view');
        }, 200 + index * 180);
    });

    /* ---------- EFECTO PARALLAX EN EL HERO ---------- */
    const heroSection = document.getElementById('hero');
    const heroImg = document.getElementById('hero-img');

    if (heroSection && heroImg) {
        let targetX = 0;
        let targetY = 0;
        let currentX = 0;
        let currentY = 0;
        const maxShift = 18; // px, movimiento discreto

        heroSection.addEventListener('mousemove', (e) => {
            const rect = heroSection.getBoundingClientRect();
            const relX = (e.clientX - rect.left) / rect.width - 0.5;
            const relY = (e.clientY - rect.top) / rect.height - 0.5;
            targetX = relX * maxShift;
            targetY = relY * maxShift;
        });

        heroSection.addEventListener('mouseleave', () => {
            targetX = 0;
            targetY = 0;
        });

        function animateParallax() {
            // Suavizado (easing) para un movimiento fluido
            currentX += (targetX - currentX) * 0.06;
            currentY += (targetY - currentY) * 0.06;
            heroImg.style.transform = `scale(1.05) translate(${currentX}px, ${currentY}px)`;
            requestAnimationFrame(animateParallax);
        }
        requestAnimationFrame(animateParallax);
    }

    /* ---------- ANIMACIONES AL HACER SCROLL (IntersectionObserver) ---------- */
    const revealEls = document.querySelectorAll('.reveal');

    if ('IntersectionObserver' in window) {
        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

        revealEls.forEach((el) => revealObserver.observe(el));
    } else {
        // Respaldo si el navegador no soporta IntersectionObserver
        revealEls.forEach((el) => el.classList.add('visible'));
    }

    /* ---------- CARRITO DE COMPRAS ---------- */
    let cartCount = 0;
    const cartCountEl = document.getElementById('cart-count');
    const addButtons = document.querySelectorAll('.btn-add');
    const cartToast = document.getElementById('cart-toast');
    let toastTimeout = null;

    function updateCartDisplay() {
        if (cartCountEl) {
            cartCountEl.textContent = String(cartCount);
            cartCountEl.classList.remove('bump');
            // Forzar reflow para reiniciar la animación
            void cartCountEl.offsetWidth;
            cartCountEl.classList.add('bump');
        }
    }

    function showNotification(message) {
        if (!cartToast) return;
        cartToast.textContent = message;
        cartToast.classList.add('show');

        clearTimeout(toastTimeout);
        toastTimeout = setTimeout(() => {
            cartToast.classList.remove('show');
        }, 2600);
    }

    addButtons.forEach((btn) => {
        btn.addEventListener('click', () => {
            cartCount++;
            updateCartDisplay();

            btn.classList.add('added');
            const originalText = btn.textContent;
            btn.textContent = 'Agregado ✓';
            setTimeout(() => {
                btn.classList.remove('added');
                btn.textContent = originalText;
            }, 1200);

            showNotification('Producto agregado al carrito.');
        });
    });

    /* ---------- SCROLL SUAVE PARA ENLACES INTERNOS ---------- */
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener('click', (e) => {
            const targetId = anchor.getAttribute('href');
            if (!targetId || targetId === '#') return;

            const targetEl = document.querySelector(targetId);
            if (targetEl) {
                e.preventDefault();
                targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    /* ---------- FORMULARIOS (evitar recarga real de la demo) ---------- */
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', (e) => {
            e.preventDefault();
            showNotification('¡Gracias por suscribirte a QuadNeX!');
            newsletterForm.reset();
        });
    }

    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const input = searchForm.querySelector('input');
            if (input && input.value.trim()) {
                showNotification(`Buscando: "${input.value.trim()}"`);
            }
        });
    }

});
