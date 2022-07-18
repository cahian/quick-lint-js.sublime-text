// Copyright (C) 2020  Matthew "strager" Glazar
// See end of file for extended copyright information.

#ifndef QUICK_LINT_JS_SUBLIME_TEXT_INTERFACE_H
#define QUICK_LINT_JS_SUBLIME_TEXT_INTERFACE_H

#include <stddef.h>

#if defined(__cplusplus)
extern "C" {
#endif

typedef unsigned int qljs_st_offset;

typedef enum qljs_st_severity {
  qljs_st_severity_error = 1,
  qljs_st_severity_warning = 2,
} qljs_st_severity;

typedef struct qljs_st_text {
  char *content;
  size_t length;
} qljs_st_text;

typedef struct qljs_st_region {
  qljs_st_offset start;
  qljs_st_offset end;
} qljs_st_region;

#if QUICK_LINT_JS_SUBLIME_TEXT_HAVE_INCREMENTAL_CHANGES
typedef struct qljs_st_position {
  qljs_st_offset line;
  qljs_st_offset character;
} qljs_st_position;
#else
typedef qljs_st_offset qljs_st_position;
#endif

#if QUICK_LINT_JS_SUBLIME_TEXT_HAVE_INCREMENTAL_CHANGES
typedef struct qljs_st_range {
  qljs_st_position start;
  qljs_st_position end;
} qljs_st_range;
#else
typedef qljs_st_region qljs_st_range;
#endif

typedef struct qljs_st_diagnostic {
  const qljs_st_range *range;
  qljs_st_severity severity;
  const char *code;
  const char *message;
} qljs_st_diagnostic;

typedef struct qljs_st_document qljs_st_document;

qljs_st_document *qljs_st_document_new(void);

void qljs_st_document_delete(qljs_st_document *self);

void qljs_st_document_set_text(qljs_st_document *self, qljs_st_text t);

#if QUICK_LINT_JS_SUBLIME_TEXT_HAVE_INCREMENTAL_CHANGES
void qljs_st_document_replace_text(qljs_st_document *self, const qljs_st_range r, const qljs_st_text t);
#endif

const qljs_st_diagnostic *qljs_st_document_lint(qljs_st_document *self);

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