var _SURVEY_SELECTORS = {
  "name": "input#name",
  "email": "input#email",
  "age": "input#age",
  "about_me": "textarea#about_me",
  "gender": "input[name='gender']",
  "address": "textarea#address",
  "favorite_book": "input#favorite_book",
  "favorite_colors": "input[name='colors']",
};

var _SurveyEventHandler = {
  // Persists the latest form values into local storage
  "updateLocalStorage": function(values) {
    if (typeof(Storage) !== undefined) {
      var persisted_values = localStorage.getItem("form-values");
      var current_values = JSON.stringify(values);

      if (current_values !== persisted_values) {
        localStorage.setItem("form-values", JSON.stringify(values));
      }
    }
  },

  // Gathers up and returns all values
  "getFormValues": function() {
    var values = {};

    values.name = $(Survey.SELECTORS.name).val();
    values.email = $(Survey.SELECTORS.email).val();
    values.age = $(Survey.SELECTORS.age).val();
    values.about_me = $(Survey.SELECTORS.about_me).val();
    values.gender = $(Survey.SELECTORS.gender + ":checked").val();
    values.address = $(Survey.SELECTORS.address).val();

    values.favorite_book = $(Survey.SELECTORS.favorite_book).val();
    values.favorite_colors = $(Survey.SELECTORS.favorite_colors + ":checked").map(function() {
      return this.value;
    }).get().join(",");

    _SurveyEventHandler.updateLocalStorage(values);

    return values;
  },

  // Determines if enough values have been provided for the form to be submitted
  "isFormFinishable": function() {
    var required_field_keys = ["name", "email", "age", "about_me"];
    var result = true;

    for (var i = 0; i < required_field_keys.length; i++) {
      var key_name = required_field_keys[i];
      var selector = Survey.SELECTORS[key_name];

      if ($(selector).val().length === 0) {
        result = false;
        break;
      }
    }

    return result;
  },


  // Checks to see if Finish button should be displayed; persists current state of form
  "blurHandler": function() {
    if (_SurveyEventHandler.isFormFinishable() === true) {
      $("li#finish").removeClass("disabled");
    }

    _SurveyEventHandler.getFormValues();
  },
};

var _SurveyBootstrapper = {
  // Sets values from local storage into the form
  "setFormValue": function(key, value) {
    var value_set = false;

    if (value.length > 0) {
      if (key == "gender") {
        $(Survey.SELECTORS[key] + "[value='" + value.toLowerCase() + "']").attr("checked", true);
        value_set = true;
      } else if (key == "favorite_colors") {
        var colors = value.split(",");
        for (var index in colors) {
          var color = colors[index];
          // Capitalize the color
          color = color[0].toUpperCase() + color.slice(1);
          $(Survey.SELECTORS[key] + "[value='" + color + "']").attr("checked", true);
          value_set = true;
        }
      } else {
        $(Survey.SELECTORS[key]).val(value);
        value_set = true;
      }
    }

    return value_set;
  },

  // Check local stroage for any previously-entered values
  "populateFormFromLocalStorage": function() {
    var values_set = false;

    if (typeof(Storage) !== undefined) {
    var persisted_values = localStorage.getItem("form-values");
    if (persisted_values !== null) {
      var values = JSON.parse(persisted_values);

      for (var key in values) {
        value = values[key];
        if (_SurveyBootstrapper.setFormValue(key, value) === true) {
          values_set = true;
        }
      }
    }
    }

    return values_set;
  },

  // Check if this user has already completed the survey
  "isSurveyAlreadyFinished": function() {
    result = false;
    if (typeof(Storage) !== undefined) {
      if (localStorage.getItem("survey-finished") !== null) {
        result = true;
      }
    }

    return result;
  },

  // If we found values in local storage, inform the user that they are continuing the survey
  "setWelcomeBackMessage": function() {
    $("li#intro > a").text("Welcome Back!");   
    $("div#tab1").empty();
    $("div#tab1").append("<p>You didn't complete the survey before, so we've saved the data you input during your last session.</p>");
    $("div#tab1").append("<p>You can continue filling out the survey right where you left off last time.</p>");
    $("li#next > a").text("Continue Survey");
  },

  // If we find that the user has already completed the survey, thank them and send them away
  "setAlreadyFinishedMessage": function() {
    $("li#intro > a").text("Survey Already Completed");   
    $("div#tab1").empty();
    $("div#tab1").append("<p>You have already completed this survey.  There's nothing more to do.</p>");
    $("div#tab1").append("<p>Thanks!!</p>");
    $("li#next > a").hide();
    $("li#finish").removeClass("disabled");
  },

  // When the user clicks on the Start/Continue button on the first tab
  "onStartButtonClicked": function() {
    $("li#next > a").text("Next");
    $("li#name").removeClass("disabled");
    $("li#age").removeClass("disabled");
    $("li#address").removeClass("disabled");
    $("li#favorites").removeClass("disabled");
    $("li#intro").remove();

    if (_SurveyEventHandler.isFormFinishable() === true) {
      $("li#finish").removeClass("disabled");
    }
  },

  // When the user clicks on the Finish button
  "onFinishButtonClicked": function() {
    if (typeof(Storage) !== undefined) {
      localStorage.removeItem("form-values");
      localStorage.setItem("survey-finished", true);
    }

    $("div.popup-survey").hide();
  },

  // When the widget has finished loading 
  "onWidgetLoaded": function() {
    $(document).ready(function() {
      $("#rootwizard").bootstrapWizard({
        onTabShow: function(tab, navigation, index) {
          var $total = navigation.find("li").length;
          var $current = index + 1;
        }
      });

      // Register event handlers for the Next and Finish buttons
      $("li#next > a").on("click", _SurveyBootstrapper.onStartButtonClicked);
      $("#rootwizard .finish").on("click", _SurveyBootstrapper.onFinishButtonClicked);

      // Register blur event handlers for blur events
      $("input").blur(Survey.EventHandler.blurHandler);
      $("textarea").blur(Survey.EventHandler.blurHandler);

      // Check to see if this user has already completed a survey
      if (_SurveyBootstrapper.isSurveyAlreadyFinished()) {
        _SurveyBootstrapper.setAlreadyFinishedMessage();
      // Populate the form with any previously-entered values
      } else if (_SurveyBootstrapper.populateFormFromLocalStorage()) {
        _SurveyBootstrapper.setWelcomeBackMessage();
      }
    });
  },
};
 
// Plumb these sub-namespaces into the global Survey namespace
Survey.Bootstrapper = Survey.Bootstrapper || _SurveyBootstrapper;
Survey.EventHandler = Survey.EventHandler || _SurveyEventHandler;
Survey.SELECTORS = Survey.SELECTORS || _SURVEY_SELECTORS;
