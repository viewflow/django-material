// Ripple effect for buttons and other elements with up-ripple attribute
up.compiler("[up-ripple]", function(elementWithRipple) {
  elementWithRipple.addEventListener('pointerdown', (mouseEvent) => {
    // Set the ripple position custom properties
    elementWithRipple.style.setProperty('--ripple-x', `${mouseEvent.offsetX}px`);
    elementWithRipple.style.setProperty('--ripple-y', `${mouseEvent.offsetY}px`);
  });
});