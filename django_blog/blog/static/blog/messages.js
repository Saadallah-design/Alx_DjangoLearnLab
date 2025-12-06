document.addEventListener('DOMContentLoaded', function() {
  const messages = document.querySelectorAll('.messages .message');
  messages.forEach(function(msg) {
    setTimeout(function() {
      msg.style.opacity = '0';
      setTimeout(function() { msg.remove(); }, 500);
    }, 3500);
  });
});
