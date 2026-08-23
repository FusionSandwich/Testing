-- PDF-only layout adjustments for the manuscript's exact comparison tables.

local widths = {
  [2] = {0.25, 0.75},
  [3] = {0.24, 0.36, 0.40},
  [4] = {0.08, 0.25, 0.40, 0.27},
  [5] = {0.17, 0.21, 0.22, 0.12, 0.28},
  [8] = {0.15, 0.25, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10},
}

function Table(table)
  if not FORMAT:match("latex") then
    return table
  end
  local selected = widths[#table.colspecs]
  if #table.colspecs == 5 and
     pandoc.utils.stringify(table.head):match("Numbered result") then
    selected = {0.14, 0.33, 0.10, 0.15, 0.28}
  elseif #table.colspecs == 5 and
         pandoc.utils.stringify(table.head):match("Manuscript result") then
    selected = {0.18, 0.205, 0.19, 0.185, 0.24}
  elseif #table.colspecs == 5 and
         pandoc.utils.stringify(table.head):match("Source and variables") then
    selected = {0.19, 0.22, 0.21, 0.12, 0.26}
  end
  if selected then
    for index, width in ipairs(selected) do
      table.colspecs[index][2] = width
    end
  end
  return table
end

function Code(code)
  if FORMAT:match("latex") and
     (code.text:match("/") or code.text:match("_") or
      code.text:match("%.[A-Za-z0-9]+$")) then
    return pandoc.RawInline("latex", "\\nolinkurl{" .. code.text .. "}")
  end
  return code
end
