function onload() {

  $('#rootwizard').bootstrapWizard({
    onTabShow: function(tab, navigation, index) {
      var $total = navigation.find('li').length;
      var $current = index + 1;
    }
  });

  // When the Start button is clicked on the Intro tab, enable the other tabs and remove the intro tab
  $("li#next > a").on("click", function() {
    $("li#next > a").text("Next");
    $("li#name").removeClass("disabled");
    $("li#age").removeClass("disabled");
    $("li#address").removeClass("disabled");
    $("li#favorites").removeClass("disabled");
    $("li#intro").remove();
  });

  $('#rootwizard .finish').click(function() {
    alert('Finished!, Starting over!');
    $('#rootwizard').find("a[href*='tab1']").trigger('click');
  });

  // This handler ensures that the Finish button is displayed only when we have the minimum values to complete the survey
  function blur_handler() {
    var required_fields = ["input#name", "input#email", "input#age", "textarea#about_me"];
    var result = true;

    for (var i = 0; i < required_fields.length; i++) {
      if ($(required_fields[i]).val().length === 0) {
        result = false;
        break;
      }
    }

    if (result == true) {
      $('li#finish').removeClass('disabled');
    }
  }

  $("input").blur(blur_handler);
  $("textarea").blur(blur_handler);
}

function jquery_loaded_callback() {
  jQuery(document).ready(function($) {
    $("div.popup-survey").load("https://hotjar-task.herokuapp.com/widget", onload);
  });
}

function _create_script(url, callback) {
  var script = document.createElement("script");
  script.setAttribute("src", url);
  script.async = false;

  if (callback !== null) {
    script.onload = callback;

    // This is for IE
    script.onreadystatechange = function() {
      if (this.readyState == 'complete') {
        callback();
      }
    }
  }

  document.head.appendChild(script);
}

function load_remote_scripts() {
  _create_script("https://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.4/jquery.min.js", null);
  _create_script("https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js", null);
  _create_script("https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap-wizard/1.2/jquery.bootstrap.wizard.min.js", jquery_loaded_callback);
}

function _load_remote_css(url) {
  var link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = url;
  document.getElementsByTagName('head')[0].appendChild(link);
}

function load_remote_css() {
  var css_urls = ["https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css", "https://hotjar-task.herokuapp.com/stylesheet"];
  css_urls.map(_load_remote_css);
}

function delayed_load() {
  load_remote_css();
  load_remote_scripts();
}

setTimeout(delayed_load, 2000);

//$(document).ready(function() {});
