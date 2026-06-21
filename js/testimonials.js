/**
 * Depoimentos — carregamento do destaque Instagram
 * https://www.instagram.com/stories/highlights/17962501514442570/
 */
(function () {
  'use strict';

  var HIGHLIGHT_URL = 'https://www.instagram.com/stories/highlights/17962501514442570/';
  var USERNAME = 'split_motorsport';

  var grid = document.getElementById('depoimentosGrid');
  var status = document.getElementById('depoimentosStatus');

  if (!grid || !status) return;

  function setStatus(message) {
    status.textContent = message;
  }

  function extractMediaCodes(html) {
    var codes = [];
    var seen = {};

    var patterns = [
      /instagram\.com\/reel\/([A-Za-z0-9_-]+)/g,
      /instagram\.com\/p\/([A-Za-z0-9_-]+)/g,
      /"code":"([A-Za-z0-9_-]{11})"/g,
      /"shortcode":"([A-Za-z0-9_-]{11})"/g
    ];

    patterns.forEach(function (pattern) {
      var match;
      while ((match = pattern.exec(html)) !== null) {
        var code = match[1];
        if (!seen[code]) {
          seen[code] = true;
          codes.push(code);
        }
      }
    });

    return codes;
  }

  function extractGraphqlCodes(html) {
    var codes = [];
    var marker = 'xdt_api__v1__feed__reels_media__connection';
    if (html.indexOf(marker) === -1) return codes;

    var edgeMatches = html.match(/"code":"([A-Za-z0-9_-]{11})"/g) || [];
    edgeMatches.forEach(function (item) {
      var code = item.replace(/"code":"(.+)"/, '$1');
      if (codes.indexOf(code) === -1) codes.push(code);
    });

    return codes;
  }

  function createEmbedCard(code, type) {
    var card = document.createElement('article');
    card.className = 'depoimentos-embed reveal visible';

    var path = type === 'reel' ? 'reel' : 'p';
    var embedUrl = 'https://www.instagram.com/' + path + '/' + code + '/embed/captioned/';

    card.innerHTML =
      '<iframe ' +
      'src="' + embedUrl + '" ' +
      'title="Depoimento Split Motorsport no Instagram" ' +
      'class="depoimentos-embed__iframe" ' +
      'loading="lazy" ' +
      'allow="autoplay; encrypted-media; picture-in-picture" ' +
      'allowfullscreen ' +
      'referrerpolicy="no-referrer-when-downgrade">' +
      '</iframe>';

    return card;
  }

  function renderEmbeds(codes) {
    grid.innerHTML = '';
    var limit = Math.min(codes.length, 6);

    for (var i = 0; i < limit; i++) {
      grid.appendChild(createEmbedCard(codes[i], 'p'));
    }

    setStatus(
      limit > 0
        ? limit + ' depoimento(s) carregado(s) do destaque Depoimentos ⚙️.'
        : 'Nenhum depoimento disponível para exibir no momento.'
    );
  }

  function renderProfileFallback() {
    grid.innerHTML =
      '<article class="depoimentos-embed depoimentos-embed--profile reveal visible">' +
      '<iframe ' +
      'src="https://www.instagram.com/' + USERNAME + '/embed" ' +
      'title="Perfil Split Motorsport no Instagram" ' +
      'class="depoimentos-embed__iframe depoimentos-embed__iframe--profile" ' +
      'loading="lazy" ' +
      'allow="autoplay; encrypted-media; picture-in-picture" ' +
      'allowfullscreen ' +
      'referrerpolicy="no-referrer-when-downgrade">' +
      '</iframe>' +
      '</article>';

    setStatus(
      'Toque em Depoimentos ⚙️ para ver todos os relatos de clientes no Instagram. ' +
      'Abaixo, conteúdo recente de @' + USERNAME + '.'
    );
  }

  function loadHighlightEmbeds() {
    setStatus('Carregando depoimentos do Instagram…');

    fetch('https://api.allorigins.win/raw?url=' + encodeURIComponent(HIGHLIGHT_URL))
      .then(function (response) {
        if (!response.ok) throw new Error('fetch failed');
        return response.text();
      })
      .then(function (html) {
        var codes = extractGraphqlCodes(html).concat(extractMediaCodes(html));
        codes = codes.filter(function (code, index) {
          return codes.indexOf(code) === index;
        });

        if (codes.length > 0) {
          renderEmbeds(codes);
        } else {
          renderProfileFallback();
        }
      })
      .catch(function () {
        renderProfileFallback();
      });
  }

  loadHighlightEmbeds();
})();
