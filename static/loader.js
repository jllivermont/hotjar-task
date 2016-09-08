function popup() {
  var new_window = window.open('https://hotjar-task.herokuapp.com/widget', 'Survey','height=500,width=500');
  new_window.focus();
}

setTimeout(popup, 2000);
