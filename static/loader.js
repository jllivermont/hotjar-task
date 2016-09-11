var _SurveyLoader = {
  "onJqueryLoaded": function() {
    jQuery(document).ready(function($) {
      $("div.popup-survey").load("http://localhost:8000/widget.html", Survey.Bootstrapper.onWidgetLoaded);
    });
  },  

  // Load scripts and optionally invoke callback when script load has finished
  "createScript": function(url, callback) {
    var script = document.createElement("script");
    script.setAttribute("src", url);
    script.async = false;

    if (callback !== null) {
      script.onload = callback;

      // This is for IE
      script.onreadystatechange = function() {
        if (this.readyState == "complete") {
          callback();
        }
      };
    }

    document.head.appendChild(script);
  },

  "loadRemoteScripts": function() {
    _SurveyLoader.createScript("https://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.4/jquery.min.js", null);
    _SurveyLoader.createScript("https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js", null);
    _SurveyLoader.createScript("http://localhost:8000/survey.js", null);
    _SurveyLoader.createScript("https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap-wizard/1.2/jquery.bootstrap.wizard.min.js", _SurveyLoader.onJqueryLoaded);
  },

  // Load stylesheets
  "loadRemoteCSS": function() {
    var css_urls = ["https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css", "http://localhost:8000/stylesheet.css"];
    for (var index in css_urls) {
      var url = css_urls[index];
      var link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = url;
      document.getElementsByTagName("head")[0].appendChild(link);
    }
  },

  "delayedLoad": function() {
    _SurveyLoader.loadRemoteCSS();
    _SurveyLoader.loadRemoteScripts();
  }
};

// Build the Survey namespace
var Survey = Survey || {};
Survey.Loader = Survey.Loader || _SurveyLoader;

// Entrypoint, a delayed load after the hosting page load is wrapping up
setTimeout(Survey.Loader.delayedLoad, 200);
