// Copyright (C) 2020  Matthew "strager" Glazar
// See end of file for extended copyright information.

#ifndef QUICK_LINT_JS_SUBLIME_TEXT_INTERFACE_H
#define QUICK_LINT_JS_SUBLIME_TEXT_INTERFACE_H

#include <stddef.h>

#if defined(__cplusplus)
extern "C" {
#endif

typedef unsigned int qljs_st_offset;

typedef enum subl_severity {
  subl_severity_error = 1,
  subl_severity_warning = 2,
} subl_severity;

typedef struct subl_text {
  char *content;
  size_t length;
} subl_text;

typedef struct subl_region {
  subl_offset start;
  subl_offset end;
} subl_region;

#if QUICK_LINT_JS_SUBLIME_TEXT_HAVE_INCREMENTAL_CHANGES
typedef struct subl_position {
  subl_offset line;
  subl_offset character;
} subl_position;
#else
typedef subl_offset subl_position;
#endif

#if QUICK_LINT_JS_SUBLIME_TEXT_HAVE_INCREMENTAL_CHANGES
typedef struct subl_range {
  subl_position start;
  subl_position end;
} subl_range;
#else
typedef subl_region subl_range;
#endif

typedef struct subl_diagnostic {
  const subl_range *range;
  subl_severity severity;
  const char *code;
  const char *message;
} subl_diagnostic;

typedef struct subl_document subl_document;

subl_document *subl_document_new(void);

void subl_document_delete(subl_document *d);

void subl_document_set_text(subl_document *d, subl_text t);

#if QUICK_LINT_JS_SUBLIME_TEXT_HAVE_INCREMENTAL_CHANGES
void subl_document_replace_text(subl_document *d, const subl_range r, const subl_text t);
#endif

const subl_diagnostic *subl_document_lint(subl_document *d);

#if defined(__cplusplus)
}
#endif

#endif  // QUICK_LINT_JS_SUBLIME_TEXT_INTERFACE_H

// quick-lint-js finds bugs in JavaScript programs.
// Copyright (C) 2020  Matthew Glazar
//
// This file is part of quick-lint-js.
//
// quick-lint-js is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// quick-lint-js is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with quick-lint-js.  If not, see <https://www.gnu.org/licenses/>.
