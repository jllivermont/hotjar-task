function _create_script(url) {
  var script = document.createElement("script");
  script.setAttribute("src", url);
  script.async = false;
  document.head.appendChild(script);
}

function load_remote_scripts() {
  var script_urls = ["https://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.4/jquery.min.js", "https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js", "https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap-wizard/1.2/jquery.bootstrap.wizard.min.js"];
  script_urls.map(_create_script);
}

function _load_remote_css(url) {
  var link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = '';
  document.getElementsByTagName('head')[0].appendChild(link);
}

function load_remote_css() {
  var css_urls = ["https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css", "https://hotjar-task.herokuapp.com/sylesheet"];
  css_urls.map(_load_remote_css);
}

function onload() {
  $(document).ready(function() {
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
  });
}

function delayed_load() {
  load_remote_scripts();
  load_remote_css();

  $("div.popup-survey").load("https://hotjar-task.herokuapp.com/widget", onload);
}

setTimeout(delayed_load, 2000);
