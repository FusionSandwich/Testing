-- PDF-only layout adjustments for the manuscript's exact comparison tables.

local widths = {
  [2] = {0.25, 0.75},
  [3] = {0.24, 0.36, 0.40},
  [4] = {0.08, 0.25, 0.40, 0.27},
  [5] = {0.19, 0.22, 0.24, 0.12, 0.23},
  [8] = {0.15, 0.25, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10},
}

function Table(table)
  if not FORMAT:match("latex") then
    return table
  end
  local selected = widths[#table.colspecs]
  if selected then
    for index, width in ipairs(selected) do
      table.colspecs[index][2] = width
    end
  end
  return table
end

function Code(code)
  if FORMAT:match("latex") and
     (code.text:match("/") or code.text:match("%.[A-Za-z0-9]+$")) then
    return pandoc.RawInline("latex", "\\nolinkurl{" .. code.text .. "}")
  end
  return code
end
