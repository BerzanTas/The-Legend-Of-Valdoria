# Documentation

Hi! This file is for our future selves. Here I will write down the pygame functions used in our project and what they do.

## Contents
1. [pygame.display.get_surface()](#pygamedisplayget_surface)
2. [pygame.display.update()](#pygamedisplayupdate)

 ## pygame.display.get_surface()

Using `pygame.display.get_surface()` is particularly useful in more complex projects where multiple modules or functions may need access to the main display surface without having to pass it as an argument each time.

In summary, `pygame.display.get_surface()` provides a convenient way to **obtain a reference to the main surface on which all game elements are drawn**. This allows for a more flexible and modular approach to programming in Pygame.

## pygame.display.update()

The `pygame.display.update()` function is used to refresh the screen in Pygame. This means that whenever you make any changes to the screen, such as drawing shapes, changing the background color, etc., you need to call this function to make those changes visible to the user.

### How does it work?

1. **Refreshing the entire screen**:
   - When you call `pygame.display.update()` with no arguments, the entire screen surface will be refreshed, displaying all the changes that have been made since the last refresh.

2. **Partial refresh**:
   - You can also pass a rectangle (or a list of rectangles) to this function, specifying which areas of the screen should be refreshed. This can be more efficient if only a part of the screen has changed.


