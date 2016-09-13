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
    var updated = false;

    if (typeof(Storage) !== undefined) {
      var persisted_values = localStorage.getItem("form-values");
      var current_values = JSON.stringify(values);

      if (current_values !== persisted_values) {
        localStorage.setItem("form-values", JSON.stringify(values));
        updated = true;
      }
    }

    return updated;
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

  // Create a new SurveyResponse
  "createSurveyResponse": function(values) {
    values = JSON.stringify(values);
    $.ajax({
      "url": "http://hotjar-task.herokuapp.com/survey",
      "method": "POST",
      "contentType": "application/json",
      "data": values,
      "success": function(data, status, xhr) {
        localStorage.setItem("response-id", data.id);
      },
      "error": function(xhr, status, error) {
        console.error("Status code " + xhr.status + " and error '" + status + "' received; reason: " + error);
      },
    });
  },

  // Update an existing SurveyResponse
  "updateSurveyResponse": function(values) {
    // The email field is an immutable field and the backend won't allow it to be mutated; don't send it
    delete values.email;
    values = JSON.stringify(values);

    id = localStorage.getItem("response-id");
    $.ajax({
      "url": "http://hotjar-task.herokuapp.com/survey/" + id,
      "method": "PUT",
      "contentType": "application/json",
      "data": values,
      "error": function(xhr, status, error) {
        if (xhr.status != 200) {
          console.error("Status code " + xhr.status + " and error '" + status + "' received; reason: " + error);
        }
      },
    });
  },

  // Create or update the state of the SurveyResponse resource on the back-end
  "syncToBackend": function(values) {
    // Only send an update to the back-end if we have a name, an email and modified values
    if ((_SurveyEventHandler.updateLocalStorage(values) === true) && (values.name.length > 0) && (values.email.length > 0)) {
      if (localStorage.getItem("response-id") === null) {
        _SurveyEventHandler.createSurveyResponse(values);
      } else {
        _SurveyEventHandler.updateSurveyResponse(values);
      }
    }
  },

  // Checks to see if Finish button should be displayed; persists current state of form
  "blurHandler": function() {
    if (_SurveyEventHandler.isFormFinishable() === true) {
      $("li#finish").removeClass("disabled");
    }

    _SurveyEventHandler.syncToBackend(_SurveyEventHandler.getFormValues());
  },

  // When the user clicks on the Start/Continue button on the first tab
  "onStartButtonClicked": function() {
    $("li#next > a").text("Next");
    $("div.navbar").show();
    $("li#intro").remove();

    if (_SurveyEventHandler.isFormFinishable() === true) {
      $("li#finish").removeClass("disabled");
    }
  },

  // When the user clicks on the close button in the upper right-hand corner
  "onCloseButtonClicked": function() {
    var values = _SurveyEventHandler.getFormValues();
    _SurveyEventHandler.syncToBackend(values);
    $("div.popup-survey").hide();
  },

  // When the user clicks on the Finish button
  "onFinishButtonClicked": function() {
    // Send one final update to the back-end with the latest values and marking the survey as finished
    var values = _SurveyEventHandler.getFormValues();
    values.finished = true;
    _SurveyEventHandler.syncToBackend(values);

    if (typeof(Storage) !== undefined) {
      localStorage.removeItem("form-values");
      localStorage.removeItem("response-id");
      localStorage.setItem("survey-finished", true);
    }

    $("div.popup-survey").hide();
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

  // When the widget has finished loading 
  "onWidgetLoaded": function() {
    $(document).ready(function() {
      $("#rootwizard").bootstrapWizard({
        onTabShow: function(tab, navigation, index) {
          var $total = navigation.find("li").length;
          var $current = index + 1;
          localStorage.setItem("current-tab", (index + 1));
        }
      });

      // Register event handlers for the Next and Finish buttons
      $("li#next > a").on("click", Survey.EventHandler.onStartButtonClicked);
      $("#rootwizard .finish").on("click", Survey.EventHandler.onFinishButtonClicked);

      // Register blur event handlers for blur events
      $("input").blur(Survey.EventHandler.blurHandler);
      $("textarea").blur(Survey.EventHandler.blurHandler);

      // Populate the form with any previously-entered values
      if (_SurveyBootstrapper.populateFormFromLocalStorage()) {
        current_tab = localStorage.getItem("current-tab");
        if (current_tab !== null) {
          $("li#tab" + (current_tab + 1)).addClass("active");
        }
      }
    });
  },
};

// Plumb these sub-namespaces into the global Survey namespace
Survey.Bootstrapper = Survey.Bootstrapper || _SurveyBootstrapper;
Survey.EventHandler = Survey.EventHandler || _SurveyEventHandler;
Survey.SELECTORS = Survey.SELECTORS || _SURVEY_SELECTORS;
