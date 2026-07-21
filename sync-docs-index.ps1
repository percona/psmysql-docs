# -----------------------------
# CONFIG
# -----------------------------
$docsPath   = Join-Path $PSScriptRoot "docs"
$outputFile = Join-Path $docsPath "index-contents.md"

# -----------------------------
# HELPERS
# -----------------------------
function Get-Heading {
    param ([string]$filePath)

    foreach ($line in Get-Content $filePath) {
        if ($line -match '^\s*#\s+(.+)') {
            return $matches[1].Trim()
        }
    }

    return [System.IO.Path]::GetFileNameWithoutExtension($filePath)
}

function Should-Ignore {
    param ([string]$path)

    return $path -match "[\\/](release-notes)[\\/]"
}

function Normalize-RelativePath {
    param ([string]$fullPath)

    $relative = $fullPath.Substring($docsPath.Length)

    return ($relative -replace '\\','/').TrimStart('/')
}

# -----------------------------
# COLLECT FILES
# -----------------------------
$files = Get-ChildItem $docsPath -Recurse -File -Filter "*.md" |
    Where-Object {
        $_.Name -ne "index-contents.md" -and
        -not (Should-Ignore $_.FullName)
    }

# -----------------------------
# BUILD TOPICS + VALIDATION
# -----------------------------
$topics = @()
$brokenLinks = @()

foreach ($file in $files) {

    $title = Get-Heading $file.FullName
    $relative = Normalize-RelativePath $file.FullName
    $link = "docs/$relative"

    # VALIDATION: ensure file still exists
    if (-not (Test-Path $file.FullName)) {
        $brokenLinks += $link
        continue
    }

    $topics += [PSCustomObject]@{
        Title = $title
        Path  = "./$relative"
    }
}

# -----------------------------
# SORT (GLOBAL ALPHABETICAL)
# -----------------------------
$topics = $topics | Sort-Object Title

# -----------------------------
# RENDER INDEX
# -----------------------------
$output = @()
$output += "# Documentation Index"
$output += ""
$output += "## Topics"
$output += ""

foreach ($t in $topics) {
    $output += "- [$($t.Title)]($($t.Path))"
}

# -----------------------------
# WRITE INDEX
# -----------------------------
$output | Set-Content -Path $outputFile -Encoding UTF8

# -----------------------------
# REPORT BROKEN LINKS
# -----------------------------
if ($brokenLinks.Count -gt 0) {
    Write-Warning "Broken links detected:"
    $brokenLinks | ForEach-Object { Write-Warning " - $_" }
}
else {
    Write-Host "All links validated successfully."
}

Write-Host "Index generated at: $outputFile"