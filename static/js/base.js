var bScroll = true;

$(document).ready(function () {
  // dynamic settings
  set_footer();

  // event
  $(window).resize(function () {
    set_footer();
  });

  $(".back-to-top").click(function () {
    $("html,body").animate({scrollTop: 0}, 500, "swing");
    return false;
  });

  $(window).scroll(function () {
    scrollHandleNow();

    // ------------------------------------------------------------
    // scrollHandle that can be optimized as executed every certain period
    if(bScroll) {
      scrollHandle();
      // handle scroll every 50
      bScroll = false;
      setTimeout(function () {
        scrollHandle();
        bScroll = true;
      }, 50);
    }
    // ------------------------------------------------------------
  }); // scroll

}); // ready

function scrollHandleNow() {

}

function scrollHandle() {
  height = $(window).scrollTop();
  if (height > 0) {
    $(".back-to-top").show("drop", 500);
  } else {
    $(".back-to-top").hide("drop", 500);
  }
}

function scrollToAnchor(id) {
  var anchor = $(id);
  $("html,body").animate({scrollTop: anchor.offset().top}, 500, "swing");
  setTimeout(function () {
  }, 600);
}

function set_footer() {
  var footer_height = $("footer").height();
  if($("body").height() < $("html").height()) {
    console.log("DEBUG: body.height < html.height");
    $("html, body").css({"height": "100%"});
    $("footer").css({"position": "absolute", "bottom": "0"});
    // $(".main-container").css({"padding-bottom": footer_height+20});
  } else {
    $("html, body").css({"height": ""});
    $("footer").css({"position": "", "bottom": ""});
  }
}
