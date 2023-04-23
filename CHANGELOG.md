# CHANGELOG

## [0.3.0] - YYYY-MM-DD
## [0.2.0] - 2023-04-23
## Added
 * Add dictionary support to choice prompt
   When a dictionary is passed in as the list of available options, the key is
   used as the display label and the value is the object returned when the user
   makes their selection.
 * Handle aborted selections cleanly
   If a user cancels a selection prompt (either by hitting `Esc` or `Ctrl-C`, a
   `SelectionAborted` exception is raised instead of the `KeyboardInterrupt`.
   This exception holds a reference to the item (or items) that were selected
   when the user aborted.
 * Support preselection for multiple choice prompts
   For multiple choice prompts, an iterable of either keys (for dict options)
   or indices (for list options) can be passed to specify the default values
   that should be selected when the prompt is shown.
   (Thanks to @constantin.braess on gitlab)
## Internal
 * Convert from Pipenv to Poetry
   This also introduces a `pyproject.toml` file as the config.
 * Use argparse instead of `click`
   `Click` was convenient but the CLI usage was never intended to be the primary
   use for this library so the additional dependency was never really justified.
