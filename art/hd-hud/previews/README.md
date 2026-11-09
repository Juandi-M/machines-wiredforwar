# Assembled artwork previews

`command-widget-with-grid-v1.png` shows the housing with the green grid inserted,
composed by the built-in image-generation tool from the two saved masters. Its
exact prompt is saved beside it. This is an illustrative artwork preview, not a
game screenshot or an exported runtime texture.

The game draws the housing and its contents separately in
`MachGuiFPCommand::doDisplay()`: the common empty grid (or the selected unit's
portrait) is overlaid at logical offset (43, 50). Both HD layers are already in
the mod. The housing master deliberately remains separate so it can support
either content. Model-specific portraits remain unchanged.
