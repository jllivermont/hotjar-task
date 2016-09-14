var _SURVEY_SELECTORS = {
  "name": "input#name",
  "email": "input#email",
  "age": "select#age",
  "about_me": "textarea#about_me",
  "gender": "input[name='gender']",
  "address": "textarea#address",
  "favorite_book": "input#favorite_book",
  "favorite_colors": "input[name='colors']",
};

// Manages model state both locally and with the backend
var _SurveyResponseManager = {
  // Create a new SurveyResponse
  "createSurveyResponse": function(values) {
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
  "syncToBackend": function(finished) {
    values = _SurveyResponseManager.getFormValues();

    // If the finished parameter is set, add a finished attribute to the values
    if (finished) {
      values.finished = true;
    }

    // Only send an update to the back-end if we have a name, an email and modified values
    if ((_SurveyResponseManager.updateLocalStorage(values) === true) && (values.name.length > 0) && (values.email.length > 0)) {
      values = JSON.stringify(values);

      if (localStorage.getItem("response-id") === null) {
        _SurveyResponseManager.createSurveyResponse(values);
      } else {
        _SurveyResponseManager.updateSurveyResponse(values);
      }
    }
  },

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

    if (values.age === null) {
      values.age = "";
    }

    return values;
  },
};

// Manages event handling 
var _SurveyEventHandler = {
  // Checks to see if Finish button should be displayed; persists current state of form
  "blurHandler": function() {
    if (Survey.Controller.isFormFinishable() === true) {
      $("li#finish").removeClass("disabled");
    } else {
      $("li#finish").addClass("disabled");
    }

    Survey.ResponseManager.syncToBackend(false);
  },

  // When the user clicks on the Start/Continue button on the first tab
  "onStartButtonClicked": function() {
    Survey.Controller.removeIntroTab();
    Survey.Controller.checkFinishButton();

    Survey.EventHandler.registerHandlers();
    $("span#close-button").show();
  },

  // When the user clicks on the close button in the upper right-hand corner
  "onCloseButtonClicked": function() {
    Survey.ResponseManager.syncToBackend(false);
    $("div.popup-survey").hide();
  },

  // When the user clicks on the Finish button
  "onFinishButtonClicked": function() {
    // Send one final update to the back-end with the latest values and marking the survey as finished
    Survey.ResponseManager.syncToBackend(true);

    if (typeof(Storage) !== undefined) {
      localStorage.removeItem("form-values");
      localStorage.removeItem("response-id");
      localStorage.removeItem("current-tab");
      localStorage.setItem("survey-finished", true);
    }

    $("div.popup-survey").hide();
  },

  // Registers all event handlers
  "registerHandlers": function() {
    // Register event handler for the Finish button
    $("#rootwizard .finish").on("click", _SurveyEventHandler.onFinishButtonClicked);

    // Register blur event handlers
    $("input").blur(_SurveyEventHandler.blurHandler);
    $("textarea").blur(_SurveyEventHandler.blurHandler);
    $("select").blur(_SurveyEventHandler.blurHandler);
  },
};


var _SurveyController = {
  // Determines if enough values have been provided for the form to be submitted
  "isFormFinishable": function() {
    var required_field_keys = ["name", "email", "age", "about_me"];
    var result = true;

    for (var i = 0; i < required_field_keys.length; i++) {
      var key_name = required_field_keys[i];
      var selector = Survey.SELECTORS[key_name];
      var value = $(selector).val();

      if ((value === null) || (value.length === 0)) {
        result = false;
        break;
      }
    }

    return result;
  },

  // Removes the Introduction tab and updates navigation buttons
  "removeIntroTab": function() {
    $("li#next > a").text("►");
    $("div.navbar").show();
    $("li#nav1").remove();
    $("div#tab1").remove();
  },

  // Navigates to the tab the user was last on
  "navigateToLastTab": function() {
    // Remove the active tag from all tabs and tab headers
    $("ul.nav li").removeClass("active");
    $("div.tab-content div").removeClass("active");

    current_tab = localStorage.getItem("current-tab");
    if (current_tab !== null) {
      $("li#nav" + (Number(current_tab) + 1)).addClass("active");
      $("div#tab" + (Number(current_tab) + 1)).addClass("active");
    }
  },

  // Displays the Finish button if enough of the survey has been completed
  "checkFinishButton": function() {
    if (_SurveyController.isFormFinishable() === true) {
      $("li#finish").removeClass("disabled");
    }
  },
};


var _SurveyBootstrapper = {
  // Sets values from local storage into the form
  "setFormValue": function(key, value) {
    var value_set = false;

    if ((value !== null) && (value.length > 0)) {
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

  // Populate the options for the age <select>
  "populateAges": function() {
    var select = document.getElementById("age");
    var option = document.createElement("option");
    option.text = "Choose Your Age";
    option.value = "placeholder";
    option.selected = true;
    option.disabled = true;
    select.appendChild(option);

    for (var i = 5; i <= 130; i++) {
      option = document.createElement("option");
      option.text = i;
      option.value = i;
      select.appendChild(option);
    }
  },

  "onWidgetLoaded": function() {
    $(document).ready(function() {
      // Populate the age <select>
      _SurveyBootstrapper.populateAges();

      // Populate the form with any previously-entered values
      if (_SurveyBootstrapper.populateFormFromLocalStorage()) {
        Survey.Controller.removeIntroTab();

        // Navigate to the last tab the user was on
        Survey.Controller.navigateToLastTab();
        Survey.Controller.checkFinishButton();

        // Enable handlers
        Survey.EventHandler.registerHandlers();
      } else {
        $("span#close-button").hide();
        $("li#next > a").on("click", Survey.EventHandler.onStartButtonClicked);
      }

      $("#rootwizard").bootstrapWizard({
        onTabShow: function(tab, navigation, index) {
          var $total = navigation.find("li").length;
          var $current = index + 1;

          // Every time we have a tab change, persist the current tab
          localStorage.setItem("current-tab", (index + 1));
        }
      });
    });
  },
};

// Plumb these sub-namespaces into the global Survey namespace
Survey.SELECTORS = Survey.SELECTORS || _SURVEY_SELECTORS;
Survey.EventHandler = Survey.EventHandler || _SurveyEventHandler;
Survey.ResponseManager = Survey.ResponseManager || _SurveyResponseManager;
Survey.Controller = Survey.Controller || _SurveyController;
Survey.Bootstrapper = Survey.Bootstrapper || _SurveyBootstrapper;
