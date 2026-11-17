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

    /* ---------- ENVÍO DE FORMULARIOS DE ACCESO (LOS PROCESA FLASK) ---------- */
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            const clave = registerForm.querySelector('[name="clave"]');
            const confirmar = registerForm.querySelector('[name="confirmar"]');
            if (clave && confirmar && clave.value !== confirmar.value) {
                e.preventDefault();
                confirmar.setCustomValidity('Las contraseñas no coinciden');
                confirmar.reportValidity();
            }
        });
        const confirmar = registerForm.querySelector('[name="confirmar"]');
        if (confirmar) confirmar.addEventListener('input', () => confirmar.setCustomValidity(''));
    }

    document.querySelectorAll('.auth-form').forEach((form) => {
        form.addEventListener('submit', (e) => {
            if (e.defaultPrevented) return;
            const submitBtn = form.querySelector('.btn-auth-submit');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> PROCESANDO...';
                submitBtn.style.opacity = '0.8';
            }
        });
    });

    /* ---------- MENSAJES FLASH: SE OCULTAN SOLOS ---------- */
    const flashBox = document.getElementById('flash-messages');
    if (flashBox) {
        setTimeout(() => {
            flashBox.classList.add('is-hidden');
            setTimeout(() => flashBox.remove(), 600);
        }, 4000);
    }

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