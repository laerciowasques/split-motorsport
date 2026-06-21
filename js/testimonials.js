/**
 * Depoimentos — avaliações Google (Split Motorsport)
 * https://share.google/lH3b8jPVgYifp3KuI
 */
(function () {
  'use strict';

  var DEFAULT_SOURCE = 'https://share.google/lH3b8jPVgYifp3KuI';
  var grid = document.getElementById('depoimentosGrid');
  var status = document.getElementById('depoimentosStatus');
  var summaryRating = document.getElementById('depoimentosRating');
  var summaryCount = document.getElementById('depoimentosCount');
  var sourceLink = document.getElementById('depoimentosGoogleLink');

  if (!grid || !status) return;

  function stars(count) {
    var value = Math.max(0, Math.min(5, count || 5));
    return '★★★★★'.slice(0, value) + '☆☆☆☆☆'.slice(0, 5 - value);
  }

  function setStatus(message) {
    status.textContent = message;
  }

  function renderStarsHtml(count) {
    return '<span class="google-review-card__stars" aria-label="' + count + ' estrelas">' + stars(count) + '</span>';
  }

  function createReviewCard(review) {
    var card = document.createElement('article');
    card.className = 'google-review-card reveal visible';

    var initial = (review.author || 'C').trim().charAt(0).toUpperCase();
    var author = review.author || 'Cliente Google';
    var text = review.text || '';

    card.innerHTML =
      '<header class="google-review-card__header">' +
      '<span class="google-review-card__avatar" aria-hidden="true">' + initial + '</span>' +
      '<div>' +
      '<strong class="google-review-card__author">' + author + '</strong>' +
      renderStarsHtml(review.rating || 5) +
      '</div>' +
      '<span class="google-review-card__brand" aria-label="Avaliação no Google">G</span>' +
      '</header>' +
      '<blockquote class="google-review-card__quote">' + text + '</blockquote>';

    return card;
  }

  function renderEmbed(data) {
    var embedUrl = data.mapsEmbedUrl || 'https://www.google.com/maps?q=Split+Motorsport&output=embed&hl=pt-BR';
    var article = document.createElement('article');
    article.className = 'depoimentos-google__embed reveal visible';
    article.innerHTML =
      '<iframe ' +
      'src="' + embedUrl + '" ' +
      'title="Split Motorsport no Google Maps" ' +
      'class="depoimentos-google__iframe" ' +
      'loading="lazy" ' +
      'allowfullscreen ' +
      'referrerpolicy="no-referrer-when-downgrade">' +
      '</iframe>';
    grid.appendChild(article);
  }

  function renderData(data) {
    var sourceUrl = data.sourceUrl || DEFAULT_SOURCE;

    if (sourceLink) sourceLink.href = sourceUrl;

    if (summaryRating) {
      summaryRating.textContent = (data.rating || 5).toFixed(1).replace('.', ',');
    }

    if (summaryCount) {
      summaryCount.textContent = data.reviewCount
        ? data.reviewCount + ' avaliações no Google'
        : 'Avaliações verificadas no Google';
    }

    grid.innerHTML = '';

    if (data.reviews && data.reviews.length) {
      data.reviews.forEach(function (review) {
        grid.appendChild(createReviewCard(review));
      });
      setStatus('Depoimentos reais publicados no Google pela Split Motorsport.');
    } else {
      renderEmbed(data);
      setStatus('Veja as avaliações completas no Google ou explore a oficina no mapa abaixo.');
    }
  }

  fetch('data/google-reviews.json')
    .then(function (response) {
      if (!response.ok) throw new Error('json failed');
      return response.json();
    })
    .then(renderData)
    .catch(function () {
      renderData({
        sourceUrl: DEFAULT_SOURCE,
        rating: 5,
        reviewCount: 0,
        reviews: []
      });
    });
})();
