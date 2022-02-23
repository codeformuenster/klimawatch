$cities = "muenster", "koeln", "leipzig", "hamburg", "karlsruhe", "landau", "moers", "chemnitz", "berlin_verursacherbilanz", "muenchen", "duesseldorf", "paderborn", "dortmund", "bielefeld", "ulm"

for ($i = 0; $i -lt $cities.Length; $i++)
{
    $city = $cities[$i]
    Write-Output -InputObject $city
    if ($city -eq "karlsruhe")
    {
        python scripts/generate_plots.py $city 2007
    }
    else
    {
        python scripts/generate_plots.py $city
    }
}