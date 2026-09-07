/* =========================================================
   QUADNEX — APP.JS (JavaScript Vanilla para Apoyo Visual)
   ========================================================= */

document.addEventListener('DOMContentLoaded', () => {

    /* ---------- ANIMACIÓN ENTRADA HERO ---------- */
    const heroAnimEls = document.querySelectorAll('.hero-anim');
    heroAnimEls.forEach((el, index) => {
        setTimeout(() => {
            el.classList.add('in-view');
        }, 150 + index * 150);
    });

    /* ---------- REVEAL EN SCROLL (IntersectionObserver) ---------- */
    const revealEls = document.querySelectorAll('.reveal');
    if ('IntersectionObserver' in window) {
        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });

        revealEls.forEach((el) => revealObserver.observe(el));
    } else {
        revealEls.forEach((el) => el.classList.add('visible'));
    }

    /* ---------- ALTERNAR MOSTRAR/OCULTAR CONTRASEÑA ---------- */
    const togglePasswordBtns = document.querySelectorAll('.toggle-password');
    
    togglePasswordBtns.forEach((btn) => {
        btn.addEventListener('click', () => {
            const input = btn.parentElement.querySelector('input');
            const icon = btn.querySelector('i');

            if (input && icon) {
                const isPassword = input.getAttribute('type') === 'password';
                input.setAttribute('type', isPassword ? 'text' : 'password');
                
                // Cambiar icono entre ojo abierto y cerrado
                if (isPassword) {
                    icon.classList.remove('fa-eye');
                    icon.classList.add('fa-eye-slash');
                } else {
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }
            }
        });
    });

    /* ---------- INTERCEPCIÓN VISUAL DE FORMULARIOS (SIN PROCESAMIENTO BACKEND) ---------- */
    const authForms = document.querySelectorAll('.auth-form');

    authForms.forEach((form) => {
        form.addEventListener('submit', (e) => {
            // Se previene la recarga por ser demostración frontal de diseño
            e.preventDefault();

            const submitBtn = form.querySelector('.btn-auth-submit');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                
                // Animación visual de carga ligera
                submitBtn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> PROCESANDO...`;
                submitBtn.style.opacity = '0.8';

                setTimeout(() => {
                    submitBtn.innerHTML = `<i class="fa-solid fa-check"></i> ¡ÉXITO!`;
                    submitBtn.style.backgroundColor = '#28a745';

                    setTimeout(() => {
                        submitBtn.innerHTML = originalText;
                        submitBtn.style.backgroundColor = '';
                        submitBtn.style.opacity = '1';

                        // Cerrar modal de Bootstrap activo si existe
                        const activeModalEl = form.closest('.modal');
                        if (activeModalEl && window.bootstrap) {
                            const modalInstance = window.bootstrap.Modal.getInstance(activeModalEl);
                            if (modalInstance) {
                                modalInstance.hide();
                            }
                        }
                    }, 1000);
                }, 1200);
            }
        });
    });

    /* ---------- MENÚ HAMBURGUESA MÓVIL ---------- */
    const hamburgerBtn = document.getElementById('hamburger-btn');
    const mainNav = document.getElementById('main-nav');

    if (hamburgerBtn && mainNav) {
        hamburgerBtn.addEventListener('click', () => {
            const isOpen = mainNav.classList.toggle('open');
            hamburgerBtn.classList.toggle('open', isOpen);
            hamburgerBtn.setAttribute('aria-expanded', String(isOpen));
        });
    }

});