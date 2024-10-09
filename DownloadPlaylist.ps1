# Check if yt-dlp is installed, if not, download it
if (-Not (Get-Command yt-dlp -ErrorAction SilentlyContinue)) {
    Write-Host "yt-dlp is not installed. Downloading..."
    $ytDlpUrl = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
    $ytDlpPath = "$env:USERPROFILE\yt-dlp.exe"
    Invoke-WebRequest -Uri $ytDlpUrl -OutFile $ytDlpPath
    $env:Path += ";$env:USERPROFILE"
    Write-Host "yt-dlp downloaded and added to PATH."
} else {
    Write-Host "yt-dlp is already installed."
}

# Set the playlist URL
$playlistUrl = "https://youtube.com/playlist?list=PLeCpuN-qM8IZiscl5qozLcCJv_dGUsWg-&si=9f3VCeQhYgNwluBv"

# Download the playlist as MP3
$downloadCommand = "$ytDlpPath -x --audio-format mp3 --yes-playlist $playlistUrl"
Invoke-Expression $downloadCommand

Write-Host "Download complete!"