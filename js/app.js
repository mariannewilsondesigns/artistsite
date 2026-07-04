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

})();
