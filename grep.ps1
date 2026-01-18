param(
    [Parameter(Mandatory)]
    [string]$Pattern,

    [string]$Path = "."
)

Get-ChildItem $Path -Recurse -File |
    Select-String -Pattern $Pattern |
    Select-Object Path, LineNumber, Line
