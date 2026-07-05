/* Marianne Wilson — site behaviour: nav state, splash entry, carousel */
(function(){
  "use strict";

  /* ---------- FOOTER year ---------- */
  var yearEl = document.querySelector("[data-year]");
  if(yearEl){ yearEl.textContent = new Date().getFullYear(); }

  /* ---------- NAV scroll state ---------- */
  var nav = document.querySelector(".site-nav");
  if(nav){
    var onScroll = function(){
      if(window.scrollY > 8){ nav.classList.add("is-scrolled"); }
      else{ nav.classList.remove("is-scrolled"); }
    };
    onScroll();
    window.addEventListener("scroll", onScroll, {passive:true});
  }

  /* ---------- SPLASH entry ---------- */
  var splash = document.querySelector(".splash");
  if(splash){
    var entered = false;
    function enterSite(){
      if(entered) return;
      entered = true;
      var href = (splash.querySelector("[data-enter]") || {}).getAttribute("href") || "works.html";
      splash.style.transition = "opacity .5s ease";
      splash.style.opacity = "0";
      setTimeout(function(){ window.location.href = href; }, 420);
    }
    requestAnimationFrame(function(){
      requestAnimationFrame(function(){ splash.classList.add("is-ready"); });
    });
    splash.querySelectorAll("[data-enter]").forEach(function(el){
      el.addEventListener("click", function(e){
        e.preventDefault();
        enterSite();
      });
    });
    /* scroll gesture — wheel down or finger-swipe down triggers entry */
    splash.addEventListener("wheel", function(e){
      if(e.deltaY > 0){ enterSite(); }
    }, {passive:true});
    var touchStartY = null;
    splash.addEventListener("touchstart", function(e){
      touchStartY = e.changedTouches[0].clientY;
    }, {passive:true});
    splash.addEventListener("touchend", function(e){
      if(touchStartY === null) return;
      var dy = e.changedTouches[0].clientY - touchStartY;
      if(dy < -30){ enterSite(); } /* swipe up */
      touchStartY = null;
    }, {passive:true});
  }

  /* ---------- CAROUSEL ---------- */
  function initCarousel(root){
    var track = root.querySelector(".carousel__track");
    var slides = Array.prototype.slice.call(root.querySelectorAll(".carousel__slide"));
    var prevBtn = root.querySelector(".carousel__arrow--prev");
    var nextBtn = root.querySelector(".carousel__arrow--next");
    var dots = Array.prototype.slice.call(root.querySelectorAll(".carousel__dot"));
    var counter = root.querySelector(".carousel__counter");
    var index = 0;
    var total = slides.length;

    function render(){
      track.style.transform = "translateX(-" + (index * 100) + "%)";
      dots.forEach(function(d,i){ d.classList.toggle("is-active", i === index); });
      if(counter){ counter.textContent = (index+1) + " / " + total; }
    }

    function go(i){
      index = (i + total) % total;
      render();
    }

    if(prevBtn){ prevBtn.addEventListener("click", function(){ go(index-1); }); }
    if(nextBtn){ nextBtn.addEventListener("click", function(){ go(index+1); }); }
    dots.forEach(function(d,i){ d.addEventListener("click", function(){ go(i); }); });

    root.setAttribute("tabindex", "0");
    root.addEventListener("keydown", function(e){
      if(e.key === "ArrowLeft"){ go(index-1); }
      if(e.key === "ArrowRight"){ go(index+1); }
    });

    /* touch swipe */
    var startX = null;
    var viewport = root.querySelector(".carousel__viewport");
    viewport.addEventListener("touchstart", function(e){ startX = e.touches[0].clientX; }, {passive:true});
    viewport.addEventListener("touchend", function(e){
      if(startX === null) return;
      var dx = e.changedTouches[0].clientX - startX;
      if(Math.abs(dx) > 40){ go(dx < 0 ? index+1 : index-1); }
      startX = null;
    }, {passive:true});

    if(total <= 1){
      if(prevBtn) prevBtn.style.display = "none";
      if(nextBtn) nextBtn.style.display = "none";
    }

    render();
  }

  document.querySelectorAll(".carousel").forEach(initCarousel);

  /* ---------- WORKS SORT ---------- */
  var sortGroup = document.querySelector("[data-sort-group]");
  var worksGrid = document.querySelector("[data-works-grid]");
  if(sortGroup && worksGrid){
    var cards = Array.prototype.slice.call(worksGrid.children);
    var mediumSubWrap = document.querySelector("[data-medium-sub]");
    var mediumSub = mediumSubWrap && mediumSubWrap.querySelector(".works-sort__sub");
    var activeFilter = null;

    /* Default: alphabetical by title */
    function alphabeticalOrder(){
      return cards.slice().sort(function(a,b){
        return (a.getAttribute("data-title") || "").localeCompare(b.getAttribute("data-title") || "");
      });
    }
    var defaultOrder = alphabeticalOrder();

    function getActiveBtn(){ return sortGroup.querySelector("[data-sort].is-active"); }
    function getSubBtn(){ return mediumSub && mediumSub.querySelector(".is-active"); }

    function renderCards(sorted){
      sorted.forEach(function(card){ worksGrid.appendChild(card); });
    }

    function sortWorks(mode, dir){
      var sorted;
      if(mode === "default"){
        sorted = alphabeticalOrder();
        if(mediumSubWrap) mediumSubWrap.classList.remove("is-open");
        activeFilter = null;
      } else if(mode === "price"){
        sorted = cards.slice().sort(function(a,b){
          return (parseFloat(a.getAttribute("data-price")) || 0) - (parseFloat(b.getAttribute("data-price")) || 0);
        });
        if(dir === "desc") sorted.reverse();
        if(mediumSubWrap) mediumSubWrap.classList.remove("is-open");
        activeFilter = null;
      } else if(mode === "size"){
        sorted = cards.slice().sort(function(a,b){
          return (parseFloat(a.getAttribute("data-size")) || 0) - (parseFloat(b.getAttribute("data-size")) || 0);
        });
        if(dir === "desc") sorted.reverse();
        if(mediumSubWrap) mediumSubWrap.classList.remove("is-open");
        activeFilter = null;
      }
      /* apply medium filter if one is active */
      if(activeFilter){
        sorted = sorted.filter(function(c){
          return c.getAttribute("data-medium") === activeFilter;
        });
      }
      renderCards(sorted);
    }

    /* main sort buttons */
    sortGroup.querySelectorAll("[data-sort]").forEach(function(btn){
      btn.addEventListener("click", function(e){
        var mode = btn.getAttribute("data-sort");
        if(mode === "medium"){
          /* toggle the sub-options slide open/closed */
          var isOpening = !mediumSubWrap.classList.contains("is-open");
          mediumSubWrap.classList.toggle("is-open");
          var arrow = btn.querySelector("[data-arrow]");
          if(arrow) arrow.textContent = isOpening ? "←" : "→";
          if(isOpening){
            sortGroup.querySelectorAll("[data-sort]").forEach(function(b){ b.classList.remove("is-active"); });
            btn.classList.add("is-active");
            /* render current filter or all */
            var subActive = getSubBtn();
            activeFilter = subActive ? subActive.getAttribute("data-filter") : null;
            renderCards(activeFilter ? cards.filter(function(c){ return c.getAttribute("data-medium") === activeFilter; }) : cards.slice());
          } else {
            btn.classList.remove("is-active");
            activeFilter = null;
            /* revert to default */
            sortGroup.querySelectorAll("[data-sort]").forEach(function(b){ b.classList.remove("is-active"); });
            sortGroup.querySelector("[data-sort='default']").classList.add("is-active");
            renderCards(alphabeticalOrder());
          }
          return;
        }
        /* close medium sub if open */
        if(mediumSubWrap) mediumSubWrap.classList.remove("is-open");
        activeFilter = null;

        sortGroup.querySelectorAll("[data-sort]").forEach(function(b){ b.classList.remove("is-active"); });
        btn.classList.add("is-active");

        var dir = btn.getAttribute("data-dir") || "asc";
        sortWorks(mode, dir);
      });
    });

    /* medium sub-option buttons */
    if(mediumSub){
      mediumSub.querySelectorAll("[data-filter]").forEach(function(subBtn){
        subBtn.addEventListener("click", function(){
          mediumSub.querySelectorAll("[data-filter]").forEach(function(b){ b.classList.remove("is-active"); });
          subBtn.classList.add("is-active");
          activeFilter = subBtn.getAttribute("data-filter");
          renderCards(cards.filter(function(c){ return c.getAttribute("data-medium") === activeFilter; }));
          /* close the slide and reset arrow */
          mediumSubWrap.classList.remove("is-open");
          var medBtn = sortGroup.querySelector("[data-sort='medium']");
          if(medBtn){
            var arrow = medBtn.querySelector("[data-arrow]");
            if(arrow) arrow.textContent = "→";
          }
        });
      });
    }

    /* toggle direction on price / size */
    sortGroup.querySelectorAll("[data-dir]").forEach(function(btn){
      btn.addEventListener("click", function(){
        var mode = btn.getAttribute("data-sort");
        if(mode === "medium" || mode === "default") return;
        var dir = btn.getAttribute("data-dir");
        var newDir = dir === "asc" ? "desc" : "asc";
        btn.setAttribute("data-dir", newDir);
        var arrow = btn.querySelector("[data-arrow]");
        if(arrow) arrow.textContent = newDir === "asc" ? "↑" : "↓";

        sortGroup.querySelectorAll("[data-sort]").forEach(function(b){ b.classList.remove("is-active"); });
        btn.classList.add("is-active");
        if(mediumSubWrap) mediumSubWrap.classList.remove("is-open");
        activeFilter = null;
        sortWorks(mode, newDir);
      });
    });

    /* set initial default */
    renderCards(defaultOrder);
  }

})();
