function popup() {
  var options = 'height=550,width=575';

  // Figure out the coordinates to place the popup in the middle of the screen
  var height = Math.floor(window.screen.height / 3);
  var width = Math.floor(window.screen.width / 3);

  options = options + ",top=" + height + ",left=" + width; 

  var new_window = window.open('https://hotjar-task.herokuapp.com/widget', 'Survey', options);
  new_window.focus();
}

setTimeout(popup, 2000);
