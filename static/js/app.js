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

    /* ---------- CARRITO DE COMPRAS (SE GUARDA EN LA SESIÓN DE FLASK) ---------- */
    const cartPanel = document.getElementById('cartPanel');
    if (cartPanel) {
        const urls = cartPanel.dataset;
        const cartCount = document.getElementById('cart-count');
        const cartItems = document.getElementById('cart-items');
        const cartEmpty = document.getElementById('cart-empty');
        const cartSummary = document.getElementById('cart-summary');
        const cartTotal = document.getElementById('cart-total');
        const cartToast = document.getElementById('cart-toast');
        let toastTimer = null;

        const formatoMXN = (valor) => '$' + Number(valor).toLocaleString('es-MX', { maximumFractionDigits: 0 }) + ' MXN';

        const mostrarToast = (mensaje) => {
            if (!cartToast) return;
            cartToast.textContent = mensaje;
            cartToast.classList.add('show');
            clearTimeout(toastTimer);
            toastTimer = setTimeout(() => cartToast.classList.remove('show'), 2500);
        };

        const peticion = async (url, datos) => {
            const opciones = datos === undefined
                ? { headers: { 'Accept': 'application/json' } }
                : {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                    body: JSON.stringify(datos)
                };
            const resp = await fetch(url, opciones);
            if (!resp.ok) throw new Error('Error ' + resp.status);
            return resp.json();
        };

        const crearElemento = (tag, clase, texto) => {
            const el = document.createElement(tag);
            if (clase) el.className = clase;
            if (texto !== undefined) el.textContent = texto;
            return el;
        };

        const pintarCarrito = (carrito) => {
            cartCount.textContent = carrito.cantidad;
            cartItems.replaceChildren();
            const vacio = carrito.items.length === 0;
            cartEmpty.hidden = !vacio;
            cartSummary.hidden = vacio;
            cartTotal.textContent = formatoMXN(carrito.total);

            carrito.items.forEach((item) => {
                const li = crearElemento('li', 'cart-item');
                li.dataset.producto = item.id;

                const img = crearElemento('img');
                img.src = item.imagen;
                img.alt = '';

                const info = crearElemento('div', 'cart-item-info');
                info.append(
                    crearElemento('p', 'cart-item-name', item.nombre),
                    crearElemento('p', 'cart-item-price', formatoMXN(item.precio))
                );

                const qty = crearElemento('div', 'cart-qty');
                const menos = crearElemento('button', 'cart-qty-btn', '−');
                menos.type = 'button';
                menos.dataset.accion = 'restar';
                menos.setAttribute('aria-label', 'Quitar uno de ' + item.nombre);
                const cantidad = crearElemento('span', 'cart-qty-value', String(item.cantidad));
                const mas = crearElemento('button', 'cart-qty-btn', '+');
                mas.type = 'button';
                mas.dataset.accion = 'sumar';
                mas.setAttribute('aria-label', 'Agregar uno más de ' + item.nombre);
                qty.append(menos, cantidad, mas);
                info.append(qty);

                const lado = crearElemento('div', 'cart-item-side');
                const quitar = crearElemento('button', 'cart-remove');
                quitar.type = 'button';
                quitar.dataset.accion = 'eliminar';
                quitar.setAttribute('aria-label', 'Eliminar ' + item.nombre + ' del carrito');
                quitar.innerHTML = '<i class="fa-solid fa-trash-can" aria-hidden="true"></i>';
                lado.append(quitar, crearElemento('strong', 'cart-item-subtotal', formatoMXN(item.subtotal)));

                li.dataset.cantidad = item.cantidad;
                li.append(img, info, lado);
                cartItems.append(li);
            });
        };

        const cargarCarrito = () => peticion(urls.urlVer).then(pintarCarrito).catch(() => {});

        // Botones "Agregar al carrito"
        document.querySelectorAll('.btn-add[data-producto]').forEach((btn) => {
            btn.addEventListener('click', async () => {
                const textoOriginal = btn.textContent;
                btn.disabled = true;
                try {
                    const carrito = await peticion(urls.urlAgregar, { id_producto: btn.dataset.producto, cantidad: 1 });
                    pintarCarrito(carrito);
                    const nombre = btn.closest('.product-card')?.querySelector('h3')?.textContent || 'Producto';
                    mostrarToast(nombre + ' se agregó al carrito');
                    btn.textContent = '¡Agregado!';
                    setTimeout(() => { btn.textContent = textoOriginal; }, 1200);
                } catch (err) {
                    mostrarToast('No se pudo agregar el producto, intenta de nuevo');
                } finally {
                    btn.disabled = false;
                }
            });
        });

        // Botones dentro del panel: +, −, eliminar
        cartItems.addEventListener('click', async (e) => {
            const btn = e.target.closest('button[data-accion]');
            if (!btn) return;
            const li = btn.closest('.cart-item');
            const id = li.dataset.producto;
            const actual = Number(li.dataset.cantidad);
            try {
                let carrito;
                if (btn.dataset.accion === 'eliminar') {
                    carrito = await peticion(urls.urlEliminar, { id_producto: id });
                } else {
                    const nueva = btn.dataset.accion === 'sumar' ? actual + 1 : actual - 1;
                    carrito = await peticion(urls.urlActualizar, { id_producto: id, cantidad: nueva });
                }
                pintarCarrito(carrito);
            } catch (err) {
                mostrarToast('No se pudo actualizar el carrito');
            }
        });

        const vaciarBtn = document.getElementById('cart-clear');
        if (vaciarBtn) {
            vaciarBtn.addEventListener('click', async () => {
                if (!confirm('¿Vaciar todo el carrito?')) return;
                try {
                    pintarCarrito(await peticion(urls.urlVaciar, {}));
                } catch (err) {
                    mostrarToast('No se pudo vaciar el carrito');
                }
            });
        }

        const pagarBtn = document.getElementById('cart-checkout');
        if (pagarBtn) {
            pagarBtn.addEventListener('click', () => mostrarToast('El pago en línea estará disponible muy pronto'));
        }

        // Si se abre un modal (p. ej. iniciar sesión) se cierra el panel del carrito
        document.querySelectorAll('.modal').forEach((modal) => {
            modal.addEventListener('show.bs.modal', () => {
                const instancia = window.bootstrap && window.bootstrap.Offcanvas.getInstance(cartPanel);
                if (instancia) instancia.hide();
            });
        });

        cartPanel.addEventListener('show.bs.offcanvas', cargarCarrito);
        cargarCarrito();
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