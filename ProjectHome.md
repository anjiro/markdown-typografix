A python markdown extension for automatic typographic tweaks :
  * Avoid widows by adding a non-breaking space between two last words inside each block element (works correctly even with inline tags around those words).
  * Replaces " " with « »
  * Replaces --- and -- with em and en dashes
  * Fixes spacing around punctuation to match classic french typographic rules

Compatible with django.contib.markup, use {% var|markdown:"safe,typografix" %} and have the extension in your path.

To do:
  * Configuration for other languages
  * Testing code
  * Support for smileys