[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$BaseUrl = "http://127.0.0.1:8000"

$Headers = @{
    "Authorization" = "Bearer agent_user1"
    "Content-Type"  = "application/json"
}

Write-Host "`n🚀 Starting BaseLock Integration Tests..."

# TEST 1
Write-Host "`n[TEST 1] SELECT Policy"
Invoke-RestMethod -Uri "$BaseUrl/generate-rls?table=projects&operation=SELECT" -Method POST -Headers $Headers | ConvertTo-Json -Depth 5

# TEST 2
Write-Host "`n[TEST 2] UPDATE Policy"
Invoke-RestMethod -Uri "$BaseUrl/generate-rls?table=projects&operation=UPDATE" -Method POST -Headers $Headers | ConvertTo-Json -Depth 5

# TEST 3
Write-Host "`n[TEST 3] History"
Invoke-RestMethod -Uri "$BaseUrl/policy-history?table=projects&operation=SELECT" -Method GET -Headers $Headers | ConvertTo-Json -Depth 5

# TEST 4
Write-Host "`n[TEST 4] Rollback"
Invoke-RestMethod -Uri "$BaseUrl/rollback-policy?table=projects&operation=SELECT&version=1" -Method POST -Headers $Headers | ConvertTo-Json -Depth 5

# TEST 5
Write-Host "`n[TEST 5] Attack Test"
Invoke-RestMethod -Uri "$BaseUrl/attack-test" -Method GET -Headers $Headers | ConvertTo-Json -Depth 5

Write-Host "`n🏁 All Tests Completed!"