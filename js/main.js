/**
 * Split Motorsport — JavaScript principal
 * Menu mobile, scroll suave, animações e validação do formulário
 */

(function () {
  'use strict';

  /* --- Elementos DOM --- */
  const header = document.getElementById('header');
  const nav = document.getElementById('nav');
  const menuToggle = document.getElementById('menuToggle');
  const navLinks = document.querySelectorAll('.nav__link');
  const revealElements = document.querySelectorAll('.reveal');
  const contactForm = document.getElementById('contactForm');
  const WHATSAPP_NUMBER = '5511958872337';

  /* --- Header: efeito ao rolar --- */
  function handleScroll() {
    if (window.scrollY > 40) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
    updateActiveNavLink();
  }

  /* --- Menu mobile --- */
  function toggleMenu() {
    const isOpen = nav.classList.toggle('open');
    menuToggle.classList.toggle('active', isOpen);
    menuToggle.setAttribute('aria-expanded', isOpen);
    menuToggle.setAttribute('aria-label', isOpen ? 'Fechar menu' : 'Abrir menu');
    document.body.style.overflow = isOpen ? 'hidden' : '';
  }

  function closeMenu() {
    nav.classList.remove('open');
    menuToggle.classList.remove('active');
    menuToggle.setAttribute('aria-expanded', 'false');
    menuToggle.setAttribute('aria-label', 'Abrir menu');
    document.body.style.overflow = '';
  }

  /* --- Link ativo no menu conforme seção visível --- */
  function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const scrollPos = window.scrollY + header.offsetHeight + 100;

    sections.forEach(function (section) {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      const id = section.getAttribute('id');

      if (scrollPos >= top && scrollPos < top + height) {
        navLinks.forEach(function (link) {
          link.classList.remove('active');
          if (link.getAttribute('href') === '#' + id) {
            link.classList.add('active');
          }
        });
      }
    });
  }

  /* --- Scroll suave para âncoras --- */
  function smoothScrollTo(target) {
    const el = document.querySelector(target);
    if (!el) return;

    const top = el.getBoundingClientRect().top + window.scrollY - header.offsetHeight;
    window.scrollTo({ top: top, behavior: 'smooth' });
  }

  /* --- Animações ao rolar (Intersection Observer) --- */
  function initRevealAnimations() {
    if (!('IntersectionObserver' in window)) {
      revealElements.forEach(function (el) {
        el.classList.add('visible');
      });
      return;
    }

    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );

    revealElements.forEach(function (el) {
      observer.observe(el);
    });
  }

  /* --- Validação do formulário --- */
  const validators = {
    nome: function (value) {
      if (!value.trim()) return 'Informe seu nome completo.';
      if (value.trim().length < 3) return 'Nome deve ter pelo menos 3 caracteres.';
      return '';
    },
    telefone: function (value) {
      const digits = value.replace(/\D/g, '');
      if (!digits) return 'Informe seu telefone ou WhatsApp.';
      if (digits.length < 10) return 'Telefone inválido. Use DDD + número.';
      return '';
    },
    modelo: function (value) {
      if (!value) return 'Selecione o modelo do veículo.';
      return '';
    },
    servico: function (value) {
      if (!value) return 'Selecione o tipo de serviço.';
      return '';
    },
    mensagem: function (value) {
      if (!value.trim()) return 'Escreva uma mensagem.';
      if (value.trim().length < 10) return 'Mensagem muito curta. Descreva melhor sua necessidade.';
      return '';
    }
  };

  function validateField(name, value) {
    const validator = validators[name];
    return validator ? validator(value) : '';
  }

  function setFieldState(field, errorMsg) {
    const errorEl = document.getElementById('error-' + field.name);
    field.classList.remove('error', 'success');

    if (errorMsg) {
      field.classList.add('error');
      if (errorEl) errorEl.textContent = errorMsg;
      return false;
    }

    field.classList.add('success');
    if (errorEl) errorEl.textContent = '';
    return true;
  }

  function validateForm() {
    let isValid = true;
    const fields = contactForm.querySelectorAll('input, select, textarea');

    fields.forEach(function (field) {
      const error = validateField(field.name, field.value);
      if (!setFieldState(field, error)) isValid = false;
    });

    return isValid;
  }

  function buildWhatsAppMessage(data) {
    return [
      'Olá! Gostaria de agendar uma avaliação na Split Motorsport.',
      '',
      '*Nome:* ' + data.nome,
      '*Telefone:* ' + data.telefone,
      '*Veículo:* ' + data.modelo,
      '*Serviço:* ' + data.servico,
      '',
      '*Mensagem:*',
      data.mensagem
    ].join('\n');
  }

  function handleFormSubmit(e) {
    e.preventDefault();

    const successEl = document.getElementById('formSuccess');
    if (successEl) successEl.hidden = true;

    if (!validateForm()) return;

    const data = {
      nome: document.getElementById('nome').value.trim(),
      telefone: document.getElementById('telefone').value.trim(),
      modelo: document.getElementById('modelo').value,
      servico: document.getElementById('servico').value,
      mensagem: document.getElementById('mensagem').value.trim()
    };

    const message = encodeURIComponent(buildWhatsAppMessage(data));
    const url = 'https://wa.me/' + WHATSAPP_NUMBER + '?text=' + message;

    if (successEl) successEl.hidden = false;

    setTimeout(function () {
      window.open(url, '_blank', 'noopener,noreferrer');
    }, 600);
  }

  /* --- Máscara simples de telefone --- */
  function maskPhone(input) {
    let value = input.value.replace(/\D/g, '');

    if (value.length > 11) value = value.slice(0, 11);

    if (value.length > 6) {
      value = '(' + value.slice(0, 2) + ') ' + value.slice(2, 7) + '-' + value.slice(7);
    } else if (value.length > 2) {
      value = '(' + value.slice(0, 2) + ') ' + value.slice(2);
    } else if (value.length > 0) {
      value = '(' + value;
    }

    input.value = value;
  }

  /* --- Event listeners --- */
  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();

  if (menuToggle) {
    menuToggle.addEventListener('click', toggleMenu);
  }

  navLinks.forEach(function (link) {
    link.addEventListener('click', function (e) {
      const href = link.getAttribute('href');
      if (href && href.startsWith('#')) {
        e.preventDefault();
        smoothScrollTo(href);
        closeMenu();
      }
    });
  });

  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    if (anchor.classList.contains('nav__link')) return;

    anchor.addEventListener('click', function (e) {
      const href = anchor.getAttribute('href');
      if (href && href.length > 1) {
        e.preventDefault();
        smoothScrollTo(href);
      }
    });
  });

  if (contactForm) {
    contactForm.addEventListener('submit', handleFormSubmit);

    contactForm.querySelectorAll('input, select, textarea').forEach(function (field) {
      field.addEventListener('blur', function () {
        const error = validateField(field.name, field.value);
        setFieldState(field, error);
      });

      field.addEventListener('input', function () {
        if (field.classList.contains('error')) {
          const error = validateField(field.name, field.value);
          if (!error) setFieldState(field, '');
        }
      });
    });

    const telefoneInput = document.getElementById('telefone');
    if (telefoneInput) {
      telefoneInput.addEventListener('input', function () {
        maskPhone(telefoneInput);
      });
    }
  }

  window.addEventListener('resize', function () {
    if (window.innerWidth > 768) closeMenu();
  });

  /* Hero: respeitar preferência de movimento reduzido */
  const heroVideo = document.querySelector('.hero__video');
  if (heroVideo && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    heroVideo.removeAttribute('autoplay');
    heroVideo.pause();
  }

  initRevealAnimations();
})();
